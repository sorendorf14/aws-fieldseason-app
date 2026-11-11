# aws-fieldseason-app

This tutorial was set up for unix/MacOS. There are separate sections for Windows OS. 

# MacOS/Unix Tutorial

## Using Conda 

### Setting up virtual environment and installing required dependencies using a file

To create a virtual environment using a dependency file (e.g., `requirements.txt` or `.yaml`), make sure you are in the directory with the file. Then, create the environment using the following commands:

`conda create --file idl.yaml --name myenv`
OR
`conda create --file requirements.txt --name myenv`

If you edited the filename included in the installation package, replace _.yaml_ or _requirements.txt_ with the updated filename. 

### Manually setting up virtual environment and installing required dependencies
We are going to create a virtual environment, which is an isolated setup of python for a specific project. This way it will not mess up the python version and packages that you may have installed for other projects that could cause issues.

`conda create --name myenv python==3.x` 

where `myenv` is the name you choose for your virtual environment and `x` is the python version you wish to use. The python version can be any version >= 3.8.

To install the required dependencies, first activate your virtual environment. 

`conda activate myenv`

Once activated, install the required packages:
```
conda install numpy
conda install pandas
conda install plotly
conda install dash
conda install scipy
```
More information about setting up virtual environments and installing packages using conda:
* Setting up and activating virtual environment
* [Installing packages using conda](https://www.anaconda.com/docs/getting-started/working-with-conda/packages/install-packages)

If you are having issues with installing plotly and/or dash:
* Installation help for [dash](https://dash.plotly.com/installation)
* Installation help for [plotly](https://plotly.com/python/getting-started)

## Using pip 
### Manually setting up virtual environment and installing required dependencies
**If you used conda to set up a virtual environment successfully, you do not need to follow the following instructions.** 

```
python -m venv myenv
```
Where the `x` is the python version you wish to install and `myenv` is the name you want to select for the virtual environment. **NOTE: Dash requires Python v3.8 or later**

Activate the environment so you can install packages. 

`source myenv/bin/activate`

Install the required packages.

```
pip install pandas
pip install numpy
pip install scipy
pip install plotly
pip install dash
pip install --upgrade kaleido
```

When you are no longer using the virtual environment (you need it to run the code!), deactivate the virtual environment.

`deactivate`

More information about setting up [virtual environments](https://www.w3schools.com/python/python_virtualenv.asp) and [installing packages using pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
* Installation help for [plotly](https://plotly.com/python/getting-started/)
* Installation help for [dash](https://dash.plotly.com/installation) 

***
***
***
***
***

# Windows OS

## Using Conda in Anaconda PowerShell Prompt
### Setting up virtual environment and installing required dependencies using `requirements.txt` or `idl.yaml`
Open a command line interface. To create a virtual environment using a dependency file (e.g., requirements.txt or idl.yaml), make sure you are in the directory with the file. Then, create the environment using the following commands:

`conda create --file idl.yaml --name myenv`
or
`conda create --file requirements.txt --name myenv`

If you edited the filename included in the installation package, replace _idl.yaml_ or _requirements.txt_ with the updated filename. 

### Manually setting up virtual environment and installing required dependencies
We are going to create a virtual environment, which is an isolated setup of python for a specific project. This way it will not mess up the python version and packages that you may have installed for other projects that could cause issues.

`conda create --name myenv python==3.9` 

where `myenv` is the name you choose for your virtual environment. The python version can be any version >= 3.8.
To install the required dependencies, first activate your virtual environment. 
`conda activate myenv`

Once activated, install the require dependencies.
```
conda install numpy
conda install pandas
conda install plotly
conda install dash
conda install scipy
```
If you are having issues with installing plotly and/or dash:
* Installation help for [dash](https://dash.plotly.com/installation)
* Installation help for [plotly](https://plotly.com/python/getting-started)

More information about setting up virtual environments and installing packages using conda:
* Setting up and activating virtual environment
* [Installing packages using conda](https://www.anaconda.com/docs/getting-started/working-with-conda/packages/install-packages)

## Using pip 
### Manually setting up virtual environment and installing required dependencies
If you used conda to set up a virtual environment successfully, you do not need to follow the following instructions. 
```
python -m venv myenv
```
Where the `myenv` is the name you assign to the virtual environment. **NOTE: Dash requires Python v3.8 or later**

Activate the environment so you can install packages. 
```
myenv\Scripts\activate
```
Install the required packages.
py -m pip install requests
```
pip install pandas
pip install numpy
pip install scipy
pip install plotly
pip install dash
pip install --upgrade kaleido
```

When you are no longer using the virtual environment (you need it to run the code!), deactivate the virtual environment.

`deactivate`

More information about setting up [virtual environments](https://www.w3schools.com/python/python_virtualenv.asp) and [installing packages using pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
* Installation help for [plotly](https://plotly.com/python/getting-started/)
* Installation help for [dash](https://dash.plotly.com/installation) 
