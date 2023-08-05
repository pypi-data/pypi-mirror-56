# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_forms_recaptcha_plugin import __version__


setup(
    name='aldryn-forms-recaptcha-plugin',
    version=__version__,
    description='This package provides a simple invisible recaptcha v3 implementation',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='what.digital',
    author_email='mario@what.digital',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[
        'aldryn_forms>=4',
        'django-recaptcha>=2',
    ],
    download_url='https://gitlab.com/what-digital/aldryn-forms-recaptcha-plugin/-/archive/{}/aldryn-forms-recaptcha-plugin-{}.tar.gz'.format(
        __version__,
        __version__
    ),
    url='https://gitlab.com/what-digital/aldryn-forms-recaptcha-plugin/tree/master',
    include_package_data=True,
    zip_safe=False,
)
