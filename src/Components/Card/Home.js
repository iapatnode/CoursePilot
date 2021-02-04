import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'

export const Home = ()=> {
    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    useEffect(() => {
        axios.get("/api/home").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);
    
    if (isLoading) {
        return <div> Loading... </div>
    }

    return(
        <div id="main-content">
            <Navbar bg="dark" variant="dark" expand="lg">
            <Navbar.Brand href="/home">Course Pilot</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
                <Nav.Link href="/home">Scheduling</Nav.Link>
                {/* <Nav.Link href="/degree">Degree Report</Nav.Link> */}
                {/* <Nav.Link href="/majors">Majors and Minors</Nav.Link> */}
                {/* <Nav.Link href="/profile">Profile</Nav.Link> */}
            </Nav>
        </Navbar.Collapse>
        </Navbar>
            <h1> Schedules </h1>
            <div id="schedule-list-view">
                <h2> Name </h2>
                <p> Put the name of all of the user's schedules here </p>
                <h2> Date Modified </h2> 
                <p> Put the date of last modification to the schedule here </p>
            </div>
            <div id="button-container">
                {/* <button type="button" id="auto-generate"> Auto-Generate Schedule </button> */}
                <button variant="primary" onClick={handleShow}> Create New Schedule </button>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Modal heading</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Woohoo, you're reading this text in a modal!</Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}> Close </Button>
                        <Button variant="primary" onClick={handleClose}> Save Changes </Button>
                    </Modal.Footer>
                </Modal>
                {/* <button type="button" id="compare-schedule"> Compare Schedules </button> */}
            </div>
        </div>     
    );
}

export default Home