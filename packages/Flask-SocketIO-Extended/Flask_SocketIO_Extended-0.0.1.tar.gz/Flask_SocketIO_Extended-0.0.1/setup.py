from setuptools import setup, find_packages


setup(
    name             = 'Flask_SocketIO_Extended',
    version          = '0.0.1',
    description      = 'Simple and easy SocketIO tool for Flask',
    long_description = open('README.md').read(),
    author           = 'MallyCrip',
    author_email     = 'pycon@kakao.com',
    install_requires = ['socketio','flask'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['api','socketio'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)