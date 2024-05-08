import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astDeadcodeRemover",
    version="0.0.1", 
    author="Rafał Roszak",
    description="Very simple software to remove deadcode from *py files based on ast module",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GPL License",
                 "Operating System :: OS Independent", ],
    python_requires='>=3.9',
    py_modules=["astDeadcodeRemover"],
    package_dir={'':'astDeadcodeRemover/src'},
    install_requires=[]
)