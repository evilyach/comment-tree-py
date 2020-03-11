import setuptools


def readme():
    with open("README.md", "r") as f:
        return f.read()


install_requirements = [
    "astroid==2.3.3",
    "autopep8==1.5",
    "certifi==2019.11.28",
    "chardet==3.0.4",
    "gevent==1.4.0",
    "greenlet==0.4.15",
    "grequests==0.4.0",
    "idna==2.8",
    "isort==4.3.21",
    "lazy-object-proxy==1.4.3",
    "mccabe==0.6.1",
    "pycodestyle==2.5.0",
    "pylint==2.4.4",
    "requests==2.22.0",
    "six==1.14.0",
    "urllib3==1.25.8",
    "wrapt==1.11.2",
]


setuptools.setup(
    name="comment-tree",
    version="0.0.1",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "comment-tree = comment_tree:main",
            "comment-tree-json = json_gen.json_generator:main",
        ]
    },

    python_requires=">=3.7",
    install_requires=install_requirements,

    author="Ilya Chesalin",
    author_email="evilyach@protonmail.com",
    description="Comment Tree Py CLI app to add comments to a JSON concurrently using jsonplaceholder.typicode.com API",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/evilyach/comment-tree-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
