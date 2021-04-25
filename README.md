# Course Pilot

# Contents
- [Course Pilot](#course-pilot)
- [Contents](#contents)
- [Set Up](#set-up)
- [Downloading Course Pilot](#downloading-course-pilot)
- [Running Course Pilot](#running-course-pilot)

# Set Up

The following must be installed:

## Node.js

Navigate to [Node.js](https://nodejs.org/en/download/) and download the Windows Installer version. Follow the prompts for installing Node.js. Do not select the checkbox for installing the necessary tools and Chocolately.

## Yarn

Using the command line, run the following commands:

#### `npm install -g yarn`

#### `yarn set version latest`

You can check the installed version of yarn using 

#### `yarn --version`

The installed version should be 1.22.10.

## Python

Navigate to [Python](https://www.python.org/downloads/release/python-385/) and select the Windows x86-64 executable installer. Follow the prompts for installation

You can check the installed version of python using 

#### `python --version`

The installed version should be Python 3.8.5.

## Flask

Using the command line, run the following command

#### `pip install flask`

Note: it may tell you to update pip. You can do this by running the command provided in the warning.

You also need to install several libraries. Using the command line, run 

#### `pip install flask_cors`


## Python Libraries

Using the command line, run the following commands to install the necessary libraries

#### `pip install python-dotenv`

## MySQL

<!-- Navigate to [MySQL](https://dev.mysql.com/downloads/installer/) and download the second installer. Follow the prompts for installing the necessary bundles and setting up a local server. You do not have to install Visual Studio. Simply, click next and continue with the installation.

Note: do not change anything from the default options.

Using the command line, run the following command to install the python connector -->

#### `pip install mysql-connector-python`

# Downloading Course Pilot

Download the CoursePilot.zip and unzip it in the folder you want to open the project. 

To make sure all dependencies for the project are installed, navigate to the project directory using the command line and run

#### `npm install`

# Running Course Pilot
To run the application, open a terminal and run the following command

#### `yarn start`

A browser window should open with the application from React loaded from http://localhost:3000.

Once the above browser window is running, open a second terminal and run the following command

#### `yarn start-api`

This starts the backend (flask server) running.

You may need to start the backend running before the front end.

# Deployment

You can access our deployment branch ar
#### http://coursepilot.gcc.edu:3000/
