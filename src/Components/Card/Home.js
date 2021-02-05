import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'

export const Home = ()=> {
    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);
    const [showSemester, setShowSemester] = useState(false)

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleSubmit = () => {
        if(document.getElementById("schedule-name").value == "") {
            setShow(true);
        }
        else {
            setShow(false);
            setShowSemester(true);
        }
    }
    const handleSemesterClose = () => setShowSemester(false);

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
                <Nav.Link href="/degree">Degree Report</Nav.Link> 
                <Nav.Link href="/majors">Majors and Minors</Nav.Link> 
                <Nav.Link href="/profile">Profile</Nav.Link> 
            </Nav>
            </Navbar.Collapse>
            </Navbar>
            <h1> Schedules </h1>
            <div id="schedule-list-view">
                <div className="row">
                    <div className="col-2"></div>
                    <div className="col-md-4" id="names">
                        <h2> Name </h2>
                        <p> Put the name of all of the user's schedules here </p>
                    </div>
                    <div className="col-md-4" id="dates">
                        <h2> Date Modified </h2> 
                        <p> Put the date of last modification to the schedule here </p>
                    </div>
                    <div className="col-2"></div>
                </div>
            </div>
            <div id="button-container">
                {/* <button type="button" id="auto-generate"> Auto-Generate Schedule </button> */}
                <button variant="primary" onClick={handleShow}> Create New Schedule </button>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Create New Schedule - Enter Name</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group controlId="schedule-name-form">
                            <Form.Control type="text" placeholder="Enter Schedule Name" id="schedule-name" name="schedule-name"></Form.Control>
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}> Cancel </Button>
                        <Button variant="primary" onClick={handleSubmit}> Continue </Button>
                    </Modal.Footer>
                </Modal>
                <Modal show={showSemester} onHide={handleSemesterClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Create New Schedule - Select Semester</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <p> semester drop down will eventually go here</p>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleSemesterClose}> Cancel </Button>
                        <Button variant="primary" onClick={handleSemesterClose}> Create Schedule </Button>
                    </Modal.Footer>
                </Modal>

                {/* <button type="button" id="compare-schedule"> Compare Schedules </button> */}
            </div>
        </div>     
    );
}

export default Home