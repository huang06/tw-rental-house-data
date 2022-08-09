import argparse
import os
import sys
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from scrapy.http import HtmlResponse, Request

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')

from tools.utils import load_django  # noqa: E402

load_django()

from rental.models import House, HouseEtc  # noqa: E402

from crawler.items import GenericHouseItem, RawHouseItem  # noqa: E402
from crawler.spiders.detail591_spider import Detail591Spider  # noqa: E402

# Allow rerun in parallel, as id is sequential
PARTITION_SIZE = 30000
TRANSACTION_SIZE = 500

rows = []
total = 0
cur_count = 0


def save(row, force=False):
    global rows
    global total
    global cur_count
    global TRANSACTION_SIZE
    if row:
        rows.append(row)
    if len(rows) >= TRANSACTION_SIZE or force:
        with transaction.atomic():
            try:
                for r in rows:
                    r.save()
                print(f'[{timezone.localtime()}] Done {cur_count}/{total} rows')
                rows = []
            except BaseException:
                traceback.print_exc()


def parse(partition_size, partition_index):
    global total
    global cur_count
    global TRANSACTION_SIZE

    id_lower = partition_size * partition_index
    id_upper = partition_size * (partition_index + 1)

    etcs = (
        HouseEtc.objects.filter(detail_raw__isnull=False, house_id__gte=id_lower, house_id__lt=id_upper)
        .order_by('house')
        .values('house', 'vendor_house_id', 'detail_raw')
    )

    paginator = Paginator(etcs, TRANSACTION_SIZE / 2)
    detailSpider = Detail591Spider()

    total = paginator.count
    print(f'==== Total {total} rows in id[{id_lower}:{id_upper}] to rerun ====')

    for page_num in paginator.page_range:
        etcs_page = paginator.page(page_num)
        for etc in etcs_page:
            cur_count += 1
            request = Request(**detailSpider.gen_request_params({'house_id': etc['vendor_house_id']}))
            response = HtmlResponse('', status=200, request=request, body=etc['detail_raw'].encode('utf-8'))
            try:
                for item in detailSpider.parse_detail(response):
                    if type(item) is RawHouseItem:
                        if 'dict' in item and not item['is_list']:
                            etc_row = HouseEtc.objects.get(pk=etc['house'])
                            etc_row.detail_dict = item['dict']
                            save(etc_row)
                    elif type(item) is GenericHouseItem:
                        to_db = item.copy()
                        house = House.objects.get(pk=etc['house'])
                        del to_db['vendor']
                        del to_db['vendor_house_id']

                        for attr in to_db:
                            if attr in to_db:
                                setattr(house, attr, to_db[attr])

                        save(house)
            except BaseException:
                seed = request.meta.get('seed')
                print(f'error in {seed}')
                traceback.print_exc()

    save(None, True)


def parse_number(input):
    try:
        return int(input, 10)
    except ValueError:
        raise argparse.ArgumentTypeError(f'Invalid number: {input}')


arg_parser = argparse.ArgumentParser(description='Rerun parser from raw html to update house table')
arg_parser.add_argument(
    '-ps',
    '--partition-size',
    dest='partition_size',
    default=PARTITION_SIZE,
    type=parse_number,
    help=f'size of one partition, default {PARTITION_SIZE}',
)

arg_parser.add_argument(
    '-pi',
    '--partition-index',
    dest='partition_index',
    default=0,
    type=parse_number,
    help='which partition to run',
)

if __name__ == '__main__':
    args = arg_parser.parse_args()

    partition_size = args.partition_size
    partition_index = args.partition_index

    parse(partition_size, partition_index)
