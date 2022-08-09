import argparse
import os
import sys
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone

sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/..')

from tools.utils import load_django  # noqa: E402

load_django()

from rental.models import House, HouseEtc  # noqa: E402

from crawler.spiders.detail591_spider import Detail591Spider  # noqa: E402

# Allow rerun in parallel, as id is sequential
PARTITION_SIZE = 30000
TRANSACTION_SIZE = 500

rows = []
total = 0
current_count = 0


def save(row, force=False):
    global rows
    global total
    global current_count
    global TRANSACTION_SIZE
    if row:
        rows.append(row)
    if len(rows) >= TRANSACTION_SIZE or force:
        with transaction.atomic():
            try:
                for r in rows:
                    r.save()
                print(f'[{timezone.localtime()}] Done {current_count}/{total} rows')
                rows = []
            except BaseException:
                traceback.print_exc()


def parse(partition_size, partition_index):
    global total
    global current_count
    global TRANSACTION_SIZE

    id_lower = partition_size * partition_index
    id_upper = partition_size * (partition_index + 1)

    etcs = (
        HouseEtc.objects.filter(detail_dict__isnull=False, house_id__gte=id_lower, house_id__lt=id_upper)
        .order_by('house')
        .values('house', 'vendor_house_id', 'detail_dict')
    )

    paginator = Paginator(etcs, TRANSACTION_SIZE)
    detailSpider = Detail591Spider()

    total = paginator.count
    print(f'==== Total {total} rows in id[{id_lower}:{id_upper}] to rerun ====')

    for page_num in paginator.page_range:
        etcs_page = paginator.page(page_num)

        for etc in etcs_page:
            house = House.objects.get(pk=etc['house'])
            try:
                if type(etc['detail_dict']) is dict:
                    detail_dict = etc['detail_dict']
                else:
                    detail_dict = etc['detail_dict']

                share_attrs = detailSpider.gen_shared_attrs(detail_dict, house)
                for attr in share_attrs:
                    setattr(house, attr, share_attrs[attr])
                    setattr(house, attr, share_attrs[attr])
                current_count += 1
                save(house)
            except BaseException:
                print(f'error in {house.id}')
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
