import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

export const Majors = () => {

    const [isLoading, setLoading] = useState(true);
    const isFirstRun = useRef(true);
    const [success, setSuccess] = useState(null);
    const majorCourses = []

    useEffect(() => {
        axios.get("/api/MajorPage").then(response => {
            setSuccess(response.data);
            
            console.log(response.data)
        })
    }, []);

    //console.log(success.data)
    //success.major.foreach(element => majorCourses.push({"value": element, "label": element}))
    

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
        <div class="req-content">
            <div class="reqYear">
                Requirement Year
            </div>
            <div class="tab">
                <button>Majors</button>
                <button>Minors</button>
            </div>
            <div>
                
            </div>
        </div>
        
        </div>
    );
}


export default Majors

