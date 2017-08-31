from setuptools import setup

setup(
    name='in_downloader',
    version='0.1',
    py_modules=['in_downloader'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        in_downloader=inet_dowloader.lib.commands:in_downloader
    ''',
)