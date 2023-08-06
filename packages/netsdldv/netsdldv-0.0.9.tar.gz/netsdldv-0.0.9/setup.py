import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_descrip = fh.read()

setuptools.setup(
    name='netsdldv',
    version='0.0.9',
    description='a tools for ami',
    long_description=long_descrip,
    long_description_content_type="text/markdown",
    url='https://git.netsdl.com/dv/DvManager',
    author='codmowa',
    author_email='chenchu@netsdl.com',
    license='MIT',
    keywords='ami dv python',
    package_dir={'': '.'},
    install_requires=['pyodbc >= 4.0.27', 'SQLAlchemy >= 1.3.11'],
    packages=setuptools.find_namespace_packages(exclude=["*test*"])
)
