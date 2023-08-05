"""
Usage:
  pgdatadiff --firstdb=<firstconnectionstring> --seconddb=<secondconnectionstring> [--only-data|--only-sequences] [--chunk-size=<size>]
  pgdatadiff --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --firstdb=postgres://postgres:password@localhost/firstdb        The connection string of the first DB
  --seconddb=postgres://postgres:password@localhost/seconddb         The connection string of the second DB
  --only-data        Only compare data, exclude sequences
  --only-sequences   Only compare seqences, exclude data
  --chunk-size=10000       The chunk size when comparing data [default: 10000]
"""

import pkg_resources
from fabulous.color import red

from pgdatadiff.pgdatadiff import DBDiff
from docopt import docopt


def main():
    arguments = docopt(
        __doc__, version=pkg_resources.require("pgdatadiff")[0].version)
    first_db_connection_string=arguments['--firstdb']
    second_db_connection_string=arguments['--seconddb']
    if not first_db_connection_string.startswith("postgres://") or \
            not second_db_connection_string.startswith("postgres://"):
        print(red("Only Postgres DBs are supported"))
        return 1

    differ = DBDiff(first_db_connection_string, second_db_connection_string,
                    chunk_size=arguments['--chunk-size'])
    if not arguments['--only-sequences']:
        differ.diff_all_table_data()
    if not arguments['--only-data']:
        differ.diff_all_sequences()
