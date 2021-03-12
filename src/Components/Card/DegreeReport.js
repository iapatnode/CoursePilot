import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'



export const Report = () => {

    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);

    // const handleClose = () => setShow(false);
    // const handleShow = () => setShow(true);

    useEffect(() => {
        axios.get("/api/degreereport").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);

    const handleSubmit = (e) => {
        axios.Cancel.post('/api/degreereport', parameters).finally(response => {
            window.location = '/degreereport';
        }).catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    if (isLoading) {
        return <div> Loading... </div>
    }

    //get element by id
    //winodw.addEventListener() -> document.querySelector("checkbox name") -> do a return here -> get all checkbox data -> gets id, name, etc.

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

            <h1> { success["degree_name"] } </h1>

            <div>
                <h3> { "Total Hours: "} { success["degree_hours"] }</h3>        
                { success["req_details"].map((req) => {
                    return <div>
                        <div className="col-md-4 col-fluid">
                            <h2> {req["req_category"]} </h2> 
                            <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                            <p> {req["req_details"]} </p>
                            <Form id="degree_report">
                                { req["req_courses"].map((course) => {
                                    return <Form.Group>
                                        <Form.Label>{course["course_code"]}  {course["course_name"]}</Form.Label>
                                        <Form.Control type="checkbox" name={req["req_category"]} id={course["course_code"]}></Form.Control>
                                    </Form.Group>
                                })}
                            </Form>
                        </div>
                        
                        <Button variant="primary" type="submit">
                            Save Changes
                        </Button>
                    </div>
                })}
            </div>
        </div>
    );
}

export default Report