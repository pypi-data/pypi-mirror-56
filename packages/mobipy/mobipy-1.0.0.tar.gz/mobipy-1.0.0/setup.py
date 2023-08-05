import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mobipy',
    version="1.0.0",
    author='Pedro Maia',
    author_email='pedro.maia@ccc.ufcg.edu.br',
    description='A library for analyzing user mobility patterns',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/pedrohcm/mobipy',
	packages=['mobipy'],
    install_requires=['geopy', 'pandas', 'numpy', 'sklearn', 'shapely'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)