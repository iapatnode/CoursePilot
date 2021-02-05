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

You also need to install the flask_cors library and a native modal library. Using the command line, run 

#### `pip install flask_cors`

#### `npm install react-boostrap bootstrap`

## Python Libraries

Using the command line, run the following commands to install the necessary libraries

#### `pip install python-dotenv`

## MySQL

Navigate to [MySQL](https://dev.mysql.com/downloads/installer/) and download the second installer. Follow the prompts for installing the necessary bundles and setting up a local server. You do not have to install Visual Studio. Simply, click next and continue with the installation.

Note: do not change anything from the default options.

Using the command line, run the following command to install the python connector

#### `pip install mysql-connector-python`

In the config.json file, change the username and password to match the credentials for your local server.

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

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
