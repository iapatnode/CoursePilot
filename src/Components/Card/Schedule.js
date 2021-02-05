import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import SchedulePage from '../../Pages/SchedulePage'

export const Schedule = () => {
    return(
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
        <div>
            <h1>Test</h1>
        </div>
    </div>
    );
}

export default Schedule