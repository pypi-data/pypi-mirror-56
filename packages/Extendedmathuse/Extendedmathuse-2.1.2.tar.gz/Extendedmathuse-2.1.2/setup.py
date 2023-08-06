import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Extendedmathuse", # Replace with your own username
    version="2.1.2",
    author="Tang Jiawei",
    author_email="3245813583@qq.com",
    description="Simple digital manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
