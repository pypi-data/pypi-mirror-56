import setuptools

# with open("README.py.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="pysocketftp_eba", 
    version="0.0.1",
    author="Eba Alemayehu",
    author_email="ebaalemayhu3@gmail.com",
    description="Final projet to icog devtools course",
    long_description='''
        # iCog course development tools final project
        ## Socket file transfer program
        > Author: **Eba Alemayehu**
        ___
        ## Introduction 

        In general this parogram is used to transfer file form the client to the server by using socket. The program uses both C and python programming languages. The c programm makes the socket connection and the python program wrap the c shared liberary and use the methods defined in the library to transfer file to the server. 

        This paogram is packaged in wheele file and it is available in pip installer. 
    ''',
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