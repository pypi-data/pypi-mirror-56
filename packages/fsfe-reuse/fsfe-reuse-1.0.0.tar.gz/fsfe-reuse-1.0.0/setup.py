#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2019 Free Software Foundation Europe e.V.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from inspect import cleandoc

from setuptools import setup

requirements = [
    "reuse"
]

if __name__ == "__main__":
    setup(
        name="fsfe-reuse",
        version="1.0.0",
        url="https://reuse.software/",
        project_urls={
            "Documentation": "https://reuse.readthedocs.io/",
            "Source": "https://github.com/fsfe/reuse-tool",
        },
        license="GPL-3.0-or-later AND Apache-2.0 AND CC0-1.0 AND CC-BY-SA-4.0",
        author="Carmen Bianca Bakker",
        author_email="carmenbianca@fsfe.org",
        description="fsfe-reuse is an alias for reuse.",
        long_description=cleandoc(
            """
            As of version 0.7.0, [reuse](https://pypi.org/project/reuse/) is
            used instead of fsfe-reuse.

            If you still depend on fsfe-reuse, then you will automatically get
            the latest version of reuse. This dummy package depends on reuse.

            If you depend on a specific older version of fsfe-reuse, then you
            will continue to get that version.
            """
        ),
        long_description_content_type="text/markdown",
        install_requires=requirements,
    )
