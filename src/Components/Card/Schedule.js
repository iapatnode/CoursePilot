import React, {Component, useState, useEffect} from 'react';
import {DayPilot, DayPilotCalendar, DayPilotNavigator} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'
import Form from 'react-bootstrap/Form'
import '../static/styles/Schedule-Style.css'


const styles = {
  wrap: {
    display: "flex"
  },
  left: {
    marginRight: "10px"
  },
  main: {
    flexGrow: "1"
  }
};


class Schedule extends Component {

  constructor(props) {
    super(props);
    this.state = {
      viewType: "Resources",
      durationBarVisible: false,
      timeRangeSelectedHandling: "Enabled",
      eventDeleteHandling: "Update",
      onEventDeleted: function(args) {
          this.message("Course Deleted: " + args.e.text());
      }
    };
  }

  componentDidMount() {

    axios.get('http://localhost:5000/api/schedule')
        .then((response) => {
            console.log(response);
            this.setState({
                columns: [
                    { name: "Monday", id: "monday", start: "2013-03-25" },
                    { name: "Tuesday", id: "tuesday", start: "2013-03-25" },
                    { name: "Wednesday", id: "wednesday", start: "2013-03-25" },
                    { name: "Thursday", id: "thursday", start: "2013-03-25" },
                    { name: "Friday", id: "friday", start: "2013-03-25" },
                ],
                events: response.data,
            })
        })
  }

  render() {
    var {...config} = this.state;
    return (
        <div>
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
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-9">
                        <DayPilotCalendar
                        {...config}
                        ref={component => {
                            this.calendar = component && component.control;
                        }}
                        />
                    </div>
                    <div className="col-md-3" id="search-container">
                      <h2> Search Courses </h2>
                        <Form noValidate autocomplete="off" method="post" action="/api/search">
                            <Form.Group>
                              <Form.Control 
                                type="search"
                                name="outlined-search" 
                                placeholder="Enter Course Name/Code Here">
                              </Form.Control>
                            </Form.Group>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    );
  }
}

export default Schedule;