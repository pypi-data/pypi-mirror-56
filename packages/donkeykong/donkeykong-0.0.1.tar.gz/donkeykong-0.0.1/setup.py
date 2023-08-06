from setuptools import setup, find_packages

setup(
    name='donkeykong',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/maurosilber/donkeykong',
    license='MIT',
    author='Mauro Silberberg',
    author_email='maurosilber@gmail.com',
    description='A monkey-patching of Luigi.',
    install_requires=['luigi', 'click', 'tabulate'],
    extras_requires=['numpy', 'pandas', 'tifffile'],
    entry_points={'console_scripts': ['donkeykong = donkeykong.scripts.main:main']}
)
