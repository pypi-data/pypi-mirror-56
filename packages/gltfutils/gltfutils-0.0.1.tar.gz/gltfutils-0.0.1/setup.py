import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="gltfutils",
    version="0.0.1",
    author="springtangent",
    author_email="springtangent42@gmail.com",
    description="A set of python libraries for reading, manipulating, and saving gltf files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=['python-datauri>=0.2.8'],
    python_requires='>=3.6',
)