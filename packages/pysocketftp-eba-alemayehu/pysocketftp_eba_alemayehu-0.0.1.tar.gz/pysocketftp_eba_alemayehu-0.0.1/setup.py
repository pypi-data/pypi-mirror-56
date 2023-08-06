import setuptools

with open("README.py.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysocketftp_eba_alemayehu", 
    version="0.0.1",
    author="Eba Alemayehu",
    author_email="ebaalemayhu3@gmail.com",
    description="Final projet to icog devtools course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.icog-labs.com/eba-alemayehu/Final-project",
    packages=["pysocketftp"],
    package_dir={'pysocketftp': 'pysocketftp'},
    package_data = {'pysocketftp': ['socket_ftp_c/build/*.so']},
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.0',
    include_package_data=True,
    zip_safe=False 
)