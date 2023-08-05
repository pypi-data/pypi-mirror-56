import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.0.2'

setup(
    name='matyan',
    version=version,
    description="Generate changelog from Git commits.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
    ],
    keywords='Changelog, Git, feature branches, gitflow, JIRA, agile, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/matyan',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    entry_points={
        'console_scripts': [
            # Standard
            'json-changelog = matyan.utils:json_changelog_cli',
            'generate-changelog = matyan.utils:generate_changelog_cli',
            # Backups
            'matyan-json-changelog = matyan.utils:json_changelog_cli',
            'matyan-generate-changelog = matyan.utils:generate_changelog_cli',
        ]
    },
    include_package_data=True,
    license='GPL-2.0-only OR LGPL-2.0-or-later',
    install_requires=[
        'GitPython',
    ],
    test_suite='tld.tests',
    tests_require=[
        'coverage',
        'factory_boy',
        'Faker',
        'pytest-cov',
        'pytest',
        'tox',
    ]
)
