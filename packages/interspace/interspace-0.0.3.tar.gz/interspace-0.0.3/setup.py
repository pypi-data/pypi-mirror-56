import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interspace", # Replace with your own username
    version="0.0.3",
    author="Rehan Guha",
    py_modules=["interspace"],
    author_email="rehanguha29@gmail.com",
    description="A package to claculate various distances given 2 points as input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rehanguha/interspace",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
