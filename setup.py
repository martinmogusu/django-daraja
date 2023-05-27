import re
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-daraja",
    version="1.3.0",
    description="A python django library for interacting with the Safaricom MPESA Daraja API.",
    long_description="""
This is a django library based on the Safaricom MPESA daraja API. Use it for a simplified experience, spend less time setting up...

Read the full documentation at https://django-daraja.readthedocs.io

MPESA Daraja API documentation can be found at https://developer.safaricom.co.ke""",
    author="Martin Mogusu",
    author_email="martinmogusu@gmail.com",
    url="https://github.com/martinmogusu/django-daraja",
    download_url="https://github.com/martinmogusu/django-daraja.git",
    license="MIT License",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=["Django>=1.11", "python-decouple", "requests", "cryptography"],
    tests_require=[
        "nose",
        "coverage",
    ],
    zip_safe=False,
    test_suite="tests.runtests.start",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="mpesa django daraja finance mobile-money safaricom api",
    project_urls={
        "Documentation": "https://django-daraja.readthedocs.io/",
        "Source": "https://github.com/martinmogusu/django-daraja",
    },
)
