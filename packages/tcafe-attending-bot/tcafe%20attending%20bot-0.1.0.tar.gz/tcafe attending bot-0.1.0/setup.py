#!/usr/bin/env python
# coding: UTF-8

from pathlib import Path

from setuptools import find_packages, setup

setup(
        name='tcafe attending bot',
        version=Path('VERSION').read_text(encoding='UTF-8'),
        author='Byeonghoon Yoo',
        author_email='bh322yoo@gmail.com',
        maintainer='Byeonghoon Yoo',
        maintainer_email='bh322yoo@gmail.com',
        description='Auto attending bot for TCafe',
        long_description=Path('README.md').read_text(encoding='UTF-8'),
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=('test',)),
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Framework :: AsyncIO',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: Korean',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: Implementation :: Stackless',
            'Typing :: Typed',
        ],
        keywords=['tcafe', 'bot'],
        license='MIT',
        python_requires='>=3.7',
        install_requires=Path('requirements.txt').read_text(encoding='UTF-8').splitlines(),
        zip_safe=True,
        entry_points={
            'console_scripts': [
                'tcafe_attending_bot = tcafe_attending_bot.__main__:console_entry',
            ]
        },
)
