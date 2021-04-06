import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import '../static/styles/Login-Style.css'
import Logo from '../static/images/logo.jpg'
import Image from 'react-bootstrap/Image'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import axios from 'axios'


// HTML Content for the login page
export const Login = ()  => {

    const [email, setEmail] = useState();
    const [password, setPassword] = useState();

    // Event listener to get the user's email
    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    // Event listener to get the user's password
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }

    const handleSubmit = (e) => {
        const parameters = {
             email: email,
             password: password ,
        }
        var url = "/api/login?email=" + email;
        axios.post(url, parameters).then(response => {
            var response = response.data.text;
            console.log(response);
            if(response != "success") {
                alert(response);
            }
            else {
                window.location = "/Home?email=" + email;
            }
        })
        .catch(err => {
            if (err.response) {
                alert("Error: Make sure all fields have been completed");
            }
        })
    }

    return(
        <div id="login-content" className="container-fluid">
            <div>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0,"></meta>
                <title>Welcome to Course Pilot</title>
            </div>
            <div id="form-content" className="row-fluid">
                <div className="col-fluid">
                    <Form id="login-form">
                        <Image src={Logo} fluid id="logo"/>
                        <Form.Control onChange={handleEmailChange} type="email" name="email" id="email-field" className="login-form-field" placeholder="Enter Email"></Form.Control> 
                        <Form.Control onChange={handlePasswordChange} type="password" name="password" id="password-field" className="login-form-field" placeholder="Enter Password"></Form.Control>
                        <Button onClick={handleSubmit} variant="primary" id="login-form-submit" className="login-form-field">
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