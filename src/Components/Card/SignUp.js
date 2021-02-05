import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import './SignUp-Style.css'
import AdminFooter from "../Footers/AdminFooter.js";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'


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
            <div id="main-content">
                <h1> Sign Up for Course Pilot </h1>
                <div className="row">
                    <div class="col"></div>
                    <Form id="signup-form" method="post" action="/api/signup" className="col-4">
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Email Address</Form.Label>
                            <Form.Control type="email" name="email" id="email-field" className="signup-form-field" placeholder="Enter Email"></Form.Control>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" name="password" id="password-field" className="signup-form-field" placeholder="Enter Password"></Form.Control>
                            <Form.Label>Confirm Password</Form.Label>
                            <Form.Control type="password" name="confirm-password" id="confirm-password-field" className="signup-form-field" placeholder="Confirm Password"></Form.Control>
                        </Form.Group>
                        <Form.Group controlId="exampleForm.ControlSelect2">
                            <Form.Label>Select Your Major(s) -- [CTRL + Click to Select Multiple]</Form.Label>
                            <Form.Control as="select" name="major" id="major" multiple>
                                {success.majors.map((value, index) => {
                                    return <option key={index} value={value}>{value}</option>
                                })}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="exampleForm.ControlSelect2">
                            <Form.Label>Select Your Minor(s) -- [CTRL + Click to Select Multiple]</Form.Label>
                            <Form.Control as="select" name="minor" id="minor" multiple>
                                {success.minors.map((value, index) => {
                                    return <option key={index} value={value}>{value}</option>
                                })}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Select Your Requirement Year</Form.Label>
                            <Form.Control as="select" name="requirement-year" id="requirement-year">
                                <option value="2020">2020</option>
                                <option value="2019">2019</option>
                                <option value="2018">2018</option>
                                <option value="2017">2017</option>
                            </Form.Control>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Select Your Graduation Year</Form.Label>
                            <Form.Control as="select" name="graduation-year" id="graduation-year">
                                <option value="2021">2021</option>
                                <option value="2022">2022</option>
                                <option value="2023">2023</option>
                                <option value="2024">2024</option>
                            </Form.Control>
                        </Form.Group>
                        <Button variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                            Create Account
                        </Button>
                    </Form>
                    <div class="col"></div>
                </div>
                {/*<form id="signup-form" method="post" action="/api/signup">
                    <input type="email" name="email" id="email-field" className="signup-form-field" placeholder="Enter Email"></input>
                    <input type="text" name="username" id="username-field" className="signup-form-field" placeholder="Enter Username"></input>
                    <input type="password" name="password" id="password-field" className="signup-form-field" placeholder="Enter Password"></input>
                    <input type="password" name="confirm-password" id="confirm-password-field" className="signup-form-field" placeholder="Confirm Password"></input>
                    <label for="major"> Select Your Major(s) </label>
                    <select name="major" id="major">
                        {success.majors.map((value, index) => {
                            return <option key={index} value={value}>{value}</option>
                        })}
                    </select>
                    <label for="minor"> Select Your Minor(s) </label>
                    <select name="minor" id="minor">
                        {success.minors.map((value, index) => {
                            return <option key={index} value={value}> {value} </option>
                        })}
                    </select>
                    <label for="requirement-year"> Select Your Requirement Year </label>
                    <select name="requirement-year" id="requirement-year">
                        <option value="2021">2021</option>
                        <option value="2020">2020</option>
                        <option value="2019">2019</option>
                        <option value="2018">2018</option>
                    </select>
                    <label for="graduation-year"> Select Your Graduation Year </label>
                    <select name="graduation-year" id="graduation-year">
                        <option value="2021">2021</option>
                        <option value="2022">2022</option>
                        <option value="2023">2023</option>
                        <option value="2024">2024</option>
                    </select>
                    <input type="submit" value="Create Account" id="login-form-submit" className="signup-form-field"></input>
                </form>*/}
                <p> Already have an account? Click <Link to="/">Here</Link> to login. </p>
            </div>
            <AdminFooter/>
        </div>
    );
}

export default SignUp