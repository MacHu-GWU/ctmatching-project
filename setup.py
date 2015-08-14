#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
    LONG_DESCRIPTION = f.read().decode("utf-8")
VERSION = __import__("ctmatching").__version__

setup(
  name = "ctmatching",
  packages = find_packages(),
  package_data = {"ctmatching": ["testdata/re78.txt"]},
  version = VERSION,
  description = "Treatment group, control group matching algorithm high level python implementation.",
  long_description=LONG_DESCRIPTION,
  author = "Sanhe Hu",
  author_email = "husanhe@gmail.com",
  url = "https://github.com/MacHu-GWU/ctmatching",
  download_url = "https://github.com/MacHu-GWU/ctmatching/tarball/0.2",
  keywords = ["statistic", "match"],
)