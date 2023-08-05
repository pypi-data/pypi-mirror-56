from setuptools import setup, find_packages


setup(
    name             = 'ChocoPY',
    version          = '0.1.3',
    description      = 'ChocoPY is simple and easy development tool for ChatBot',
    long_description = open('README.md').read(),
    author           = 'MallyCrip',
    author_email     = 'pycon@kakao.com',
    install_requires = ['requests','flask'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['api'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)