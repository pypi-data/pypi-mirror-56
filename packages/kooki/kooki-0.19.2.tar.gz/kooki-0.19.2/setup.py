#!/usr/bin/env python
import textwrap

from setuptools import find_packages, setup

__version__ = "0.19.2"

long_description = textwrap.dedent(
    """\
    |build_status|_
    |coverage|_
    |pypi_version|_

    Kooki is a powerful template system that help you create documents with Markdown and YAML.
    Kooki come with different extensions that let you generate HTML, LaTeX and even more.

    Need more info, look at the documentation. `kooki.gitlab.io <http://www.python.org/>`_.

    .. |build_status| image:: https://gitlab.com/kooki/kooki/badges/master/build.svg
    .. _build_status: https://gitlab.com/kooki/kooki/commits/master
    .. |coverage| image:: https://gitlab.com/kooki/kooki/badges/master/coverage.svg?job=coverage
    .. _coverage: https://kooki.gitlab.io/kooki/coverage
    .. |pypi_version| image:: https://badge.fury.io/py/kooki.svg
    .. _pypi_version: https://badge.fury.io/py/kooki
    """
)

setup(
    name="kooki",
    version=__version__,
    description="The ultimate document generator.",
    long_description=long_description,
    keywords="document generator template markdown YAML",
    author="Noel Martignoni",
    include_package_data=True,
    package_data={"kooki.config": ["format.yaml"]},
    author_email="noel@martignoni.fr",
    url="https://gitlab.com/kooki/kooki",
    scripts=["scripts/kooki"],
    install_requires=[
        "empy==3.3.2",
        "pyyaml==3.12",
        "toml==0.10.0",
        "termcolor==1.1.0",
        "mistune==0.8.4",
        "karamel==0.2.2",
        "cerberus==1.2",
        "munch==2.3.2",
        "packaging==18.0",
    ],
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
