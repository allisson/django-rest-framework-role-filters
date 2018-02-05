import codecs
import os
import re

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

version = '0.0.0'
changes = os.path.join(here, 'CHANGES.rst')
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group('version')
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()


install_requirements = [
    'djangorestframework>=3.5.4',
]
tests_requirements = [
    'django',
    'pytest',
    'pytest-cov',
    'pytest-django',
]


class VersionCommand(Command):
    description = 'print library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='djangorestframework-role-filters',
    version=version,
    description='django-rest-framework-role-filters',
    long_description=long_description,
    url='https://github.com/allisson/django-rest-framework-role-filters',
    author='Allisson Azevedo',
    author_email='allisson@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='djangorestframework rest role permission',
    packages=find_packages(exclude=['docs', 'tests*']),
    setup_requires=['pytest-runner'],
    install_requires=install_requirements,
    tests_require=tests_requirements,
    cmdclass={
        'version': VersionCommand,
    },
)
