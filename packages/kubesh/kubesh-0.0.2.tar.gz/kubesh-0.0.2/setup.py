from setuptools import setup
import sys

assert sys.version_info >= (3, 6, 0), "requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def setup_package():
    setup()


if __name__ == "__main__":
    setup_package()
