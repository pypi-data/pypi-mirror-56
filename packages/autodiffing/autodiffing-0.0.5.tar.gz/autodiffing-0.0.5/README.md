# How to Use Package

## Installation

To begin, the user has to work in a `python` environment (preferably version >= 3.7). It is advisable for the user to create a new virtual environment for interacting with our package. To create a new virtual environment, enter the following command in the terminal:

`conda create -n env_autodiff python=3.7`

After which, activate the environment with the following command:

`conda activate env_autodiff`

Since we have used PyPI to host our package, users can download our Automatic Differentiation package with the following command in the terminal:

`pip install autodiffing`

As we have set up the pip package in a way such that the required dependencies will be installed during `pip install autodiffing`, users need not worry about not having the required dependencies when using the Automatic Differentiation package. 

In case users fail to get the required dependencies during pip install, users can still refer to the contents of requirements.txt below to pip install the main dependencies that are required. If not, users can visit https://pypi.org/project/autodiffing/#files to download the latest gunzip tar file and unzip the contents to get the requirements.txt file. In the directory with the unzipped folder containing the requirements.txt file, users need to run the following command in the terminal to download the required dependencies:

`pip install -r requirements.txt`

Within our requirements.txt, we have the a number of packages that come with the installation of `python` version 3.7 and our main packages, but the main packages that we require for our Automatic Differentiation package are: 

`numpy==1.17.4`\
`matplotlib==3.1.1`\
`scipy==1.3.2`

`numpy` is essential for our Automatic Differentiation package as we require it for the calculation of our elementary functions, and for dealing with arrays and matrices when there are vector functions and vector inputs.

`matplotlib` is needed for any potential visualization of our outputs.

`scipy` is a good package to have for its optimization and linear algebra abilities.

## Using the Package

Once users have installed all the dependencies and the package itself, they may begin to use our package to quickly find derivatives of functions.  For this section, we walk through three different examples of how users can interact with the package for their purposes.  Users should start by importing the DualNumber and ElementaryFunctions modules.  

```python
from AD.DualNumber import DualNumber
from AD import ElementaryFunctions as EF
```

As specified in Milestone 1 and in this document, users should start by initializing a DualNumber object:

```python
# DualNumber is a class in module AD, user must initialize the value of the variable in the initialization.
x = DualNumber(5)
```

Note that when the user initializes a variable, he or she _must_ provide the initial value.  For this milestone, the user may only pass in scalar-valued functions of scalars, but in the future we will implement methods and classes for the user to input vector-valued functions of vectors.  The initial value of the derivative is set as a default of 1, but the user may overwrite this. To find the derivative of a specific elementary function, users should pass this initialized object into our custom-designed elementary functions as follows:
```python
# ElemFunctions is a class where we define some elementary function derivatives and calculate the derivative function.
func = EF.Sin(x)

# we can get the value and derivative from the attributes "val" and "der". If we did not assign value and derivative direction in the fist
# step, we can do it here. 
print(func.val)
print(func.der)
```
