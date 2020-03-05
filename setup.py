import setuptools

with open("README.md", "r") as f:
    desc = f.read()

setuptools.setup(
    name="comment-tree-py",
    version="0.0.1",
    author="Ilya Chesalin",
    author_email="evilyach@protonmail.com",
    description="Comment Tree Py CLI app to add comments to a JSON concurrently using jsonplaceholder.typicode.com API",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/evilyach/comment-tree-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
