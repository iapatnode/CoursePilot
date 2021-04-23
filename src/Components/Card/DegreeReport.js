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
import '../static/styles/DegreeReport-Style.css'
import { makeStyles } from '@material-ui/core/styles'

global.email = String(window.location).split("?")[1];
global.email = String(global.email).split("=")[1];

// Styling of the autocomplete UI element
const useStyles = makeStyles((theme) => ({
    root: {
        "& .MuiFormLabel-root": {
            color: "#F7F3F3"
        },

        "&:hover .MuiFormLabel-root": {
            color: "#F7F3F3"
        },

        "&.Mui-focused .MuiFormLabel-root": {
            color: "#F7F3F3"
        },

        "& .MuiIconButton-root": {
            color: "#F7F3F3"
        }
    },

    inputRoot: {
        color: "#F7F3F3",
        '&[class*="MuiOutlinedInput-root"] .MuiAutocompleted-input:first-child': {
            paddingLeft: 26
        },
        "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#d89cf6"
        },
        "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#d89cf6"
        },
        "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#d89cf6"
        },
    },

    option: {
        backgroundColor: "#8E8D8D",
        color: "#060606",
        '&[data-focus="true"]': {
            backgroundColor: "#F7F3F3",
            borderColor: 'transparent',
            
        },
        '&[aria-selected="true"]': {
            backgroundColor: "#d89cf6",
            color: "#060606",
            borderColor: 'transparent',
        }
    },

    tag: {
        backgroundColor: "#d89cf6",

        "& .MuiChip-label": {
            color: "#060606",
        },

        "& .MuiChip-deleteIcon": {
            color: "#4B4A4A",
        }
    },
}));

export const Report = () => {
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();

    const [checked, setChecked] = useState([]);
    const [unchecked, setUnchecked] = useState([]);
    const [selected, setSelected] = useState([]);
    const [unselected, setUnselected] = useState([]);

    const styles = useStyles();


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

    /**
     * Handles when an user saves their changes
     * @param {*} e the event that happened (save changes button was hit)
     */
    const submitListener = (e) => {
        const parameters = {
            "checkedAdd": checked,
            "checkedRemove": unchecked,
            "selectedAdd": selected,
            "selectedRemove": unselected
        }

        axios.post('/api/degreereport?email=' + global.email, parameters).finally(response => {
            alert("Changes saved!");
        }).catch(err => {
            if(err.response) {
                console.log(err.response);
            }
        })
    }

    /**
     * Checks if a course (under the checkboxes) is already in the database
     * @param {*} courseCode  the code of the course we are checking if complete
     * @param {*} reqCat the requirement category under which the course falls
     * @returns true if the course has been checked, false otherwise
     */
    function isChecked(courseCode, reqCat) {
        for(const course of checked) {
            if(course["course_code"] === courseCode && course["req_category"] === reqCat) {
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
     * Adds checked courses to a list of completed courses and removes from list of unchecked/unselected courses
     * Adds unchecked courses to list of previously completed courses and removes from current completed list
     * @param {} event the event that happened (i.e., box was checked or unchecked)
     * @param {*} courseCode the course code
     * @param {*} courseName the name of the course
     * @param {*} reqCat the requirement category that the course falls under
     * @param {*} reqYear the requirement year of the student
     */
    const handleChecked = (event, courseCode, courseName, reqCat, reqYear) => {
        //Checks if course has already been marked as completed in some other category and alerts the user if so
        if(event.target.checked && (checked.some(e => e.course_code === courseCode && e.req_category !== reqCat) || selected.some(e => e.course_code === courseCode))) {
            alert(courseCode + " " + courseName + " has already been marked as completed.")
        }

        //handles when course was marked as completed
        if(event.target.checked) {
            setUnchecked(unchecked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setUnselected(unselected.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setChecked(checked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
        }
        //handles when course was previously marked as complete and is now incomplete
        else if(!event.target.checked) {
            setChecked(checked.filter((course) => course.course_code !== courseCode || course.req_category !== reqCat))
            setUnchecked(unchecked.concat({course_code: courseCode, course_name: courseName, req_category: reqCat, req_yr: reqYear}))
        }
    }

    /**
     * Event handler for when for when a course is selected
     * Adds deselected courses to a list of previously selected courses and removes from list of selected courses
     * Adds selected courses to a list of selected courses, removes from previously selected/checked courses
     * @param {*} courses the list of updated completed courses for the given requirement category
     * @param {*} reqCat the requirement category that the courses fall under
     * @param {*} reqYear the requirement year of the student
     */
    const handleSelect = (courses, reqCat, reqYear) => {

        // Parses course codes and course names from the format of courseCode + courseName
        var completedCourses = []
        
        for(const course of courses) {
            const courseSplit = course.split(" ")
            const courseCode = courseSplit[0] + " " + courseSplit[1]

            var courseName = ""

            for(var i = 2; i < courseSplit.length - 1; i++) {
                courseName += courseSplit[i] + " "
            }

            courseName += courseSplit[courseSplit.length - 1]

            completedCourses.push({course_code: courseCode, course_name: courseName})
        }

        // Grabs every course that is in the requirement category and marked as complete
        var completedCategoryCourses = []

        for(const course of selected) {
            if(course.req_category === reqCat) {
                completedCategoryCourses.push({course_code: course.course_code, course_name: course.course_name})
            }
        }

        // Tells us whether we deleted a course or marked a new course as compelte
        var isDeletion = false

        // Adds every class that has been removed to a list of deleted courses
        var deletedCourses = []

        for(const course of completedCategoryCourses) {
            // If course is in the completed courses list but not in the updated completed courses list for the requirement category, then it has been deleted
            if(completedCourses.some(e => e.course_code === course.course_code) === false) {
                isDeletion = true
                deletedCourses.push({course_code: course.course_code, course_name: course.course_name, req_category: reqCat, req_yr: reqYear})
            }
        }

        if(isDeletion === true) {
            // Updates the list of selected courses to not include the deleted courses
            setSelected(selected.filter((course) => deletedCourses.some(e => e.course_code === course.course_code) === false || course.req_category !== reqCat))
            // Adds deleted courses to the list of deselected courses
            setUnselected(unselected.concat(deletedCourses))
        }
        else {
            const completedCourse= completedCourses[completedCourses.length - 1]

            // Alerts user if course has already been marked complete somewhere on the page
            if(selected.some(e => e.course_code === completedCourse.course_code) || checked.some(e => e.course_code === completedCourse.course_code)) {
                alert(completedCourse.course_code + " " + completedCourse.course_name + " has already been marked as completed.")
            }

            // Updates the unselected and unchecked lists (which contain courses that were unmarked) to not include the course that was just marked as completed
            setUnselected(unselected.filter((course) => course.course_code !== completedCourse.course_code || course.req_category !== reqCat))
            setUnchecked(unchecked.filter((course) => course.course_code !== completedCourse.course_code || course.req_category !== reqCat))
            // Updates the list of selected courses to include the courses we are adding
            setSelected(selected.concat({course_code: completedCourse.course_code, course_name: completedCourse.course_name, req_category: reqCat, req_yr: reqYear}))
        }
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

            <div class="container-fluid" id="report-header">
                <div class="row align-items-center text-center">
                    <div class="col-sm-4"></div>
                    <div class="col-sm-4 align-items-center">
                            <h1> { success[0]["degree_name"] } </h1>
                            <h3> { "Total Hours: "} { success[0]["degree_hours"] } </h3> 
                    </div>
                    <div class="col-sm-3">
                        <Button variant="primary" value="Submit" id="save-change" onClick={submitListener}>
                                        Save Changes
                        </Button>
                    </div> 
                    <div class="col-sm-1"></div>
                </div>
            </div>

            <div id="degree-report-content"> 
                { success[0]["req_details"].map((req) => {
                    return <div>
                        {req["req_courses"].length > 0 ? 
                            <div class="mt-3 col-md-12" id="req_block">
                                <h2> {req["req_category"]} </h2> 
                                <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                                <div class="row">
                                    <div class="col-md-4"></div>
                                    <p class="col-md-4"> {req["req_details"]} </p>
                                    <div class="col-md-4"></div>
                                </div>
                                <div class="row">
                                    <div class="col-md-3"></div>
                                    <div class="col-md-4 text-left">
                                        { req["req_courses"].filter(course => req["req_courses"].indexOf(course) % 2 == 0).map((course) => {
                                            return <div>
                                                <FormControlLabel control = {
                                                    <Checkbox 
                                                        style = {{color: "#d89cf6"}}
                                                        defaultChecked = {isChecked(course["course_code"], req["req_category"])}
                                                        name = {req["req_category"] + " " + course["course_name"]}
                                                        onChange={(event) => handleChecked(event, course["course_code"], course["course_name"], req["req_category"], success[0]["req_yr"])}
                                                    />
                                                }
                                                label = {course["course_code"] + " " + course["course_name"]}/>
                                            
                                        </div>
                                        })}
                                    </div>
                                    <div class="col-md-4 text-left">
                                        { req["req_courses"].filter(course => req["req_courses"].indexOf(course) % 2 == 1).map((course) => {
                                                return <div>
                                                    <FormControlLabel control = {
                                                        <Checkbox 
                                                            style = {{color: "#d89cf6"}}
                                                            defaultChecked = {isChecked(course["course_code"], req["req_category"])}
                                                            name = {req["req_category"] + " " + course["course_name"]}
                                                            onChange={(event) => handleChecked(event, course["course_code"], course["course_name"], req["req_category"], success[0]["req_yr"])}
                                                        />
                                                    }
                                                    label = {course["course_code"] + " " + course["course_name"]}/>
                                                
                                            </div>
                                        })}
                                    </div>
                                    <div class="col-md-1"></div>
                                </div>
                            </div>
                            :
                             <div class="mt-3 col-md-12" id="req_block">
                                <h2> { req["req_category"] }</h2>
                                <h4> {"Required Hours: "} { req["required_hrs"]} </h4>
                                <div class="row">
                                    <div class="col-md-3"></div>
                                    <p class="col-md-6"> {req["req_details"]} </p>
                                    <div class="col-md-3"></div>
                                </div>
                                <div class="row">
                                    <div class="col-md-4"></div>
                                    <div class="col-md-4 align-items-center">
                                        <Autocomplete
                                            defaultValue = {isSelected(req["req_category"])}
                                            // id="elective-courses"
                                            classes={styles}
                                            multiple
                                            options={success[1].map((course) => course["course_code"] + " " + course["course_name"])}
                                            style={{width: 600}}
                                            onChange = {(event, inputValue) => handleSelect(inputValue, req["req_category"], success[0]["req_yr"])}
                                            renderInput = {(params) =>
                                                <TextField {...params}
                                                    label="Enter course"
                                                    variant="outlined"
                                                    fullWidth
                                                />
                                            }
                                        />
                                    </div>
                                    <div class="col-md-4"></div>
                                </div>
                            </div>
                        }
                    
                    </div>
                })}
            </div>
        </div>
    );
}

export default Report

