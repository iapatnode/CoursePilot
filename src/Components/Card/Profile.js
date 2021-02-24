import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'


global.loggedOut = false;

function signOut() {
    if(global.loggedOut == false) {
        global.loggedOut = true;
        window.location = "/";
    }
}

export const Profile = () => {
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