import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interspace", # Replace with your own username
    version="0.0.5",
    author="Rehan Guha",
    py_modules=["interspace"],
    author_email="rehanguha29@gmail.com",
    description="Interspace gives us different type distances between two vectors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rehanguha/interspace",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=2.7',
    install_requires=['numpy'],
)
