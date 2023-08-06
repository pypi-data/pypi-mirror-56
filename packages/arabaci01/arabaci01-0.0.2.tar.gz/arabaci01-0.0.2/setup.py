import setuptools

setuptools.setup(
    name="arabaci01", # Replace with your own username
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description_content_type="text/markdown",
    url="https://github.com/Ahmet57/araba",
    packages=setuptools.find_packages(),
    install_requires=['PySide2','numpy','qdarkstyle', 'torchvision'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

