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
      courseInfo: [],
      onEventDeleted: function(args) {
          this.message("Course Deleted: " + args.e.text());
      }
    };
  }
  
  classFilter() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    console.log(input)
    filter = input.value.toUpperCase();
    ul = document.getElementById("courses");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
  }

  componentDidMount() {

      axios.get('http://localhost:5000/api/schedule')
        .then((response) => {
            var start = "2013-03-25T12:00:00"
            var end = "2013-03-25T13:00:00"
            var text = ""
            var id = 1
            var resource = "monday"
            console.log(response.data);
            this.setState({
                columns: [
                    { name: "Monday", id: "monday", start: "2013-03-25" },
                    { name: "Tuesday", id: "tuesday", start: "2013-03-25" },
                    { name: "Wednesday", id: "wednesday", start: "2013-03-25" },
                    { name: "Thursday", id: "thursday", start: "2013-03-25" },
                    { name: "Friday", id: "friday", start: "2013-03-25" },
                ],
                events: [],
                courseInfo: response.data,
            })
            response.data.forEach(element => {
              var para = document.createElement("li");
              var tag = document.createElement("a");
              para.setAttribute("id", element["course_name"] + "/" + element["course_section"])
              para.appendChild(tag)
              var node = document.createTextNode(element["course_name"] + " " + element["course_section"]);
              tag.appendChild(node);
              var element = document.getElementById("courses");
              element.appendChild(para);
            })
            document.getElementById("courses").addEventListener("click", function(e) {
              if(e.target && e.target.nodeName === "A") {
                //was console.log(e.target.id)
                console.log(e.target.innerText + " was clicked");
                text = e.target.innerText
                console.log(text)
                id = 1
              }
              
            })
            document.getElementById("myInput").addEventListener("click", function(e) {
              console.log("bar was clicked")
            })
            // this.setState({
            //   events: [
            //     {
            //       "start": start,
            //       "end": end,
            //       "text": text,
            //       "id": id,
            //       "resource": resource
            //     }
            //   ]
            // })
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
                        <Form noValidate autoComplete="off" method="post" action="/api/search">
                        
                            <Form.Group>
                              <Form.Control 
                                type="search"
                                name="outlined-search" 
                                placeholder="Enter Course Name/Code Here">
                              </Form.Control>
                            </Form.Group>
                        </Form>
                        
                        <div id="div1">
                        <input type="text" id="myInput" onKeyUp={this.classFilter} placeholder="Search for Class" title="Type in a name"></input>
                          <ul id="courses">
                            
                          </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
  }
}

export default Schedule;