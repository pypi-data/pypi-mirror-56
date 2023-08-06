import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="voronoi-wall", # Replace with your own username
    version="0.0.1",
    author="NCSU",
    author_email="drsheehy@ncsu.edu",
    description="It's a Voronoi wall.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/VoronoiWall",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)