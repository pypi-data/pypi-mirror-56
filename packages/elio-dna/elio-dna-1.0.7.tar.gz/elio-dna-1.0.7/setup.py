# -*- coding: utf-8 -*-
import os
import setuptools
from distutils.core import setup


def read_file_into_string(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ""


def get_readme():
    if os.path.exists("README.md"):
        return read_file_into_string("README.md")
    return ""


setup(
    name="elio-dna",
    packages=[
        "dna",
        "dna.management",
        "dna.management.commands",
        "dna.templatetags",
    ],
    package_data={"dna": ["templates/*.*", "templates/dna/*.*"]},
    install_requires=[
        "elio-apep",
        "Django",
        "django-polymorphic",
        "easy-thumbnails",
        "Pillow",
        "python-slugify",
    ],
    include_package_data=True,
    version="1.0.7",
    description="Django models, views, forms, and templates, built on schema.org Things the elioWay.",
    author="Tim Bushell",
    author_email="tcbushell@gmail.com",
    url="https://elioway.gitlab.io/eliothing/dna",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
    ],
    license="MIT",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
)
