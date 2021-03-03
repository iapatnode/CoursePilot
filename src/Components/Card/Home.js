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

global.semester="";

export const Home = ()=> {

    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);
    const [redirect, setRedirect] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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

    async function clickListener(e) {
        console.log(e.target.innerText);
        let params = {
            "name": e.target.innerText
        }
        var result = await makePostRequest('/api/existingSchedule', params);
        console.log(result);
        if(result == "good") {
            alert("Schedule Loaded... Take me to my schedule!");
            window.location = "/Schedule";
        }
    }

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
            <h1> Schedules </h1>
            <div className="container" id="schedule-list-view">
                <div className="row">
                <div className="col-2 text-center" id="container"></div>
                    <div className="col-md-4 col-md-offset-2" id="names">
                        <h2> Name </h2>
                        <ul>
                            {success.map((value, index) => {
                                let schedule_url = "http://localhost:3000/Schedule"
                                return <li onClick={clickListener} key={index} value={value["scheduleName"]}>{value["scheduleName"]}<br></br></li>
                                // return <Link id="link" to='/Schedule' key={index} value={value["scheduleName"]}>{value["scheduleName"]}<br></br></Link>
                            })}
                        </ul>
                    </div>
                    <div className="col-md-4" id="dates">
                        <h2> Date Modified </h2> 
                        <ul>
                            {success.map((value, index) => {
                                return <li key={index} value={value["dateModified"]}>{value["dateModified"]}</li>
                            })}
                        </ul>
                    </div>
                    <div className="col-2"></div>
                </div>
            </div>
            <div id="button-container">
                <Button variant="primary" onClick={handleShow}> Create New Schedule </Button>
                <Modal show={show} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Create New Schedule - Enter Name</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form method="post" action="/api/home">
                            <Form.Group>
                                <Form.Control type="text" placeholder="Enter Schedule Name" id="schedule-name" name="schedule-name"></Form.Control>
                                <Form.Control as="select" id="schedule-semester" name="schedule-semester">
                                    <option value="fall">Fall</option>
                                    <option value="spring">Spring</option>
                                </Form.Control>
                                <Button variant="secondary" onClick={handleClose}>
                                    Cancel
                                </Button>
                                <Button variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                                    Create Schedule
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