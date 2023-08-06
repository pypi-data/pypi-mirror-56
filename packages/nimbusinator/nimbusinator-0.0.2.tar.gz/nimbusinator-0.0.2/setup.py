import setuptools

with open('readme.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="nimbusinator",
    version="0.0.2",
    author="Tim Adams",
    author_email="adamstimb@gmail.com",
    description="RM Nimbus GUI for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamstimb/nimbusinator",
    packages=setuptools.find_packages(),
    package_data={'nimbusinator': ['data/*']},
    install_requires=[
        "opencv-python",
        "numpy",
        "simpleaudio",
        "pynput",
        "psutil"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)