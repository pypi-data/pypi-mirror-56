import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sogoqa",                            
    version="0.2.0",                                  
    author="sunqiang",                                 
    author_email="530631372@qq.com",                    
    description="QA by sogo engine",            
    long_description=long_description,                     
    long_description_content_type="text/markdown",          
    url="https://github.com/sunqiang25/sogouQA",                            
    packages=setuptools.find_packages(),                    
    classifiers=[                                   
        "Programming Language :: Python :: 3",    
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",   
    ],
)

