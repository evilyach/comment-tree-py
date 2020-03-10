import setuptools

with open("README.md", "r") as f:
    desc = f.read()

setuptools.setup(
    name="comment-tree-py",
    version="0.0.1",
    packages=setuptools.find_packages(),

    python_requires=">=3.7",
    install_requires=[
        'astroid==2.3.3',
        'autopep8==1.5',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'gevent==1.4.0',
        'greenlet==0.4.15',
        'grequests==0.4.0',
        'idna==2.8',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.3',
        'mccabe==0.6.1',
        'pycodestyle==2.5.0',
        'pylint==2.4.4',
        'requests==2.22.0',
        'six==1.14.0',
        'urllib3==1.25.8',
        'wrapt==1.11.2',
    ],

    author="Ilya Chesalin",
    author_email="evilyach@protonmail.com",
    description="Comment Tree Py CLI app to add comments to a JSON concurrently using jsonplaceholder.typicode.com API",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/evilyach/comment-tree-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
