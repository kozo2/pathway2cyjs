from setuptools import setup

__version__ = '0.0.1'

with open("README.md") as f:
    long_description = f.read()

setup(
    name='pathway2cyjs',
    version=__version__,
    url='https://github.com/ecell/pathway2cyjs',
    license='MIT',
    py_modules=['pathway2cyjs'],
    python_requires='>=3.6',
    author='Kozo Nishida',
    author_email='knishida@riken.jp',
    install_requires=['requests'],
    description='Convert Escher, Wikipathways, KEGG data to Cytoscape.js JSON (.cyjs)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=['License :: OSI Approved :: MIT License',]
)
