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
    name='django-daraja',
    version='0.0.2',
    description='A python django library for interacting with the MPESA Daraja API.',
    long_description=
'''
This is a django module based on the MPESA daraja API. Use it to interact with the MPESA API in a simplified manner, abstracting the details for a simple, intuitive usage experience, as well as extensive error handling.    

Read the documentation at https://django-daraja.readthedocs.io

Daraja API documentation can be found at https://developer.safaricom.co.ke''',
    author='Martin Mogusu',
    author_email='martinmogusu@gmail.com',
    url='https://github.com/martinmogusu/django-daraja',
    download_url='https://github.com/martinmogusu/django-daraja.git',
    license='MIT License',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
        'python-decouple',
        'requests'
    ],
    tests_require=[
        'nose',
        'coverage',
    ],
    zip_safe=False,
    test_suite='tests.runtests.start',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='mpesa django daraja finance mobile-money',
    project_urls={
    'Documentation': 'https://django-daraja.readthedocs.io/',
    'Source': 'https://github.com/martinmogusu/django-daraja',
},
)