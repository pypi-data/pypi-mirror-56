import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="check_express",                            
    version="0.0.1",                                  
    author="sunqiang",                                 
    author_email="530631372@qq.com",                    
    description="check express by express_id",            
    long_description=long_description,                     
    long_description_content_type="text/markdown",          
    url="http://106.12.107.253/",                            
    packages=setuptools.find_packages(),                    
    classifiers=[                                   
        "Programming Language :: Python :: 3",    
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",   
    ],
)

