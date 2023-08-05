from setuptools import setup, find_packages


setup(
    name             = 'ChocoPY',
    version          = '0.1.5',
    long_description_content_type='text/markdown',
    description      = 'Simple and easy development tool for create chat bot',
    long_description = open('README.md').read(),
    author           = 'MallyCrip',
    author_email     = 'pycon@kakao.com',
    install_requires = ['flask'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['api','chat_bot'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)