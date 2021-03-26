import React, {Component, useState, useEffect, useRef} from 'react';
import {DayPilot, DayPilotCalendar, DayPilotNavigator} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'
import '../static/styles/Compare-Style.css'


global.classEvents = []; // Global variable keep track of class events for schedule component
global.courses = []; // Global variable keep track of which courses are in the schedule
global.scheduleOne = String(window.location).split("?")[1];
global.scheduleOne = String(global.scheduleOne).split("&")[0];
global.scheduleTwo = String(window.location).split("?")[1];
global.scheduleTwo = String(global.scheduletwo).split("&")[0];


class Schedule extends Component {

  // Set state variables that are used by the schedule component
  constructor(props) {
    super(props);
    this.state = {
      viewType: "Resources",
      durationBarVisible: false,
      timeRangeSelectedHandling: "Enabled",
      eventDeleteHandling: "Update",    
    };
  }
  
  /*
  Method is run when the page loads. Send a GET request to get all of the schedule information
  for the schedules the user has selected to compare, set state variables accordingly. 
  */
  async componentDidMount() {
    await axios.get('http://localhost:5000/api/loadComparedSchedules?' + global.scheduleOne + "&" + global.scheduleTwo + "&email=dybasjt17@gcc.edu")
      .then((response) => {
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

  // HTML for the compare schedule page
  render() {
    var {...config} = this.state; // Set state variables for the page
    window.addEventListener("beforeunload", function(e) {
      var confirmationMessage = "Are you sure you want to leave this page?";
      (e || window.event).returnValue = confirmationMessage;
      return confirmationMessage;
    });
    return (
        <div>
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
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-12">
                        <DayPilotCalendar
                        {...config}
                        ref={component => {
                            this.calendar = component && component.control;
                        }}
                        />
                    </div>

                </div>
            </div>
            <Button href="/home" variant="secondary" type="submit" id="exit-schedule" className="signup-form-field">
              Exit
            </Button>
        </div>
    );
  }
}

export default Schedule;