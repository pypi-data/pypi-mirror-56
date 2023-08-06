from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
setup(
    name = 'webvis',
    packages = find_packages(),
    version = '0.0.8',
    description = 'A live two-way data binder for python',
    author = 'Danil Lykov',
    author_email = 'lkvdan@gmail.com',
    url = 'https://github.com/DaniloZZZ/pywebviz',
    install_requires=['matplotlib', 'numpy', 'requests',
                      'mpld3','trio','trio-websocket'],
    python_requires='>=3.3',
    include_package_data=True,
    license='MIT',
    keywords = ['tools', 'data', 'framework', 'visualization'], 
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers = [],
)
