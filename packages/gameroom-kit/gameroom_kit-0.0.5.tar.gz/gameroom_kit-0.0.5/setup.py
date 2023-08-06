import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gameroom_kit",
    version="0.0.5",
    author="InfiniteToken",
    author_email="infinitetoken@gmail.com",
    description="A Python package for the Gameroom API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gameroomforpresident/GameroomKit-Python",
    packages=setuptools.find_packages(),
    installRequires=[
        'uuid',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
