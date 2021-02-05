import React from 'react';
import { Link } from 'react-router-dom';
import './Login-Style.css';
import AdminFooter from "../Footers/AdminFooter.js";
import Logo from '../../CoursePilotLogo.jpg'
import Image from 'react-bootstrap/Image'


export const Login = ()  => {
    return(
        <div id="main-content">
            <header>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
                <title>Welcome to Course Pilot</title>
            </header>
            <div>
                <main id="main-content">
                    <Image src={Logo} fluid/>
                    <h1> Welcome to Course Pilot! </h1>
                    <form id="login-form" action="/api/login" method="POST">
                        <input type="email" name="email" id="email-field" className="login-form-field" placeholder="Email"/>
                        <input type="password" name="password" id="password-field" className="login-form-field" placeholder="Password"/>
                        <input type="submit" value="login" id="login-form-submit"></input>
                    </form>
                    <p> Don't have an account? Sign up <Link to="/SignUp">Here</Link> </p>
                </main>
            </div>
            <AdminFooter />
        </div>
    );    
}

export default Login;