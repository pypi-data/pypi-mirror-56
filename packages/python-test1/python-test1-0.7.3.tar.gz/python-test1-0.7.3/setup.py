from setuptools import setup
from setuptools import find_packages

install_requires = [
]

test_requires = []

setup(
    name='python-test1',
    version='0.7.3',
    description="Python Test program",
    author="suresh",
    author_email="sureshkumarr.s@gmail.com",
    url="https://github.com/sureshkvl/python-test",
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=install_requires,
    license="Apache",
    keywords='python',
    python_requires='>=2.6, <3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'Programming Language :: Python :: 2.7'
    ]
)
