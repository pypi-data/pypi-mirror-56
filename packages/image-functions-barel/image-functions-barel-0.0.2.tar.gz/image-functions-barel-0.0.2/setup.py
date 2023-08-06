import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image-functions-barel",
    version="0.0.2",
    author="Barel Levy",
    author_email="barel.levy.bl@gmail.com",
    description="Helper functions for image processing tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Barelos/MyLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
        "opencv-python",
        "pillow"
    ],
)
