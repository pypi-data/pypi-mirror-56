"""
Samba

A small PAAS to deploy Flask/Django, Node, PHP and Static HTML sites using GIT, similar to Heroku

https://github.com/mardix/samba/

"""

from setuptools import setup, find_packages


__summary__ = "A very small PaaS to do git push app deployments to your own servers, similar to Heroku"
__uri__ = "https://github.com/mardix/samba/"
setup(
    name="samba",
    version="0.0.0",
    license="MIT",
    author="Mardix",
    author_email="mcx2082@gmail.com",
    description=__summary__,
    long_description=__doc__,
    url="https://github.com/mardix/samba/",
    download_url='https://github.com/mardix/samba/tarball/master',
    py_modules=['samba'],
    packages=find_packages(),
    install_requires=[
        'virtualenv',
        'uwsgi',
        'click',
    ],
    keywords=['deploy', 'samba', 'flask', 'gunicorn', 'django', 'workers', 'heroku', 'firebase', 'dokku', 'paas'],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
