import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bindglobal", # Replace with your own username
    version="0.0.3",
    author="segalion",
    author_email="segalion@gmail.com",
    description="python-tkinter-bind alike, for global desktop enviroment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/segalion/bindglobal",
    packages=setuptools.find_packages(),
    install_requires=[
        'pynput',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
