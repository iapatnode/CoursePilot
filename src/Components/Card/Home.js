import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import '../static/styles/Home-Style.css'
import Link from 'react-router-dom/Link'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'


global.semester=""; // Global variable for which semester the user has chosen


/*
Functional component for the home page, where the user can see and create new schedules
*/
export const Home = ()=> {
    const [isLoading, setLoading] = useState(true); // Determine whether or not the page is loading
    const [success, setSuccess] = useState(); // State variable used to store response of initial get request
    const [show, setShow] = useState(false); // Variable to determine whether or not to show modal to create new schedule
    const [showAuto, setShowAuto] = useState(false);
    const [redirect, setRedirect] = useState(false);
    const [compare, setCompare] = useState(false); // Variable to determine whether or not to show compare modal
    const [scheduleName, setScheduleName] = useState();
    const [scheduleSemester, setScheduleSemester] = useState();

    const handleScheduleName = (e) => {
        setScheduleName(e.target.value);
    }

    const handleScheduleSemester = (e) => {
        setScheduleSemester(e.target.value);
    }

    /*
    The below functions are used to open and close the new schedule modal. Used as 
    click listeners in the html code below  
    */
    const handleClose = () => setShow(false);
    const handleAuto = () => setShowAuto(true);
    const handleShow = () => setShow(true);
    const handleCompare = () => setCompare(true);
    const handleCloseCompare = () => setCompare(false);
    const handleCloseAuto = () => setShowAuto(false);


    /*
    makePostRequest() --> Method used to send a post request with the given parameters
    to the provided url. Catches an error if there are invalid parameters or invalid
    url provided
    */
    function makePostRequest(path, params) {
        return new Promise(function (resolve, reject) {
            axios.post(path, params).then(
                (response) => {
                    var result = response.data;
                    console.log('Processing request');
                    resolve(result)
                },
                    (error) => {
                        reject(error)
                    }
            );
        });
    }

    /*
    Function that uses the makePostRequest method above to send a request to the 
    below URL when the user selects to view an existing schedule. Will result
    in the user being redirected to the schedule page where the can view the 
    schedule they selected. 
    */
    async function clickListener(e) {
        console.log(e.target.innerText);
        let params = {
            "name": e.target.innerText
        }
        var result = await makePostRequest('/api/existingSchedule', params);
        if(result == "good") {
            window.location = "/Schedule";
        }
    }

    function createSchedule() {
        console.log(scheduleName);
        var makeRequest = true;
        success.forEach(element => {
            if(scheduleName == element["scheduleName"]) {
                alert("Error: You cannot add two schedules with the same name");
                makeRequest = false;
            }
        });
        if(makeRequest) {
            var semester = ""
            if(scheduleSemester === undefined) {
                console.log("hm");
                semester = "fall"
            }
            else {
                semester = "spring";
            }
            console.log(semester);
            const parameters = {
                "schedule-name": scheduleName,
                "schedule-semester": semester
           }
           axios.post('/api/home', parameters).then(response => {
            window.location = "/Schedule"
        })
        .catch(err => {
            if (err.response) {
                alert("Error: There was a problem with creating your schedule");
                window.location = "/Home";
            }
        })
        }
    }

    /*
    useEffect() --> Run when the page first loads. Gets necessary information (user schedule info).
    Stores the result of the get request in the success variable, and sets loading to false. 
    */
    useEffect(() => {
        console.log("URL: " + window.location);
        var url_array = String(window.location).split("=")
        var email = url_array[1];
        console.log(email);
        axios.get("/api/home?email=" + email).then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);

    // If the get request hasn't completed, display a loading page to the user. 
    if (isLoading) {
        return <div> Loading... </div>
    }

    // HTML content of the home page. 
    return(
        <div id="main-content">
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
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
            <div className="container-fluid" id="home-header">
                <h1 id="home-header"> Schedules </h1>
            </div>
            <div className="container" id="schedule-list-view">
                <div className="row">
                    <div className="col-md-4" id="names">
                        <h2 id="name-header"> Name </h2>
                        <ul>
                            {success.map((value, index) => {
                                return <li id="schedule-name" onClick={clickListener} key={index} value={value["scheduleName"]}>{value["scheduleName"]}<br></br></li>
                            })}
                        </ul>
                    </div>
                    <div className="col-md-4" id="semesters">
                        <h2 id="semester-header"> Semester </h2>
                        <ul>
                            {success.map((value, index) => {
                                return <li id="schedule-semester" key={index} value={value["scheduleSemester"]}>{value["scheduleSemester"]}<br></br></li>
                            })}
                        </ul>
                    </div>
                    <div className="col-md-4" id="dates">
                        <h2 id="date-header"> Date Modified </h2> 
                        <ul>
                            {success.map((value, index) => {
                                return <li id="schedule-date" key={index} value={value["dateModified"]}>{value["dateModified"]}</li>
                            })}
                        </ul>
                    </div>
                </div>
            </div>
            <div id="button-container-home">
                <Button variant="primary" id="home-page-secondary-button" onClick={handleAuto}> Auto Gen Schedule </Button>
                    <Modal show={showAuto} onHide={handleCloseAuto}>
                        <Modal.Header closeButton>
                            <Modal.Title>Auto-Generate Schedule</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <Form method="post" action="/api/autoGenerate">
                                <Form.Group>
                                    <Form.Control type="text" placeholder="Enter Schedule Name" id="auto-schedule-name" name="schedule-name"></Form.Control>
                                    <Form.Control as="select" id="schedule-semester" name="schedule-semester">
                                        <option value="fall">Fall</option>
                                        <option value="spring">Spring</option>
                                    </Form.Control>
                                    <Button variant="secondary" onClick={handleCloseAuto}>
                                        Cancel
                                    </Button>
                                    <Button variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                                        Auto Gen
                                    </Button>
                                </Form.Group>
                            </Form>
                        </Modal.Body>
                    </Modal>
                <Button variant="primary" id="home-page-secondary-button" onClick={handleShow}> Create New Schedule </Button>
                <Button variant="primary" id="home-page-secondary-button" onClick={handleCompare}> Compare Two Schedules </Button>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Create New Schedule - Enter Name</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group>
                                <Form.Control onChange={handleScheduleName} type="text" placeholder="Enter Schedule Name" id="enter-schedule-name" name="schedule-name"></Form.Control>
                                <Form.Control onChange={handleScheduleSemester} as="select" id="schedule-semester" name="schedule-semester">
                                    <option value="fall">Fall</option>
                                    <option value="spring">Spring</option>
                                </Form.Control>
                                <Button variant="secondary" onClick={handleClose}>
                                    Cancel
                                </Button>
                                <Button onClick={createSchedule} variant="primary" id="signup-form-submit" className="signup-form-field">
                                    Create Schedule
                                </Button>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                </Modal>

                <Modal show={compare} onHide={handleCloseCompare}>
                    <Modal.Header closeButton>
                        <Modal.Title>Compare Two Schedules</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form method="post" action="/api/compare">
                            <Form.Group>   
                                <Form.Control as="select" id="schedule-one" name="schedule-one">
                                    {success.map((value, index) => {
                                        return <option key={index} value={value["scheduleName"]}>{value["scheduleName"]}</option>
                                    })}
                                </Form.Control>
                                <Form.Control as="select" id="schedule-two" name="schedule-two">
                                    {success.map((value, index) => {
                                        return <option key={index} value={value["scheduleName"]}>{value["scheduleName"]}</option>
                                    })}
                                </Form.Control>
                                <Button variant="secondary" onClick={handleCloseCompare}>
                                    Cancel
                                </Button>
                                <Button variant="primary" type="submit" id="compare-schedule" className="signup-form-field">
                                   Compare Selected Schedules
                                </Button>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                </Modal>
            </div>
        </div>     
    );
}

export default Home