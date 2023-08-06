from setuptools import setup, find_packages

setup(
    name = 'webvis',
    packages = find_packages(),
    version = '0.0.5',
    description = 'A live two-way data binder for python',
    author = 'Danil Lykov',
    author_email = 'lkvdan@gmail.com',
    url = 'https://github.com/DaniloZZZ/pywebviz',
    install_requires=['matplotlib', 'numpy', 'requests',
                      'mpld3','trio','trio-websocket'],
    python_requires='>=3.3',
    include_package_data=True,
    license='MIT',
    keywords = ['tools', 'data', 'framework', 'visualization'], # arbitrary keywords
    classifiers = [],
)
