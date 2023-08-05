from setuptools import setup, find_packages


setup(
    name             = 'ChocoPY',
    version          = '0.0.1',
    description      = 'ChocoPY is XXX',
    long_description = open('README.md').read(),
    author           = 'MallyCrip',
    author_email     = 'pycon@kakao.com',
    install_requires = ['requests'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['api'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)