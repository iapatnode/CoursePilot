import React from 'react'
import { Route, Link } from 'react-router-dom'
import './Login-Style.css'
import logo from './logo.jpg'

function Login() {
    return(
        <div id="main-content">
            <head>
            <meta charset="UTF-8"></meta>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
            <title>Welcome to Course Pilot</title>
        </head>
            <body>
                <main id="main-content">
                    <img src={require ('./logo.jpg')}></img>
                    <h1> Welcome to Course Pilot! </h1>
                    <form id="login-form" action="/" method="POST">
                        <input type="email" name="email" id="email-field" className="login-form-field" placeholder="Email"></input>
                        <input type="password" name="password" id="password-field" className="login-form-field" placeholder="password"></input>
                        <input type="submit" value="login" id="login-form-submit"></input>
                    </form>
                    <p> Don't have an account? Sign up <Link to="/SignUp">Here</Link> </p>
                </main>
            </body>
        </div>
    )
}

export default Login;