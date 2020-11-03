import argparse
import logging


def set_up_logging(verbose: int = 1) -> None:
    if verbose > 2:
        level = logging.DEBUG
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    log_format = (
        "%(levelname)s:%(asctime)s:%(name)s:%(filename)s:"
        "%(funcName)s:%(lineno)d:%(message)s"
    )
    logging.basicConfig(format=log_format, level=level)


def default_arguments(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--camera", help="Camera number.", type=int, default=0)
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        default=0,
        nargs="+",
        help="Logging verbosity",
    )
    return parser
