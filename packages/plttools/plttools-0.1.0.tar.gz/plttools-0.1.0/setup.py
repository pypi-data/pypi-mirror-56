import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
    name="plttools",
    version="0.1.0",
    description="Interact with PLTs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/anishpatelwork/plttools",
    author="Anish Patel",
    license="MIT",
    packages=["plttools"]
)
