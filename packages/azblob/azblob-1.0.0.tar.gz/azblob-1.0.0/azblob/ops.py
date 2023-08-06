import argparse
import logging
import os
import sys

from azure.storage.blob import BlobClient, ContainerClient
import tabulate

logger = logging.getLogger("azblob")
logger.setLevel(logging.DEBUG)
console_logger_handler = logging.StreamHandler()
console_logger_handler.setLevel(logging.INFO)
console_logger_formatter = logging.Formatter(
    "%(asctime)s|%(name)s|%(levelname)s::%(message)s", "%m-%d@%H:%M"
)
console_logger_handler.setFormatter(console_logger_formatter)
logger.addHandler(console_logger_handler)


def parse_credentials(accountname, accountkey):
    accountname = accountname or os.environ["AZBLOB_ACCOUNTNAME"]
    accountkey = accountkey or os.environ.get("AZBLOB_ACCOUNTKEY")
    return accountname, accountkey


def credentials(f):
    def f_with_credentials(*args, **kwargs):
        kwargs["accountname"], kwargs["accountkey"] = parse_credentials(
            kwargs["accountname"], kwargs["accountkey"]
        )
        logger.info("Azure storage account name: '{}'".format(kwargs["accountname"]))
        if kwargs["accountkey"] is None:
            logger.info("using anonymous access.")
        return f(*args, **kwargs)

    return f_with_credentials


@credentials
def downloadapi(
    container, blob, accountname=None, accountkey=None, replace=True, blob_target=None
):
    block_blob_service = BlobClient(
        accountname, container, blob, credential=accountkey
    )
    blob_target = blob_target or os.path.join(os.getcwd(), blob)
    if not replace and os.path.isfile(blob_target):
        logger.info(
            "will skip download, {} already exists and replace=False".format(
                blob_target
            )
        )
        return
    logger.info("downloading '{}/{}' to '{}'".format(container, blob, blob_target))
    with open(blob_target, "wb") as f:
        blob_data = block_blob_service.download_blob()
        blob_data.readinto(f)
    logger.info("finished download")


def download(container, blob, accountname=None, accountkey=None, replace=True, target=None):
    downloadapi(
        container,
        blob,
        accountname=accountname,
        accountkey=accountkey,
        replace=replace,
        blob_target=target,
    )


@credentials
def listblobsapi(container, accountname, accountkey=None, nmax=None):
    block_blob_service = ContainerClient(
        accountname, container, credential=accountkey
    )
    logger.info("listing blobs in '{}/{}'".format(accountname, container))
    if nmax is None:
        nmax = sys.maxsize
    blobs = block_blob_service.list_blobs()
    # TODO use namedtuple
    blob_list = [
        {"name": blob.name, "date": blob.creation_time}
        for i, blob in enumerate(blobs)
        if i < nmax
    ]
    return blob_list


def listblobs(container, accountname=None, accountkey=None, nmax=None):
    blobs = listblobsapi(
        container, accountname=accountname, accountkey=accountkey, nmax=nmax
    )
    table_header = ("Name", "Date")
    table_rows = [(blob["name"], blob["date"]) for blob in blobs]
    print(tabulate.tabulate(table_rows, headers=table_header))
    


def cli():
    # azblob
    parser = argparse.ArgumentParser(
        description="minimal Azure blob storage operations"
    )
    parser.add_argument("-n", "--accountname", default=None)
    parser.add_argument("-k", "--accountkey", default=None)

    subparsers = parser.add_subparsers(dest="operation", help="blob operations")

    # azblob download
    parser_get = subparsers.add_parser("download", help="download blob")
    parser_get.add_argument("container", help="container name")
    parser_get.add_argument("blob", help="blob name (file name)")
    parser_get.add_argument(
        "--dontreplace",
        action="store_true",
        help="Check if target download path exists and if so then dont download.",
    )
    parser_get.add_argument(
        "--target", default=None,
        help="Target file name.",
    )

    # azblob list
    parser_get = subparsers.add_parser(
        "list", help="list containers and blob in containers"
    )
    parser_get.add_argument("container", help="container name")
    parser_get.add_argument(
        "--nmax", type=int, help="maximum number of blobs to list", default=10
    )

    args = parser.parse_args()
    logger.debug("cli args: op={}".format(args.operation))

    if args.operation == "download":
        download(
            args.container,
            args.blob,
            accountname=args.accountname,
            accountkey=args.accountkey,
            replace=not args.dontreplace,
            target=args.target
        )
    elif args.operation == "list":
        listblobs(args.container, args.accountname, args.accountkey, args.nmax)


if __name__ == "__main__":
    cli()
