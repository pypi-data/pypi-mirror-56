import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name='tractorcan',
    version='0.1',
    author="John Darrington",
    author_email="johnw.darrington@gmail.com",
    description="An open source J1939 CAN bus reader configured for raspberry pi zero",
    long_description_content_type="text/markdown",
    url="https://github.com/dnoberon/tinCAN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
