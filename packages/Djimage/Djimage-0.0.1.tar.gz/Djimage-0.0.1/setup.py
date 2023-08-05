from setuptools import find_packages, setup

import djimage

setup(
    name=djimage.__name__,
    version=djimage.__version__,
    packages=find_packages(),
    url='https://github.com/sainipray/djimage',
    author=djimage.__author__,
    author_email=djimage.__author_email__,
    description=djimage.__description__,
    include_package_data=True,
    platforms=['any'],
    install_requires=[
        "Pillow"
    ],
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
    ],
)