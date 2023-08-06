from __future__ import absolute_import
from __future__ import unicode_literals
import os
from setuptools import setup

base_dir = os.path.dirname(__file__)


def get_long_desciption():
    with open(os.path.join(base_dir, "README.md")) as f:
        return f.read()


setup(
    name='dimagi-memoized',
    version='1.1.3',
    description="A simple memoization decorator that's also memory efficient on instance methods",
    long_description=get_long_desciption(),
    long_description_content_type="text/markdown",
    url="https://github.com/dimagi/memoized",
    author='Dimagi',
    author_email='dev@dimagi.com',
    license='BSD-3',
    py_modules=['memoized'],
    install_requires=(),
    extras_require={
        'test': [
            'nose',
            'testil',
        ],
    },
    options={"bdist_wheel": {"universal": "1"}},
)
