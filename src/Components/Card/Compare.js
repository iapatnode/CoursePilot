import React, {Component} from 'react';
import {DayPilotCalendar} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'  
import Button from 'react-bootstrap/Button'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'
import '../static/styles/Compare-Style.css'


global.classEvents = []; // Global variable keep track of class events for schedule component
global.courses = []; // Global variable keep track of which courses are in the schedule
global.scheduleOne = String(window.location).split("?")[1];
global.scheduleOne = String(global.scheduleOne).split("&")[0];
global.scheduleTwo = String(window.location).split("?")[1];
global.scheduleTwo = String(window.location).split("&")[1];
global.email = String(window.location).split("&")[2];


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
    console.log(global.email)
    await axios.get('http://coursepilot.gcc.edu:5000/api/loadComparedSchedules?' + global.scheduleOne + "&" + global.scheduleTwo + "&email=" + global.email)
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
    return (
        <div>
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                  <Nav.Link href={"/home?" + global.email}>Scheduling</Nav.Link>
                  <Nav.Link href={"/degree?" + global.email}>Degree Report</Nav.Link> 
                  <Nav.Link href={"/majors?" + global.email}>Majors and Minors</Nav.Link> 
                  <Nav.Link href={"/profile?" + global.email}>Profile</Nav.Link> 
              </Nav>
              </Navbar.Collapse>
            </Navbar>
            <div id="compare-content">
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
              <br/>
              <div className="row" id="legend">
                <h2 id="legend-schedule-one"> Schedule One: {String(global.scheduleOne.split("=")[1].replaceAll("%20", " "))} </h2>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <h2 id="legend-schedule-two"> Schedule Two: {String(global.scheduleTwo.split("=")[1].replaceAll("%20", " "))} </h2>
              </div>
              <Button href={"/home?" + global.email} variant="secondary" type="submit" id="exit-compare-schedule" className="signup-form-field">
                Exit
              </Button>
            </div>
        </div>
    );
  }
}

export default Schedule;