import React, { useState, useEffect, useRef } from 'react'
import { Link, Redirect } from 'react-router-dom'
import axios from 'axios'
import '../static/styles/SignUp-Style.css'
import AdminFooter from "../Footers/AdminFooter.js";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'
import Logo from '../static/images/logo.jpg'
import Image from 'react-bootstrap/Image'


export const SignUp = () => {
    const [isLoading, setLoading] = useState(true); // Variable to determine whether or not the page is loading
    const [success, setSuccess] = useState(); // Store data to render on the page gotten from the server
    const [email, setEmail] = useState(); // State variable that holds the user email
    const [password, setPassword] = useState(); // State variable to hold user password
    const [confirm, setConfirm] = useState(); // State variable to hold user's confirmed password
    const [minorSelectedValue, setMinorSelectedValue] = useState([]); // Which minors the user has selected
    const [majorSelectedValue, setMajorSelectedValue] = useState([]); // Which major the user selected
    const [requirement, setRequirement] = useState("2017"); // Which requirement year the user has selected
    const [graduation, setGraduation] = useState("2021"); // User graduation year. 
    const isFirstRun = useRef(true); // Keep track of whether or not this is the first time the page has loaded
    const minorOptions = [] // List of all minor options
    const majorOptions = [] // List of all major options

    /*
    If this is the first time the page has been loaded, set the success variable to contain
    all of the major and minor options that were sent from the server. Set the loading 
    variable to false so we can display the signup page to the user. 
    */
    useEffect(() => {
        if(isFirstRun.current) {
            axios.get("/api/signup").then(response => {
                setSuccess(response.data);
                setLoading(false);
                console.log(response);
            });
        }
    }, []);

    // Event listener to get the user's email
    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    // Event listener to get the user's password
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }

    // Event listener to get user's confirmed password
    const handleConfirmChange = (e) => {
        setConfirm(e.target.value);
    }

    // Get the minors that the user has selected
    const handleChange = (e) => {
        setMinorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }

    // Get the majors that the user has selected
    const handleMajorChange = (e) => {
        setMajorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }

    // Get the user's requirement year
    const handleRequirementChange = (e) => {
        setRequirement(e.target.value);
    }

    // Get the user's graduation year
    const handleGraduationChange = (e) => {
        setGraduation(e.target.value);
    }

    /*
    When the user clicks signup, send all of the user information to the backend 
    server in a post request to create the account and reroute the user accordingly
    */
    const handleSubmit = (e) => {
        const parameters = {
             email: email,
             password: password ,
             confirm_password: confirm,
             major: majorSelectedValue,
             minor: minorSelectedValue,
             requirement_year: requirement,
             graduation_year: graduation 
        }
        
        axios.post('/api/signup', parameters).finally(response => {
            alert("Account Creation Successful!");
            window.location = '/Home';
        })
        .catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }
    
    // Determine whether or not the page is loading
    if (isLoading) {
        return <div> Loading... </div>
    }

    // Set major and minor arrays accordingly to contain the results of the get request. 
    success.minors.forEach(element => minorOptions.push( {"value": element, "label": element} ))
    success.majors.forEach(element => majorOptions.push( {"value": element, "label": element} ))

    // HTML content for the signup page. 
    return(
        <div id="signup-content">
            <div>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
                <title>Welcome to Course Pilot</title>
            </div>    
            <div id="signup-form-container">
                <div className="container">
                    <div className="row">
                        <div className="col"></div>
                        <div className="col-md-6 col-fluid" id="form-material-signup">
                            <Form id="signup-form">
                                <Form.Group>
                                    <Form.Label>Email Address</Form.Label>
                                    <Form.Control onChange={handleEmailChange} type="email" name="email" id="email-field" className="signup-form-field" placeholder="Enter Email"></Form.Control>
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control onChange={handlePasswordChange} type="password" name="password" id="password-field" className="signup-form-field" placeholder="Enter Password"></Form.Control>
                                    <Form.Label>Confirm Password</Form.Label>
                                    <Form.Control onChange={handleConfirmChange} type="password" name="confirm-password" id="confirm-password-field" className="signup-form-field" placeholder="Confirm Password"></Form.Control>
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label className="signup-form-field">Select Your Major(s)</Form.Label>
                                    <Select 
                                            placeholder="Select Your Major(s)"
                                            value={majorOptions.filter(obj => majorSelectedValue.includes(obj.value))}
                                            onChange={handleMajorChange}
                                            options={majorOptions} 
                                            isMulti
                                            isClearable
                                            className="signup-form-field"
                                            name="major"
                                            id="major"
                                        />
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label className="signup-form-field">Select Your Minor(s)</Form.Label>
                                        <Select 
                                            placeholder="Select Your Minor(s)"
                                            value={minorOptions.filter(obj => minorSelectedValue.includes(obj.value))}
                                            onChange={handleChange}
                                            options={minorOptions} 
                                            isMulti
                                            isClearable
                                            className="signup-form-field"
                                            name="minor"
                                            id="minor"
                                        />
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label className="signup-form-field">Select Your Requirement Year</Form.Label>
                                    <Form.Control onChange={handleRequirementChange} as="select" name="requirement-year" id="requirement-year" className="signup-form-field">
                                        <option value="2020">2020</option>
                                        <option value="2019">2019</option>
                                        <option value="2018">2018</option>
                                        <option value="2017">2017</option>
                                    </Form.Control>
                                </Form.Group>
                                <Form.Group>
                                    <Form.Label className="signup-form-field">Select Your Graduation Year</Form.Label>
                                    <Form.Control onChange={handleGraduationChange} as="select" name="graduation-year" id="graduation-year" className="signup-form-field">
                                        <option value="2021">2021</option>
                                        <option value="2022">2022</option>
                                        <option value="2023">2023</option>
                                        <option value="2024">2024</option>
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </div>
                        <div className="col"></div>
                    </div>
                    <Button onClick={handleSubmit} variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                                    Create Account
                    </Button>
                </div>
            </div>
        </div>
    );
}

export default SignUp