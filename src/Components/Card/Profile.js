import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'
import Select from 'react-select'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'
import '../static/styles/Profile-Style.css'


global.loggedOut = false;
global.email = ""

function signOut() {
    axios.post("/api/logout?email=" + global.email).then(response => {
        if(response.data.text === "success") {
            window.location = "/"
        }
    })
}

export const Profile = () => {
    const [success, setSuccess] = useState();
    const [degreeInfo, setDegreeInfo] = useState();
    const [isLoading, setLoading] = useState(true);
    const [showMajor, setShowMajor] = useState(false);
    const [showMinor, setShowMinor] = useState(false);
    const isFirstRun = useRef(true);
    const [showPassword, setShowPassword] = useState(false);
    const [ready, setReady] = useState(false);
    const [minorSelectedValue, setMinorSelectedValue] = useState([]);
    const [majorSelectedValue, setMajorSelectedValue] = useState([]);
    const [newPasswordValue, setNewPasswordValue] = useState();
    const [confirmPasswordValue, setConfirmPasswordValue] = useState();
    const [oldPasswordValue, setOldPasswordValue] = useState();
    const [populate, setPopulate] = useState(false);
    const minorOptions = []
    const majorOptions = []

    const handleCloseMajor = () => setShowMajor(false);
    const handleShowMajor = () => setShowMajor(true);

    const handleCloseMinor = () => setShowMinor(false);
    const handleShowMinor = () => setShowMinor(true);

    const handleClosePassword = () => setShowPassword(false);
    const handleShowPassword = () => setShowPassword(true);

    const handleChange = (e) => {
        setMinorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }
    const handleMajorChange = (e) => {
        setMajorSelectedValue(Array.isArray(e) ? e.map(x => x.value) : []);
    }

    const handleNewPasswordChange = (e) => {
        setNewPasswordValue(e.target.value);
    }

    const handleOldPasswordChange = (e) => {
        setOldPasswordValue(e.target.value);
    }

    const handleConfirmPasswordChange = (e) => {
        setConfirmPasswordValue(e.target.value);
    }
 
    const handleMajorSubmit = (e) => {
        const parameters = {
             major: majorSelectedValue,
        }
        
        axios.post('/api/changeMajor?email=' + global.email, parameters).finally(response => {
            alert("Major Changed Successfully");
            setShowMajor(false);
            window.location = '/Profile?email=' + global.email;
        })
        .catch(err => {
            if (err.response) {
                alert("Whoops... looks like something went wrong there");
            }
        })
    }

    const handleMinorSubmit = (e) => {
        const parameters = {
             minor: minorSelectedValue,
        }
        
        axios.post('/api/changeMinor?email=' + global.email, parameters).finally(response => {
            alert("Minor Changed Successfully");
            setShowMinor(false);
            window.location = '/Profile?email=' + global.email;
        })
        .catch(err => {
            if (err.response) {
                alert("Whoops... looks like something went wrong");
            }
        })
    }

    const handlePasswordSubmit = (e) => {
        const parameters = {
            oldPassword: oldPasswordValue,
            newPassword: newPasswordValue,
        }

        var message = "";
        var cont = true;

        if(newPasswordValue.length < 8) {
            message = "Error: Password must be at least 8 characters";
            cont = false;
        }

        else if(oldPasswordValue === newPasswordValue) {
            message = "Error: New Password and old password cannot be the same";
            cont = false;
        }

        else if(!(/[a-z]/.test(newPasswordValue)) || !(/[A-Z]/.test(newPasswordValue)) || !(/[0-9]/.test(newPasswordValue))) {
            message = "Error: Password must be a combination of uppercase, lowecase, and special characters";
            cont = false;
        }

        else if(!(/[@_!#$%^&*()<>?/\|}{~:]/.test(newPasswordValue))) {
            message = "Error: Password must contain special characters";
            cont = false;
        }

        else if(success["passwrd"] !== oldPasswordValue) {
            message = "Error: Current password was incorrect";
            cont = false;
        }

        else if(newPasswordValue !== confirmPasswordValue) {
            message = "Error: New passwords must match"
            cont = false;
        }

        if (message !== "") {
            alert(message);
            cont = false;
            window.location = "/Profile?email=" + global.email
        }

        else if(cont) {
            console.log(cont);
            axios.post('/api/changePassword?email=' + global.email, parameters).finally(response => {
                if(response == "success") {
                    alert("Password Changed Successfully");
                    setShowPassword(false);
                    window.location = "/Profile?email=" + global.email
                }
                else {
                    alert("Password Changed Successfully")
                    setShowPassword(false);
                    window.location = "/Profile?email=" + global.email
                }
            })
            .catch(err => {
                if (err.response) {
                    alert("Password Changed Successfully")
                    window.location = "/Profile?email=" + global.email
                }
            })
        }
    }

    useEffect(() => {
        global.email = String(window.location).split("?")[1]
        global.email = String(global.email).split("=")[1];
        axios.get("/api/profile?email=" + global.email).then(response => {
            setSuccess(response.data);
            setReady(true);
        });
    }, []);

    if(isFirstRun.current){
        if(ready) {
            axios.get("/api/signup").then(response => {
                setDegreeInfo(response.data);
                setPopulate(true);
                setLoading(false);
                setReady(false);
            });
            success.majors.forEach(element => {
                majorSelectedValue.push(element);
            })
            success.minors.forEach(element => {
                minorSelectedValue.push(element);
            })
        }
    }

    if(isLoading) {
        return <div> Loading... </div>
    }

    if(populate) {
        degreeInfo.minors.forEach(element => minorOptions.push( {"value": element, "label": element} ))
        degreeInfo.majors.forEach(element => majorOptions.push( {"value": element, "label": element} ))
    }

    return (
        <div id="main-content-profile">
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                  <Nav.Link href={"/home?email=" + global.email}>Scheduling</Nav.Link>
                  <Nav.Link href={"/degree?email=" + global.email}>Degree Report</Nav.Link> 
                  <Nav.Link href={"/majors?email=" + global.email}>Majors and Minors</Nav.Link> 
                  <Nav.Link href={"/profile?email=" + global.email}>Profile</Nav.Link> 
              </Nav>
              </Navbar.Collapse>
            </Navbar>

        <div className="container">
            <div className="row">
                <div className="col">
                    <h1 id="profile-h1"> Hello,  {success.email} </h1>
                    <div id="user-data-div">
                        <h1 id="account-info"> Account Information </h1>
                        <h2 className="profile-h2"> Major(s): {success["majors"].join(", ")} </h2>
                        <h2 className="profile-h2"> Minor(s): {success["minors"].join(", ")} </h2>
                        <Button variant="primary" id="profile-button" onClick={handleShowPassword}> Change Password </Button>
                        <Button variant="primary" id="profile-button" onClick={handleShowMajor}> Change Major </Button>
                        <Button variant="primary" id="profile-button" onClick={handleShowMinor}> Change Minor </Button>
                    </div>
                            <Modal show={showPassword} onHide={handleClosePassword}>
                                <Modal.Header closeButton>
                                    <Modal.Title class="modal-title">Change Password</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <Form action="/api/changePassword" method="POST">
                                        <Form.Group>
                                        <Form.Label> Current Password </Form.Label>
                                            <Form.Control 
                                                onChange={handleOldPasswordChange} 
                                                type="password" 
                                                name="old-password" 
                                                id="password-field" 
                                                className="signup-form-field" 
                                                placeholder="Enter Old Password">
                                            </Form.Control>
                                            <Form.Label> New Password </Form.Label>
                                            <Form.Control 
                                                onChange={handleNewPasswordChange} 
                                                type="password" 
                                                name="new-password" 
                                                id="password-field" 
                                                className="signup-form-field" 
                                                placeholder="Enter New Password">
                                            </Form.Control>
                                            <Form.Label> Confirm New Password </Form.Label>
                                            <Form.Control 
                                                onChange={handleConfirmPasswordChange} 
                                                type="password" 
                                                name="confirm-password" 
                                                id="password-field" 
                                                className="signup-form-field" 
                                                placeholder="Confirm New Password">
                                            </Form.Control>
                                        </Form.Group>
                                        <Button variant="primary" id="change-button" type="submit" onClick={handlePasswordSubmit}> Confirm New Password </Button>
                                    </Form>
                                </Modal.Body>
                            </Modal>
                            <Modal show={showMajor} onHide={handleCloseMajor}>
                                <Modal.Header closeButton>
                                    <Modal.Title class="modal-title">Choose Major(s)</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <Form>
                                        <Form.Group>
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
                                    </Form>
                                    <Button variant="primary" id="change-button" type="submit" onClick={handleMajorSubmit}> Confirm Major(s) </Button>
                                </Modal.Body>
                            </Modal>
                            <Modal show={showMinor} onHide={handleCloseMinor}>
                                <Modal.Header closeButton>
                                    <Modal.Title class="modal-title">Choose Minor(s)</Modal.Title>
                                </Modal.Header>
                                <Modal.Body>
                                    <Form>
                                        <Form.Group>
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
                                    </Form>
                                    <Button variant="primary" id="change-button" type="submit" onClick={handleMinorSubmit}> Confirm Minor(s) </Button>
                                </Modal.Body>
                            </Modal>
                    <Button onClick={signOut} variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                        Log Out
                    </Button>
                </div>
            </div>
        </div>
        </div>
    );
}

export default Profile