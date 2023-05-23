# Repository Mining
## Table Of Content

Introduction

Prerequisites

Input

Output

How to Run The Program

## Introduction
Repository mining is the process of extracting imformation and knowledge from software repositories, mostly git , bitbucker.Repository mining imvolve alanalyzing and extracting data from these repositories to gain insights and desired information.

Some common repositories mining includes:

- Bug analysis and fixing

- Code Quality Assessment

- Collaboration analysis

## Prerequisites
 
- Python 3
- Pydriller
    - To install pi driller use this command 
    
  `Pip install pydriller==2.4.1`
  
-Javalang 

  - to install javalang use this command
  
    `pip install javalang==0.13.0`

## Input
To run this project, you will need to provide the path to the project and pass the required parameter(URL) using an input JSON file.

## output
Once the project execution is complete, the output will be displayed in a JSON file named "repositoryminingOutput."

## How to run the project
- Step One:

        window enviroment: Open the Command Prompt 

        MacOs and Ubuntu: Open the Terminal application. 

- Step Two:

    - Navigate to the directory where you want to create your   virtual environment. This can be any location on your system. Use the cd command to change directories.

            Example: cd /path/to/my/project

-   Step Three:

    - Create a virtual environment using the venv module. This module is available by default in Python 3.
    -  Run the following command to create a virtual environment  named "myenv":
        
        `python3 -m venv myenv`

- Step Four

    - Activate the virtual environment

             Window: source myenv/bin/activate

            Mac and Ubuntu: source myenv/bin/activate

- Step Five

    - Your terminal prompt should now indicate that you are working within the virtual environment. It typically looks like (myenv). You can now install any required Python packages using pip.


        `pip install Pydriller==2.4.1`
        
        `pip install javalang==0.13.0`

- Step six

    - Once you step up your virtual enviroment.clone the repository

    `git clone https://github.com/jenshwetakc/repository_mining`

- Step Seven

    - Change to the cloned repository directory:

        `cd repository_mining`

- Step Eight

    - At this point, you should see the Python program files within the cloned repository.
    - Pass the desired reposirtory url as an input to perform the repository mining in input.json. 
    - To do so change the value of “repo_url” key with desired repository for mining.


- Step Nine: Run the program 

    `python repository_mining.py`

- Step Ten

    - Check output in repositoryOutput.json

