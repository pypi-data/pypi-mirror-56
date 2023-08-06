#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/installation.rst') as install_file:
    install = install_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

INSTALL_REQUIRES = ['py-trello', 'ConfigArgParse', 'loguru']

setup_requirements = ['pytest-runner', ]

EXTRAS_REQUIRE = {
    "docs": ["sphinx", "watchdog[watchmedo]"],
    "tests": [
        "coverage",
        # "hypothesis",
        # "pympler",
        "pytest>=4.3.0",  # 4.3.0 dropped last use of `convert`
    ],
}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"] + ["pre-commit"]
)

setup(
    author="Matt Katz",
    author_email='github@morelightmorelight.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Take your weekly done cards and turn them into a bulleted list in another column, just like Alice Goldfuss does.",
    entry_points = {
                'console_scripts': ['trello-release=trello_release_notes.__main__:main'],
            },
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    license="MIT license",
    long_description=readme + '\n\n' + install + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='trello_release_notes',
    name='trello_release_notes',
    packages=find_packages(include=['trello_release_notes']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=EXTRAS_REQUIRE["tests"],
    url='https://github.com/mattkatz/trello_release_notes',
    version='0.3.1',
    zip_safe=False,
)
