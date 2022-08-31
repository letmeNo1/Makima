import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setuptools.setup(
    name="Makima",
    version="0.1.5",
    author="hank.huang",
    author_email="hank.huang550@gmail.com",
    description="A cross-platform desktop automated testing framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/letmeNo1/Makima",
    packages=setuptools.find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
