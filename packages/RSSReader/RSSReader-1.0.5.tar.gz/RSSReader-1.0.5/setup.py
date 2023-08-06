import setuptools

with open("README.md",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="RSSReader", # Replace with your own username
    version="1.0.5",
    author="tim",
    author_email="tim_xia@icloud.com",
    description="a simple Schedule of RSS Reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)