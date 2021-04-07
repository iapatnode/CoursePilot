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

export const Report = () => {
    
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();

    const [checked, setChecked] = useState([]);
    const [unchecked, setUnchecked] = useState([]);
    const [selected, setSelected] = useState([]);
    const [unselected, setUnselected] = useState([]);

    useEffect(() => {
        axios.get("/api/degreereport").then(response => {
            setSuccess(response.data)
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

        axios.post('/api/degreereport', parameters).finally(response => {
            window.location = '/degreereport';
        }).catch(err => {
            if(err.response) {
                console.log("BAD!");
            }
        })
    }

    if (isLoading) {
        return <div> Loading... </div>
    }

    /**
     * Checks if a course (under the checkboxes) is already in the database 
     * @param {*} courseCode the code of the course we are checking if complete
     * @param {*} reqCat    the requirement category under which the course falls
     * @returns true if the course has been checked, false otherwise
     */
    // THIS WORKS AND IS TESTED
    function isChecked(courseCode, reqCat) {
        for(const course of checked) {
            if(course["course_code"] === courseCode && course["req_category"] === reqCat) {
                return true
            }
        }
        return false
    }

    // const handleChecked = (event, courseCode, courseName, reqCat, reqYear) => {
    //     if(event.target.checked && (checked.some(e => e.course_code == courseCode) || selected.some(e => e.course_code == courseCode))) {
    //         alert(courseCode + " " + courseName + " is already marked as completed.")
    //     }
    //     else if(event.target.checked && checked.some(e => e.course_code == courseCode) === false && selected.some(e => e.courseCode == courseCode) === false) {
    //         setUnchecked(unchecked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
    //         setUnselected(unselected.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
    //         setChecked(checked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
    //     }
    //     else if(event.target.unchecked) {
    //         setChecked(checked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
    //         setUnchecked(unchecked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
    //     }

    //     console.log("Checked: ")
    //     console.log(checked)

    //     console.log("Uhchecked: ")
    //     console.log(unchecked)
    // }

    /**
     * Grabs all courses under the given requirement category that have been completed
     * @param {*} reqCat the requirement category that we want to check if any completed courses fall under
     * @returns a list of courses (in course code then course name format) that have been completed for that requirement category
     */
    //THIS WORKS AND HAS BEEN TESTED!!!
    function isSelected(reqCat) {
        var selectedCourses = []

        for(const course of selected) {
            if(course["req_category"] === reqCat) {
                selectedCourses.push(course["course_code"] + " " + course["course_name"])
            }
        }

        return selectedCourses
    }

    return (
        <div id="main-content">
            <Navbar bg="dark" variant="dark" expand="lg">
                <Navbar.Brand href="/home">Course Pilot</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
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

            <h1>{ success[0]["degree_name"] }</h1>

            <div>
                <h3> {"Total Hours: "} { success[0]["degree_hours"] }</h3>

                <Form id="degree_report">
                    <Button variant="primary" type="submit" value="Submit" onClick={submitListener}>Save Changes</Button>

                    { success[0]["req_details"].map((req) => {
                        return <div>
                            {req["req_courses"].length > 0 ?
                                <div className="col-md-12">
                                    <Form.Group>
                                        <h2> {req["req_category"]} </h2>
                                        <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                                        <p> { req["req_details"] }</p>

                                        { req["req_courses"].map((course) => {
                                            return <FormControlLabel control = {
                                                <Checkbox
                                                    defaultChecked = {isChecked(course["course_code"], req["req_category"])}
                                                    name = {course["course_code"] + " " + course["course_name"]}
                                                    // onChange = {(event) => handleChecked(event, course["course_code"], course["course_name"], req["req_category"], success[0]["req_yr"])}
                                                />
                                            }
                                            label = {course["course_code"] + " " + course["course_name"]}/>
                                        })}
                                    </Form.Group>
                                </div>
                            : <div className="col-md-12">
                                <Form.Group>
                                    <h2> {req["req_category"]} </h2>
                                    <h4> {"Required Hours: "} { req["required_hrs"]} </h4>
                                    <p> { req["req_details"] }</p>
                                    <div>
                                        <Autocomplete 
                                            defaultValue = {isSelected(req["req_category"])}
                                            id="elective-courses"
                                            multiple
                                            options={success[1].map((course) => course["course_code"] + " " + course["course_name"])}
                                            style={{ width: 600}}
                                            renderInput = {(params) =>
                                                <TextField {...params}
                                                    label="Select course"
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
