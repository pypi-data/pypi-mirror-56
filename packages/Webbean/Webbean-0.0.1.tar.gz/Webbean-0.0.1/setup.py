from setuptools import setup, find_packages


setup(
    name="Webbean",
    version="0.0.1",
    author="Pesche Romain",
    author_email="rpesche@pesche.fr",
    description=("An application to get transactions diff"
                 "between accounting file and bank"),
    license="GNU AGPL 3",
    packages=find_packages(),
    install_requires=['beancount', 'weboob==1.3', 'Jinja2==2.10.3', 'Unidecode==1.1.1'],
    include_package_data=True,
    keywords="accounting weboob synchronization",
    url="http://packages.python.org/webbean",
    long_description=open('README').read(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: BSD License",
    ],

    entry_points={
            'console_scripts': [
                'webbean = webbean.bank:main',
            ],
        },
)
