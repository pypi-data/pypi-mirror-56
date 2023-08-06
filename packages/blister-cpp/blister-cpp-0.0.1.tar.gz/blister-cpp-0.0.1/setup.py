import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blister-cpp", # Replace with your own username
    version="0.0.1",
    author="Eduardo Costa",
    author_email="m4c0@users.noreply.github.com",
    description="Conventions-over-configuration C++/modules project manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m4c0/blister",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
    ],
    install_requires=[
        "PyYAML>=5.1.2"
    ],
    scripts=[
        "bin/bli"
    ],
    python_requires='>=3.6',
)
