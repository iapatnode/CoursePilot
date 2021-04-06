import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'

global.email = String(window.location).split("?")[1];
global.email = String(global.email).split("=")[1]

export const Report = () => {

    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);

    const [checked, setChecked] = useState([]);
    const [unchecked, setUnchecked] = useState([]);

    useEffect(() => {
        console.log("URL: " + window.location);
        var url_array = String(window.location).split("=")
        global.email = url_array[1];
        axios.get("/api/degreereport?email=" + global.email).then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);

    const submitListener = (e) => {
        const parameters = {
            "add": checked,
            "remove": unchecked
        }

        axios.post('/api/degreereport?email=' + global.email, parameters).finally(response => {
            alert("I made it out of the server code");
        }).catch(err => {
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    const handleChange = (event, courseCode, reqCat, reqYear) => {
        console.log(event)

        if(event.target.checked) {
            setUnchecked(unchecked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setChecked(checked.concat({courseCode: courseCode, reqCat: reqCat, reqYear: reqYear}))
        }
        else {
            setChecked(checked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setUnchecked(unchecked.concat({courseCode: courseCode, reqCat: reqCat, reqYear: reqYear}))
        }

        console.log(checked)
    }

    function isChecked(courses, courseCode, reqCat) {

        console.log(courses)

        for(const course of courses) {
            console.log(course)
            if(course["course_code"] == courseCode && course["req_cat"] == reqCat) {
                return true
            }
        }

        return false
    }

    if (isLoading) {
        return <div> Loading... </div>
    }

    return (
        <div id="main-content">
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                  <Nav.Link href={"/home?email=" + global.email}>Scheduling</Nav.Link>
                  <Nav.Link href={"/degree?email=" + global.email}>Degree Report</Nav.Link> 
                  <Nav.Link href={"/majors?email=" + global.email}>Majors and Minors</Nav.Link> 
                  <Nav.Link href={"/profile?email=" + global.email}>Profile</Nav.Link> 
              </Nav>
              </Navbar.Collapse>
            </Navbar>

            <div>
                <meta charSet="UTF-8"></meta>
            </div>

            <h1> { success[0]["degree_name"] } </h1>

            <div>
                <h3> { "Total Hours: "} { success[0]["degree_hours"] } </h3>  
                <Form id="degree_report">      
                <Button variant="primary" value="Submit" onClick={submitListener}>
                            Save Changes
                </Button>

                { success[0]["req_details"].map((req) => {
                    return <div>
                        <div className="col-md-12">
                        <Form.Group>
                            <h2> {req["req_category"]} </h2> 
                            <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                            <p> {req["req_details"]} </p>
                                { req["req_courses"].map((course) => {
                                    return <FormControlLabel control = {
                                        <Checkbox
                                            defaultChecked = {isChecked(success[1], course["course_code"], req["req_category"])}
                                            name = {req["req_category"] + " " + course["course_name"]}
                                            onChange={(event) => handleChange(event, course["course_code"], req["req_category"], success[0]["req_yr"])}
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