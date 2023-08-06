import os
from setuptools import setup, find_packages

def read_file(filename):
    basepath=os.path.dirname(os.path.dirname(__file__))
    filepath=os.path.join(basepath, filename)
    if os.path.exists(filepath):
        return open(filepath, encoding='utf8').read()
    else:
        return ''

setup(
    name='Rambo_zhou_guestbook',
    version='1.0.1',
    description='A guestbook web application.',
    author = 'rambo_zhou',
    author_email='zjy13929412080139@126.com',
    url='https://rambo_zhou@bitbucket.org/rambo_zhou/guestbook/',
    long_description = read_file ('README.rst'),
    classifiers=['Development Status :: 4 - Beta',
        'Framework :: Flask',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords= ['web', 'guestbook'],
    license='BSD License',
    install_requires=[
    'Flask',
    ],
    entry_points="""
        [console_scripts]
        guestbook=guestbook:main
    """,
    )
