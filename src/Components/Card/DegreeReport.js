import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormControlLabel from '@material-ui/core/FormControlLabel'
import Checkbox from '@material-ui/core/Checkbox'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete'

export const Report = () => {

    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();
    const [show, setShow] = useState(false);

    const [checked, setChecked] = useState([]);
    const [unchecked, setUnchecked] = useState([]);
    const [selected, setSelected] = useState([]);
    const [unselected, setUnselected] = useState([]);

    useEffect(() => {
        axios.get("/api/degreereport").then(response => {
            setSuccess(response.data);
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
            if (err.response) {
                console.log("BAD!");
            }
        })
    }

    const handleChecked = (event, courseCode, reqCat, reqYear) => {

        //MIGHT NEED TO CHANGE THESE TO ORS
        if(event.target.checked) {
            setUnchecked(unchecked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setChecked(checked.concat({courseCode: courseCode, reqCat: reqCat, reqYear: reqYear}))
        }
        else {
            setChecked(checked.filter((course) => course.courseCode !== courseCode && course.reqCat !== reqCat))
            setUnchecked(unchecked.concat({courseCode: courseCode, reqCat: reqCat, reqYear: reqYear}))
        }

        //NEED TO CHECK IF IT IS IN THE SELECTED LIST, if in unselected, need to remove it
    }

    function isChecked(courses, courseCode, reqCat) {
        for(const course of courses) {
            if(course["course_code"] === courseCode && course["req_cat"] === reqCat) {
                return true
            }
        }
        return false
    }

    //Parses the course code from each course in courses and adds it to an array
    function splitCourses(courses) {
        var courseCodes = []

        for(const course of courses) {
            const courseSplit = course.split(" ")
            const courseString = courseSplit[0] + " " + courseSplit[1]
            courseCodes.push(courseString)
        }

        return courseCodes
    }

    //grabs every course that is in the requirement category we are looking at
    function getReqCourses(requirementCategory) {
        var categoryCourses = []

        for(const course of selected) {
            if(course.reqCat === requirementCategory) {
                categoryCourses.push(course.courseCode)
            }
        }

        return categoryCourses
    }

    /** adds every class that has been removed (i.e., in the selected array but not in the updated list of selected courses) 
         * to a list of deleted courses.
    **/
    function getDeletedCourses(courses, reqCat, reqYear) {
        var deletedCourses = []

        //list that holds all courses in the given requirement categry
        const requirementCourses = getReqCourses(reqCat)

        for(const course of requirementCourses) {
            if(courses.includes(course) === false) {
                deletedCourses.push({courseCode: course, reqCat: reqCat, reqYear, reqYear})
            }
        }

        return deletedCourses
    }

    const handleSelected = (event, courses, reqCat, reqYear) => {
        //list that holds the parsed course codes
        const courseCodes = splitCourses(courses)

        var isChecked = false

        //check if courses have already been selected
        for(const course of courseCodes) {
            if(checked.some(e => e.courseCode == course) || selected.some(e => e.courseCode == course && e.reqCat != reqCat)) {
                alert(course + " is already marked complete on your Degree Report.")
                isChecked = true
            }
        }

        if(isChecked === false) {
            //list that holds the courses that have been deleted
            const deletedCourses = getDeletedCourses(courses, reqCat, reqYear)
                
            /** update the list of selected courses to not include the courses we are deleting and 
             * add the deleted courses to the list of deselected courses
             **/
            if(deletedCourses.length > 0) {
                    setSelected(selected.filter((selectedCourse) => deletedCourses.some(e => e.courseCode == selectedCourse.courseCode) === false || selectedCourse.reqCat !== reqCat))
                    setUnselected(unselected.concat(deletedCourses))
            }
            else {
                /** update the list of selected courses to include the course we are deleting and 
                * delete the course from the list of deselected courses if necessary
                **/
                if(courseCodes.length > 0) {
                    setUnselected(unselected.filter((course) => course.courseCode !== courseCodes[courseCodes.length - 1] || course.reqCat !== reqCat))
                    setSelected(selected.concat({courseCode: courseCodes[courseCodes.length - 1], reqCat: reqCat, reqYear: reqYear}))

                    //removes course from unchecked list if it is there (it has since been selected)
                    setUnchecked(unchecked.filter((course) => course.courseCode !== courseCodes[courseCodes.length - 1]))
                }
            }
        }

        console.log("Selected courses: ")
        console.log(selected)
        console.log("Unselected courses: ")
        console.log(unselected)


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

            <h1> { success[0]["degree_name"] } </h1>

            <div>
                <h3> { "Total Hours: "} { success[0]["degree_hours"] } </h3>  
                <Form id="degree_report">      
                <Button variant="primary" type="submit" value="Submit" onClick={submitListener}>
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
                                        defaultChecked = {isChecked(success[1], course["course_code"], req["req_category"])}
                                        name = {req["req_category"] + " " + course["course_name"]}
                                        onChange={(event) => handleChecked(event, course["course_code"], req["req_category"], success[0]["req_yr"])}
                                    />
                                }
                                label = {course["course_code"] + " " + course["course_name"]}/>
                            })}
                            </Form.Group>
                        </div>
                        : <div className="col-md-12">
                            <Form.Group>
                            <h2> {req["req_category"]}</h2>
                            <h4> {"Required Hours: "} {req["required_hrs"]} </h4>
                            <p> {req["req_details"]} </p>
                            <div>
                                <Autocomplete
                                //set default values
                                    id="elective-courses"
                                    multiple
                                    options={success[2].map((course) => course["course_code"] + " " + course["course_name"])}
                                    style={{ width: 600 }}
                                    onChange = {(event, inputValue) => handleSelected(event, inputValue, req["req_category"], success[0]["req_yr"])}
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