import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as rt:
    install_reqs = rt.read().splitlines() 


setuptools.setup(
    name="autodiffing",
    version="0.0.5",
    
    install_requires=install_reqs,
    
    author="Shuvom, Sijie, Silin, Edwin",
    author_email="ssadhuka@college.harvard.edu, sijiesun@g.harvard.edu, szou@g.harvard.edu, chng_weimingedwin@g.harvard.edu",
    description="A package for Automatic Differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoDiffingFall2019/cs207-FinalProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
