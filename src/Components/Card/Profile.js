import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'
import Select from 'react-select'


global.loggedOut = false;

function signOut() {
    if(global.loggedOut == false) {
        global.loggedOut = true;
        window.location = "/";
    }
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
 
    const handleMajorSubmit = (e) => {
        const parameters = {
             major: majorSelectedValue,
        }
        
        axios.post('/api/changeMajor', parameters).finally(response => {
            alert(response);
            setShowMajor(false);
            window.location = '/Profile';
        })
        .catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    const handleMinorSubmit = (e) => {
        const parameters = {
             minor: minorSelectedValue,
        }
        
        axios.post('/api/changeMinor', parameters).finally(response => {
            alert(response);
            setShowMinor(false);
            window.location = '/Profile';
        })
        .catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    const handlePasswordSubmit = (e) => {
        const parameters = {
            oldPassword: oldPasswordValue,
            newPassword: newPasswordValue,
        }

        console.log(parameters);

        var message = "";

        if(newPasswordValue.length < 8) {
            message = "Error: Password must be at least 8 characters";
        }

        else if(oldPasswordValue == newPasswordValue) {
            message = "Error: New Password and old password cannot be the same";
        }

        else if(!(/[a-z]/.test(newPasswordValue)) || !(/[A-Z]/.test(newPasswordValue)) || !(/[0-9]/.test(newPasswordValue))) {
            message = "Error: Password must be a combination of uppercase, lowecase, and special characters";
        }

        else if(!(/[@_!#$%^&*()<>?/\|}{~:]/.test(newPasswordValue))) {
            message = "Error: Password must contain special characters";
        }

        else if(success["passwrd"] != newPasswordValue) {
            message = "Error: Current password was incorrect";
        }

        if (message != "") {
            alert(message);
        }
        if(message == "") {
            axios.post('/api/changePassword', parameters).finally(response => {
                alert("Password Changed Successfully");
                setShowPassword(false);
            })
            .catch(err => {
                if (err.response) {
                console.log("BAD!");
                }
            })
        }
    }

    useEffect(() => {
        axios.get("/api/profile").then(response => {
            console.log(response.data["email"]);
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
        <div id="main-content">
            <Navbar bg="dark" variant="dark" expand="lg">
                <Navbar.Brand href="/home">Course Pilot</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="/home">Scheduling</Nav.Link>
                    <Nav.Link href="/degree">Degree Report</Nav.Link> 
                    <Nav.Link href="/majors">Majors and Minors</Nav.Link> 
                    <Nav.Link href="/profile">Profile</Nav.Link> 
                </Nav>
                </Navbar.Collapse>
            </Navbar>

        <div className="container">
            <div className="row">
                <div className="col">
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