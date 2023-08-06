from setuptools import setup, find_packages
import os

version = '1.1.0'

tests_require = [
    'plone.app.testing'
]

setup(
    name='ftw.slacker',
    version=version,
    description='Uses webhooks to post messages into a slack channel.',
    long_description=(open('README.rst').read() + '\n' +
                      open(os.path.join('docs', 'HISTORY.txt')).read()),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "Framework :: Zope :: 2",
        "Framework :: Zope :: 4",
        "Framework :: Zope",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords='ftw slacker slack webhoock api',
    author='4teamwork AG',
    author_email='mailto:info@4teamwork.ch',
    url='https://git.4teamwork.ch/ftw/ftw.slacker',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ftw'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'setuptools',
        'Plone',
        'requests',
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
