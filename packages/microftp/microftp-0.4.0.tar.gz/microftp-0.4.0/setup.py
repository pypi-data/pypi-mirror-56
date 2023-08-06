import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microftp",
    version="0.4.0",
    author="Vlatko Kosturjak",
    author_email="vlatko.kosturjak@gmail.com",
    description="Small FTP library client to handle broken servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kost/microftp-python",
    packages=setuptools.find_packages(),
    py_modules=['microftp'],
    install_requires=[],
    classifiers=[
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    scripts=['scripts/microftpcmd']
)

