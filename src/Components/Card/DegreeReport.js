import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'
import TextField from '@material-ui/core/TextField'
import Autocomplete from '@material-ui/lab/Autocomplete'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'

global.email = String(window.location).split("?")[1];
global.email = String(global.email).split("=")[1];

export const Report = () => {
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();

    const [checked, setChecked] = useState();
    const [unchecked, setUnchecked] = useState([]);
    const [selected, setSelected] = useState();
    const [unselected, setUnselected] = useState([]);

    useEffect(() => {
        console.log("URL: " + window.location);
        var url_array = String(window.location).split("=")
        global.email = url_array[1];
        axios.get("/api/degreereport?email=" + global.email).then(response => {
            setSuccess(response.data);
            setChecked(response.data[2]["checked"]);
            setSelected(response.data[2]["selected"]);
            setLoading(false);
        });
    }, []);

    const submitListener = (e) => {
        const parameters = {
            "checkedAdd": checked,
            "checkedRemove": unchecked,
            "selectedAdd": selected,
            "selectedRemove": unselected
        }

        axios.post('/api/degreereport?email=' + global.email, parameters).finally(response => {
            alert("Saved Changes Successfully");
        }).catch(err => {
            if(err.response) {
                console.log("BAD!");
            }
        })
    }

    /**
     * Checks if a course (under the checkboxes) is already in the database
     * @param {*} courseCode  the code of the course we are checking if complete
     * @param {*} reqCat the requirement category under which the course falls
     * @returns true if the course has been checked, false otherwise
     */
    // THIS WORKS AND IS TESTED
    function isChecked(courseCode, reqCat) {
        for(const course of checked) {
            if(course["course_code"] == courseCode && course["req_category"] == reqCat) {
                return true
            }
        }

        return false
    }

    /**
     * Grabs all courses under the given requirement category that have been completed
     * @param {*} reqCat the requirement category that we want to check if any completed courses fall under
     * @returns a list of courses (format: courseCode + courseName) that have been completed for that requirement category
     */
    //THIS WORKS AND HAS BEEN TESTED!!
    function isSelected(reqCat) {
        var selectedCourses = []

        for(const course of selected) {
            if(course["req_category"] === reqCat) {
                selectedCourses.push(course["course_code"] + " " + course["course_name"])
            }
        }

        return selectedCourses
    }

    /**
     * Event handler for when a box is checked or unchecked,
     * Adds checked courses to a list of completed courses and removes if previously marked as unchecked
     * Adds unchecked courses to list of previously completed courses and removes from current completed list
     * @param {} event the event that happened (i.e., box was checked or unchecked)
     * @param {*} courseCode the course code
     * @param {*} courseName the name of the course
     * @param {*} reqCat the requirement category that the course falls under
     * @param {*} reqYear the requirement year of the student
     */
    //WORKS, NEEDS TO BE TESTED MORE
    const handleChecked = (event, courseCode, courseName, reqCat, reqYear) => {
        //Checks if course has already been marked as completed in some other category and alerts the user if so
        if(event.target.checked && (checked.some(e => e.course_code == courseCode && e.req_category != reqCat) || selected.some(e => e.course_code == courseCode))) {
            alert(courseCode + " " + courseName + " has already been marked as completed.")
        }
        //handles when course was marked as completed
        else if(event.target.checked) {
            setUnchecked(unchecked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setUnselected(unselected.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setChecked(checked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
        }
        //handles when course was previously marked as complete and is now incomplete
        else if(!event.target.checked) {
            setChecked(checked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setUnchecked(unchecked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
        }

        console.log("Checked: ")
        console.log(checked)

        console.log("Unchecked: ")
        console.log(unchecked)
    }

    if(isLoading) {
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
                        {req["req_courses"].length > 0 ? 
                            <div className="col-md-12">
                                <Form.Group>
                                    <h2> {req["req_category"]} </h2> 
                                    <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                                    <p> {req["req_details"]} </p>
                                        { req["req_courses"].map((course) => {
                                            return <FormControlLabel control = {
                                                <Checkbox
                                                    defaultChecked = {isChecked(course["course_code"], req["req_category"])}
                                                    name = {req["req_category"] + " " + course["course_name"]}
                                                    onChange={(event) => handleChecked(event, course["course_code"], course["course_name"], req["req_category"], success[0]["req_yr"])}
                                                />
                                            }
                                            label = {course["course_code"] + " " + course["course_name"]}/>
                                        })}
                                </Form.Group>
                            </div>
                            : <div className="col-md-12">
                                <Form.Group>
                                    <h2> { req["req_category"] }</h2>
                                    <h4> {"Required Hours: "} { req["required_hrs"]} </h4>
                                    <p> { req["req_details"] }</p>
                                    <div>
                                        <Autocomplete
                                            defaultValue = {isSelected(req["req_category"])}
                                            id="elective-courses"
                                            multiple
                                            options={success[1].map((course) => course["course_code"] + " " + course["course_name"])}
                                            style={{width: 600}}
                                            renderInput = {(params) =>
                                                <TextField {...params}
                                                    label="Enter course"
                                                    variant="outlined"
                                                />
                                            }
                                        />
                                    </div>
                                </Form.Group>
                            </div>
                        }
                    </div>
                })}
            </Form>
            </div>
        </div>
    );
}

export default Report

