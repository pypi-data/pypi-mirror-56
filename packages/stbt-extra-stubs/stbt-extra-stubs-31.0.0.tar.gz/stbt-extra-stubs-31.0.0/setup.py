# coding: utf-8

import setuptools


long_description = """\
# stbt-extra-stubs

* Copyright © 2018-2019 Stb-tester.com Ltd.

This package contains API stubs for Stb-tester's premium features (such as
audio capture & analysis) which are only available when you run your test
scripts on the [Stb-tester Node] hardware. Installing this package will allow
your IDE to provide better linting & autocompletion, but you won't be able to
run these APIs locally.

[Stb-tester Node]: https://stb-tester.com
"""

setuptools.setup(
    name="stbt-extra-stubs",
    version="31.0.0",
    author="Stb-tester.com Ltd.",
    author_email="support@stb-tester.com",
    description="Stubs for Stb-tester's premium APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stb-tester.com",
    packages=["stbt"],
    classifiers=[
        # pylint:disable=line-too-long
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Testing",
    ],
    # I have only tested Python 2.7 & 3.6
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
)
