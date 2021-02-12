import React, { useState, useEffect } from 'react'
import { Link, Redirect } from 'react-router-dom'
import axios from 'axios'
import '../static/styles/SignUp-Style.css'
import AdminFooter from "../Footers/AdminFooter.js";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'


export const SignUp = () => {
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();
    const [confirm, setConfirm] = useState();
    const [minorSelectedValue, setMinorSelectedValue] = useState([]);
    const [majorSelectedValue, setMajorSelectedValue] = useState([]);
    const [requirement, setRequirement] = useState("2020");
    const [graduation, setGraduation] = useState("2021");
    const minorOptions = []
    const majorOptions = []

    const handleEmailChange = (e) => {
        setEmail(e.target.value)
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }

    const handleConfirmChange = (e) => {
        setConfirm(e.target.value);
    }

    const handleChange = (e) => {
        setMinorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }

    const handleMajorChange = (e) => {
        setMajorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }

    const handleRequirementChange = (e) => {
        setRequirement(e.target.value);
    }

    const handleGraduationChange = (e) => {
        setGraduation(e.target.value);
    }

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
        
        axios.post('/api/signup', parameters).then(response => {
            alert("Account Creation Successful!")
            window.location = '/Home'
        })
        .catch((error) => {
            if (error.status === 400) {
                alert("Error")
                window.location = '/Signup'
            }
            else {
                window.location = '/Home'
            }
        })
    }

    useEffect(() => {
        axios.get("/api/signup").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);
    
    if (isLoading) {
        return <div> Loading... </div>
    }

    success.minors.forEach(element => minorOptions.push( {"value": element, "label": element} ))
    success.majors.forEach(element => majorOptions.push( {"value": element, "label": element} ))

    return(
        <div id="main-content">
            <div>
                <meta charSet="UTF-8"></meta>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
                <title>Welcome to Course Pilot</title>
            </div>    
            <div id="main-content">
                <h1> Sign Up for Course Pilot </h1>
                <div className="container">
                    <div className="row">
                        <div className="col-md-4 col-md-offset-4"></div>
                        <Form id="signup-form" onSubmit={handleSubmit}>
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
                                <Form.Label className="signup-form-field">Select Your Major(s) -- [CTRL + Click to Select Multiple]</Form.Label>
                                <Select 
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
                                <Form.Label className="signup-form-field">Select Your Minor(s) -- [CTRL + Click to Select Multiple]</Form.Label>
                                    <Select 
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
                            <Button onClick={handleSubmit} variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                                Create Account
                            </Button>
                        </Form>
                        <div className="col"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SignUp