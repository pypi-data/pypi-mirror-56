from setuptools import setup, find_packages

setup(
    name='sussex',
    version='0.2',
    license='MIT',
    author = 'Simon Sorensen',
    author_email='hello@simse.io',
    url='https://simse.io',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'BeautifulSoup4',
        'yaspin'
    ],
    entry_points='''
        [console_scripts]
        sussex=sussex.cli:cli
    ''',
)