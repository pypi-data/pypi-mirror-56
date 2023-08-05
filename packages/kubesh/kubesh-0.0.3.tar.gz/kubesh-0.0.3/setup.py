from setuptools import setup
import sys
import os
import io

assert sys.version_info >= (3, 6, 0), "requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def setup_package():

    # Get readme
    readme_path = os.path.join(CURRENT_DIR, "README.md")
    with io.open(readme_path, encoding="utf8") as f:
        readme = f.read()

    setup(long_description=readme, long_description_content_type="text/markdown")


if __name__ == "__main__":
    setup_package()
