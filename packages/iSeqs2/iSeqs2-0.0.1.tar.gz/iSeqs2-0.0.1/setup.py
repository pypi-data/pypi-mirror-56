import setuptools


#scripts=['change_set_subfield'] ,

setuptools.setup(
     name='iSeqs2',  
     version='0.0.1',
     author="Alessandro Coppe",
     author_email="",
     description="Another bunch of scripts I use in my Next Generation Sequencing Bioinformatics Analyses",
     url="https://github.com",
     packages=["iseqs2"],
     scripts=["scripts/build_leukemia_genes_list.py"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
