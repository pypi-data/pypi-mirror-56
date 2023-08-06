import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="UTF-8") as fh:
    require = fh.readlines()
require = [x.strip() for x in require]

setuptools.setup(
    name="pySankey2",
    version="2.0.0",
    author="victor-galisson",
    author_email="victor.galisson@gmail.com",
    description="Make simple, pretty Sankey Diagrams as a matplotlib object",
    long_description=long_description,
    license="GNU General Public License v3.0",
    long_description_content_type="text/markdown",
    url="https://github.com/vgalisson/pySankey",
    packages=setuptools.find_packages(),
    install_requires=require,
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ),
)
