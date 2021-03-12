import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'

export const Report = () => {

    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);

    const [checked, setChecked] = useState([]);
    const [unchecked, setUnchecked] = useState([]);

    // const handleClose = () => setShow(false);
    // const handleShow = () => setShow(true);

    useEffect(() => {
        axios.get("/api/degreereport").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);

    const submitListener = (e) => {
        const parameters = {
            "add": checked,
            "remove": unchecked
        }

        axios.Cancel.post('/api/degreereport', parameters).finally(response => {
            // window.location = '/degreereport';
        }).catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    const handleChange = (event, courseCode, reqCat) => {
        console.log(event)

        if(event.target.checked) {
            setUnchecked(unchecked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setChecked(checked.concat({courseCode: courseCode, reqCat: reqCat}))
        }
        else {
            setChecked(checked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setUnchecked(unchecked.concat({courseCode: courseCode, reqCat: reqCat}))
        }

        console.log(checked)
    }

    if (isLoading) {
        return <div> Loading... </div>
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

            <div>
                <meta charSet="UTF-8"></meta>
            </div>

            <h1> { success["degree_name"] } </h1>

            <div>
                <h3> { "Total Hours: "} { success["degree_hours"] } </h3>  
                <Form id="degree_report">      
                <Button variant="primary" type="submit" value="Submit" onClick={submitListener}>
                            Save Changes
                </Button>

                { success["req_details"].map((req) => {
                    return <div>
                        <div className="col-md-12">
                        <Form.Group>
                            <h2> {req["req_category"]} </h2> 
                            <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                            <p> {req["req_details"]} </p>
                                { req["req_courses"].map((course) => {
                                    return <FormControlLabel control = {
                                        <Checkbox
                                            name = {req["req_category"] + " " + course["course_name"]}
                                            onChange={(event) => handleChange(event, course["course_code"], req["req_category"])}
                                        />
                                    }
                                    label = {course["course_code"] + " " + course["course_name"]}/>
                                })}
                            </Form.Group>
                        </div>
                    </div>
                })}
            </Form>
            </div>
        </div>
    );
}

export default Report