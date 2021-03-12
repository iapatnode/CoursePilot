import React, {Component, useState, useEffect, useRef} from 'react';
import {DayPilot, DayPilotCalendar, DayPilotNavigator} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'
import Form from 'react-bootstrap/Form'
import '../static/styles/Schedule-Style.css'
import Button from 'react-bootstrap/Button'
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'

global.classEvents = [];
global.courses = [];

class Schedule extends Component {

  constructor(props) {
    super(props);
    this.state = {
      viewType: "Resources",
      durationBarVisible: false,
      timeRangeSelectedHandling: "Enabled",
      eventDeleteHandling: "Update",    
    };
  }
  
  async componentDidMount() {
    await axios.get('http://localhost:5000/api/loadComparedSchedules')
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

  render() {
    var {...config} = this.state;
    return (
        <div>
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
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