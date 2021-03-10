import React, {Component, useState, useEffect, useRef} from 'react';
import {DayPilot, DayPilotCalendar, DayPilotNavigator} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'
import Form from 'react-bootstrap/Form'
import '../static/styles/Schedule-Style.css'
import Button from 'react-bootstrap/Button'


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

global.addedClass = false;
global.classAdded = "";
global.classEvents = [];
global.courses = [];
global.classTime = "";
global.endTime = "";
global.conflict = false;
global.removedCourses = []
global.className = "";

class Schedule extends Component {

  constructor(props) {
    super(props);
    this.addClass = this.addClass.bind(this);
    this.state = {
      viewType: "Resources",
      durationBarVisible: false,
      timeRangeSelectedHandling: "Enabled",
      eventDeleteHandling: "Update",
      courseInfo: [],
      myRef: React.createRef(true),
      onEventDeleted: function(args) {
        if(!global.removedCourses.includes(args.e.text())) {
          global.removedCourses.push(args.e.text());
        }
        this.message("Course Deleted: " + args.e.text());
        var newEvents = [];
        var newCourses = [];
        global.classEvents.forEach(element => {
          if(element.text != args.e.text()) {
            newEvents.push(element);
            if(newCourses.includes(element.text) == false) {
              newCourses.push(element.text)
            }
          }
          global.classEvents = newEvents;
          global.courses = newCourses;
        });        
      }
    };
    console.log(global.removedCourses);
    console.log(global.courses)
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

  //TODO: Send async request to see if a user is allowed to take the course or not (checking prerequisites)
  addClass(e) {
    if(e.target && e.target.nodeName === "A") {
      var days = e.target.id.substring(e.target.id.indexOf("!") + 1, e.target.id.length);
      var section_and_time = e.target.id.substring(e.target.id.indexOf("*") + 1, e.target.id.indexOf("!"));
      var start_end_times = section_and_time.substring(section_and_time.indexOf("*") + 1, section_and_time.length);
      global.classTime = start_end_times.substring(0, start_end_times.indexOf("*"));
      if(global.classTime.length < 8) {
        global.classTime = "0" + global.classTime
      }
      global.endTime = start_end_times.substring(start_end_times.indexOf("*") + 1, start_end_times.length);
      if(global.endTime.length < 8) {
        global.endTime = "0" + global.endTime;
      }
      var text = e.target.innerText
      global.addedClass = true;
      global.classAdded = {text};
      global.className = text.substring(0, text.indexOf("-") - 9);

      var id = 1
    }
    if(global.classAdded) { 
      var cont = true;
      global.courses.push(global.classAdded.text)
      for(var i = 0; i < days.length; i++) {
        var res = "";
        switch(days.charAt(i)) {
          case "M":
            res = "monday";
            break;
          case "T":
            res = "tuesday";
            break;
          case "W":
            res = "wednesday";
            break;
          case "R":
            res = "thursday";
            break;
          default:
            res = "friday";
            break;
        }
        global.classEvents.forEach(element => {
          if((element.start.value == "2013-03-25T" + global.classTime) && element.resource == res) {
            global.conflict = true;
          }
        })
        if(!global.conflict) {
          global.classEvents.push({
            "id": 1,
            "text": global.className,
            "start": "2013-03-25T" + global.classTime,
            "end": "2013-03-25T" + global.endTime,
            "resource": res,
            "days": days
            },
          )
          this.setState({
            events: global.classEvents,
          })
        }
      }
      if(global.conflict) {
        global.conflict = false;
        cont = false;
        alert("Error: Adding '" + global.classAdded.text + "' will cause a time conflict.");
      }
      // This is where we are going to check prerequisites
      if(cont) {

      }
    }
  }

  saveSchedule() {
    var http = new XMLHttpRequest();
    var url = '/api/schedule';
    var params = JSON.stringify(
      {
        courses: global.courses,
        removed: global.removedCourses,
      }
    );
    console.log(global.courses);
    http.open("POST", url, true);

    http.onreadystatechange = function() {
      if(http.readyState == 4) {
        alert("Schedule Saved Successfully");
      }
    }
    http.send(params);
    global.courses = [];
    window.location = "/Home";
  }

  async componentDidMount() {
    if(this.state.myRef) {
      await axios.get('http://localhost:5000/api/getScheduleInfo')
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
          global.classEvents = response.data;
          console.log(global.courses);
      })
      await axios.get('http://localhost:5000/api/schedule')
      .then((response) => {
          response.data.forEach(element => {
            var para = document.createElement("li");
            var tag = document.createElement("a");
            para.appendChild(tag);
            var node = document.createTextNode(element["course_name"] + " " + element["course_section"]);
            var course = document.createTextNode(element["course_code"] + "\n");
            var time = document.createTextNode(" " + element["course_time"] + " - " + element["course_end"])
            tag.appendChild(course);
            tag.appendChild(time);
            tag.appendChild(node);
            tag.setAttribute("id", element["course_name"] + "*" + element["course_section"] + "*" + element["course_time"] + "*" + element["course_end"] + "!" + element["days"]);
            var element = document.getElementById("courses");
            element.appendChild(para);
          })
          document.getElementById("courses").addEventListener("click", this.addClass);

          document.getElementById("myInput").addEventListener("click", function(e) {
            console.log("bar was clicked")
          })
      })
    }
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
                        <div id="div1">
                        <input type="text" id="myInput" onKeyUp={this.classFilter} placeholder="Search for Class" title="Type in a name"></input>
                        <ul id="courses"></ul>
                        </div>
                    </div>
                </div>
            </div>
            <Button onClick={this.saveSchedule} variant="primary" type="submit" id="signup-form-submit" className="signup-form-field">
                Save Schedule
            </Button>
            <Button href="/home" variant="secondary" type="submit" id="exit-schedule" className="signup-form-field">
              Exit
            </Button>
        </div>
    );
  }
}

export default Schedule;