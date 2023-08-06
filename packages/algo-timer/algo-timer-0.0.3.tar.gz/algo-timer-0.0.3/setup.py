import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algo-timer",
    version="0.0.3",
    author="Xiangzhuang Shen",
    author_email="datahonor@gmail.com",
    description="An easy-to-use algorithms timer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shenxiangzhuang/algo-timer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
