import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './SignUp-Style.css'


export const SignUp = () => {
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();

    useEffect(() => {
        axios.get("/api/signup").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);
    
    if (isLoading) {
        return <div> Loading... </div>
    }
    return(
        <div id="main-content">
            <div>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
                <title>Welcome to Course Pilot</title>
            </div>
            <div>
                
                <div id="main-content">
                    <h1> Sign Up for Course Pilot </h1>
                    <form id="login-form" method="post" action="/api/signup">
                        <input type="email" name="email" id="email-field" className="signup-form-field" placeholder="Enter Email"></input>
                        <input type="text" name="username" id="username-field" className="signup-form-field" placeholder="Enter Username"></input>
                        <input type="password" name="password" id="password-field" className="signup-form-field" placeholder="Enter Password"></input>
                        <input type="password" name="confirm-password" id="confirm-password-field" className="signup-form-field" placeholder="Confirm Password"></input>
                        <p> Select Major </p>
                        <select name="major" id="major">
                            {success.majors.map((value, index) => {
                                return <option value={value}>{value}</option>
                            })}
                        </select>
                        <p> Select Minor (Optional) </p>
                        <select name="minor" id="minor">
                            {success.minors.map((value, index) => {
                                return <option value={value}> {value} </option>
                            })}
                        </select>
                        <p> Requirement Year </p>
                        <select name="requirement-year" id="requirement-year">
                            <option value="2021">2021</option>
                            <option value="2020">2020</option>
                            <option value="2019">2019</option>
                            <option value="2018">2018</option>
                        </select>
                        <p> Graduation Year </p>
                        <select name="graduation-year" id="graduation-year">
                            <option value="2021">2021</option>
                            <option value="2022">2022</option>
                            <option value="2023">2023</option>
                            <option value="2024">2024</option>
                        </select>
                        <input type="submit" value="Create Account" id="login-form-submit" className="signup-form-field"></input>
                    </form>
                    <p> Already have an account? Click <Link to="/">Here</Link> to login. </p>
                </div>
            </div>
        </div>
    );
}

export default SignUp