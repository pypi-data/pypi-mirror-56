import pathlib
from setuptools import setup, find_packages


def get_version():
    for line in (HERE / "libbisca" / "__init__.py").read_text().split("\n"):
        if line.startswith("__version__"):
            return line.split('"')[1]


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = get_version()


setup(
    name="libbisca",
    version=VERSION,
    description="A Python bisca library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NunoMCSilva/libbisca",
    author="Nuno Miguel Casteloa da Silva",
    author_email="NunoMCSilva@gmail.com",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="bisca, cards, card game",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    tests_require=[
        "pytest>=5.2.2",
        "pytest-mock>=1.11.2",
        "pytest-mypy>=0.4.1",
        "pytest-cov>=2.8.1",
    ],
)
