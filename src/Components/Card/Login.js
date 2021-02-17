import React from 'react';
import { Link } from 'react-router-dom';
import '../static/styles/Login-Style.css'
import Logo from '../static/images/logo.jpg'
import Image from 'react-bootstrap/Image'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'


export const Login = ()  => {
    return(
        <div id="login-content" className="container-fluid">
            <div>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0,"></meta>
                <title>Welcome to Course Pilot</title>
            </div>
            <div id="form-content" className="row-fluid">
                <div className="col-fluid">
                    <Form id="login-form" action="/api/login" method="POST">
                        <Image src={Logo} fluid id="logo"/>
                        <Form.Control type="email" name="email" id="email-field" className="login-form-field" placeholder="Enter Email"></Form.Control> 
                        <Form.Control type="password" name="password" id="password-field" className="login-form-field" placeholder="Enter Password"></Form.Control>
                        <Button variant="primary" type="submit" id="login-form-submit" className="login-form-field">
                                Sign In
                        </Button>
                        <p id="sign-up-link">Don't have an account? Sign up <Link to="/SignUp">Here</Link></p>
                    </Form>
                </div>
            </div>
        </div>
    );    
}

export default Login;