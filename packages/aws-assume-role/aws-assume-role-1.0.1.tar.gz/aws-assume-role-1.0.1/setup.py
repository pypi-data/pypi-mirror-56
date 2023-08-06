#!/usr/bin/env python3

import io

from setuptools import setup

version = "1.0.1"

requirements = [
    'boto3>=1.10',
    'click>=7.0',
]

with io.open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='aws-assume-role',
    version=version,
    description=('A helper tool to help you assume AWS roles'),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Yudi A Phanama',
    url='https://github.com/phanama/aws-assume-role',
    packages=[
        'aws_assume_role',
    ],
    package_dir={'aws_assume_role': 'aws_assume_role'},
    entry_points={
        'console_scripts': [
            'aws-assume-role = aws_assume_role.__main__:main',
        ]
    },
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=requirements,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
    keywords=(
        'aws-assume-role, aws, Python, assume-role,'
    ),
)