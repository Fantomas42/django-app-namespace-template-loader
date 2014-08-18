"""Setup script for django-app-namespace-template-loader"""
import os

from setuptools import setup
from setuptools import find_packages

__version__ = '0.2'
__license__ = 'BSD License'

__author__ = 'Fantomas42'
__email__ = 'fantomas42@gmail.com'

__url__ = 'https://github.com/Fantomas42/django-app-namespace-template-loader'


setup(
    name='django-app-namespace-template-loader',
    version=__version__,
    zip_safe=False,

    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    author=__author__,
    author_email=__email__,
    url=__url__,

    license=__license__,
    platforms='any',
    description='Template loader allowing you to both '
                'extend and override a template at the same time. ',
    long_description=open(os.path.join('README.rst')).read(),
    keywords='django, template, loader',
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=['six']
)
