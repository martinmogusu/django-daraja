import re
import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-daraja",
    version="1.0",
    description="A python django library for interacting with the MPESA Daraja API.",
    long_description=read('README.md'),
    author="Martin Mogusu",
    author_email="martinmogusu@gmail.com",
    url="https://github.com/martinmogusu/django-daraja",
    download_url="https://github.com/martinmogusu/django-daraja.git",
    license="MIT License",
    packages=[
        "django_daraja",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.11",
    ],
    tests_require=[
        "nose",
        "coverage",
    ],
    zip_safe=False,
    test_suite="tests.runtests.start",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)