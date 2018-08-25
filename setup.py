"""
virtualmod
==========
"""
from setuptools import setup


def get_long_description():
    with open('README.md') as f:
        rv = f.read()
    return rv


setup(
    name='virtualmod',
    version='1.0.0',
    url='https://github.com/brettlangdon/virtualmod',
    license='MIT',
    author='Brett Langdon',
    author_email='me@brett.is',
    description='Python package for creating and importing virtual modules.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    py_modules=['virtualmod'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
    ]
)
