import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Wigman", # Replace with your own username
    version="1.0.0",
    author="Amin Mahpour",
    author_email="amin.mgh.harvard@gmail.com",
    description="A package to plot genomic scores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AminMahpour/Wigman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
