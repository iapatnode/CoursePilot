import React from 'react';
import { Link } from 'react-router-dom';
import './Login-Style.css';

 
import AdminFooter from "../Footers/AdminFooter.js";

//import axios from 'axios'




class Login extends React.Component {

    /*generateRequest = function() {
        const url = "http://localhost:5000/"
        console.log("test")
        var email = document.getElementById("email-field");
        var password = document.getElementById("password-field");
        const comment = {
            "email": email, 
            "password": password
        };
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(comment);
        xhr.onreadystatechange = function() {
            if(this.readyState==4 && this.status==200) {
                console.log(xhr.status);
            }
        }
    }*/

    render() {
        return(
            <div id="main-content">
            <header>
                
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
                <title>Welcome to Course Pilot</title>
            </header>
                <div>
                    <main id="main-content">
                        <h1> Welcome to Course Pilot! </h1>
                        <form id="login-form" action="/api/login" method="POST">
                            <input type="email" name="email" id="email-field" className="login-form-field" placeholder="Email" onChange={this.onChange} />
                            <input type="password" name="password" id="password-field" className="login-form-field" placeholder="password" onChange={this.onChange} />
                            <input type="submit" value="login" id="login-form-submit"></input>
                        </form>
                        <p> Don't have an account? Sign up <Link to="/SignUp">Here</Link> </p>
                    </main>
                </div>
                <AdminFooter />
            </div>
        );
    }
}

export default Login;