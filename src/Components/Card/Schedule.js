import React, {Component} from 'react';
import {DayPilotCalendar} from "daypilot-pro-react";
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import axios from 'axios'
import '../static/styles/Schedule-Style.css'
import Button from 'react-bootstrap/Button'
import Logo from '../static/images/logo.jpg'
import Image from 'react-bootstrap/Image'


// Class Variables
global.addedClass = false; // Variable that tells whether or not the user has added a class
global.classAdded = ""; // Keep track of the information of the course that was added 
global.classEvents = []; // Array of classes that displays class events on the calendar
global.courses = []; // Array of courses that is used in a post request to add courses to the DB
global.classTime = ""; // Start time of the class that was added
global.endTime = ""; // End time of the class that was added
global.conflict = false; // Keep track of any time conflicts in the schedule
global.removedCourses = [] // List of courses that the user has removed from the schedule
global.className = ""; // Name of the class that was added
global.formSubmitting = false;
global.email = "";


class Schedule extends Component {
  
  // Constructor to set state variables for the schedule page
  constructor(props) {
    super(props);
    this.addClass = this.addClass.bind(this); // Method used to add a class to the schedule component
    this.state = {
      viewType: "Resources",
      durationBarVisible: false,
      timeRangeSelectedHandling: "Enabled",
      eventDeleteHandling: "Update",
      courseInfo: [],
      myRef: React.createRef(true), // Variable used to make sure that get requests are executed in order

      // Function used to delete courses from the schedule and the database. 
      onEventDeleted: function(args) {
        if(!global.removedCourses.includes(args.e.text())) {
          global.removedCourses.push(args.e.text());
        }
        this.message("Course Deleted: " + args.e.text());
        var newEvents = [];
        var newCourses = [];
        global.classEvents.forEach(element => {
          if(element.text !== args.e.text()) {
            newEvents.push(element);
            if(newCourses.includes(element.text) === false) {
              newCourses.push(element.text)
            }
          }
          global.classEvents = newEvents;
          global.courses = newCourses;
        });        
      }
    };
  }
  
  /*
  ClassFilter() --> Helper function used to display courses that the user searches for using the 
  searchbar on the side column. Courses that match the pattern that the user enters are displayed, 
  while all others are hidden. 
  */
  classFilter() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
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

  /*
  Helper method: titleCase() is used to display the course names in title case 
  (i.e. the first letter of each word is capitalized)
  */
  titleCase(x) {
    var str = x.toLowerCase();
    var str1 = str.split(' ');
    for(var i = 0; i < str1.length; i++) {
      str1[i] = str1[i].charAt(0).toUpperCase() + str1[i].slice(1);
    }
    return str1.join(' ');
  }

  /*
  addClass() --> Method used to add a course that the user selects to the schedule component
  on the web page. Does this by parsing the id of the course selected, picking out the name, 
  course code, start and end times, and section, appending them to the appropriate lists, and 
  updating the schedule component to place the class on the schedule and rerender the page. 
  */
  addClass(e) {
    var course_code;
    var cont = true;
    // If the user has clicked an element, and it is an a tag (i.e. it is a course)
    if(e.target && e.target.nodeName === "A") {
      // Get all of the course information from the ID of the element
      var days = e.target.id.substring(e.target.id.indexOf("!") + 1, e.target.id.indexOf("~"));
      var section_and_time = e.target.id.substring(e.target.id.indexOf("*") + 1, e.target.id.indexOf("!"));
      var start_end_times = section_and_time.substring(section_and_time.indexOf("*") + 1, section_and_time.length);
      course_code = e.target.id.substring(e.target.id.indexOf("~") + 1);
      global.classTime = start_end_times.substring(0, start_end_times.indexOf("*"));

      // Class time needs to have the format HH:MM:SS, make sure that all courses fit this format. 
      if(global.classTime.length < 8) {
        global.classTime = "0" + global.classTime
      }
      global.endTime = start_end_times.substring(start_end_times.indexOf("*") + 1, start_end_times.length);
      if(global.endTime.length < 8) {
        global.endTime = "0" + global.endTime;
      }

      /*
      Get the course code and course name of each course that is added to the schedule. If there is 
      already an instance of the course in the schedule, the user is alerted that they cannot add
      duplicate classes, and the course is not added to the schedule
      */
      var text = e.target.innerText
      global.addedClass = true;
      global.classAdded = {text};
      global.className = text.substring(0, text.indexOf("-") - 9);
      var section = global.classAdded.text.slice(-1)
      global.classEvents.forEach(element => {
        if(element["text"] === course_code && cont && section <= "L") {
          alert("Error: You have already added this course to your schedule");
          cont = false;
        }
      });
    }

    /*
    If there are no instances of the course already in the user's schedule, check to see
    if adding the course will result in a time conflict. If it does, alert the user that
    adding the course will cause a time conflict. Otherwise, add the course to the schedule
    state variable and update the page. 
    */
    if(global.classAdded && cont) { 
      global.courses.push(global.classAdded.text)
      // For each day of the course, create a calendar event for the given day
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
        // Check if adding the course will result in a time conflict. 
        global.classEvents.forEach(element => {
          var classTime = "2013-03-25T" + global.classTime;
          var endTime = "2013-03-25T" + global.endTime;
          console.log(element.start.value.substring(11, 13))
          if((element.start.value === "2013-03-25T" + global.classTime) && element.resource === res) {
            global.conflict = true;
          }
          else if (element.start.value.substring(11, 13) < classTime.substring(11, 13) && element.start.value.substring(11, 13) < endTime.substring(11, 13)) {
            global.conflict = true;
          }
          else if (element.start.value.substring(11, 13) > classTime.substring(11, 13) && element.start.value.substring(11, 13) <= endTime.substring(11, 13)) {
            global.conflict = true;
          }
        })

        // If adding the course does not result in a time conflict, add the course to the schedule
        if(!global.conflict) {
          global.classEvents.push({
            "id": 1,
            "text": global.className.substring(0, 8),
            "start": "2013-03-25T" + global.classTime,
            "end": "2013-03-25T" + global.endTime,
            "resource": res,
            "days": days,
            "backColor": "#926DD6"
            },
          )
          this.setState({
            events: global.classEvents,
          })
        }
      }
      // Alert the user of potential time conflicts. 
      if(global.conflict) {
        global.courses.pop()
        global.conflict = false;
        cont = false;
        alert("Error: Adding '" + global.classAdded.text + "' will cause a time conflict.");
      }
    }
  }

  /*
  When the user selects the save schedule option, send a post request that contains all of the 
  course info from the schedule. 
  */
  saveSchedule() {
    var http = new XMLHttpRequest();
    var queryString = String(window.location).split("?")[1];
    var url = '/api/schedule?' + queryString + "&semester=fall";
    var params = JSON.stringify(
      {
        courses: global.courses,
        removed: global.removedCourses,
      }
    );
    http.open("POST", url, true);

    http.onreadystatechange = function() {
      if(http.readyState === 4) {
        alert(this.responseText);
        global.courses = [];
        window.location = "/Home?" + String(queryString).split("&")[0];
      }
    }
    global.formSubmitting = true;
    http.send(params);
  }

  exitSchedule(location) {
    var queryString = String(window.location).split("?")[1];
    window.location = "/Home?" + String(queryString).split("&")[0];
  }

  /*
  When the user selects the delete option on the schedule page, send a post request to the
  given api route that contains the name of the schedule to be deleted and then redirects the 
  user. 
  */
  deleteSchedule() {
    var http = new XMLHttpRequest();
    var queryString = String(window.location).split("?")[1]
    var email = queryString.split("&")[0]
    var scheduleName = queryString.split("&")[1];
    scheduleName = scheduleName.split("=")[1]
    var queryString = String(window.location).split("?")[1]
    var url = '/api/delete?' + queryString;
    http.open("POST", url, true);
    http.onreadystatechange = function() {
      if(http.readyState === 4) {
        if(this.responseText === "success") {
          alert("Schedule Deleted Successfully");
          global.formSubmitting = true;
          window.location = "/Home?" + email;
        } 
        else {
          alert("Whoops... That didn't seem to work");
          global.formSubmitting = true;
          window.location = "/Home?" + email;
        }
      }
    }
    if(window.confirm("Click 'OK' if you are sure you want to delete this schedule.")) {
      http.send();
    }
  }

  /*
  componentDidMount() --> When the page first loads, send a request to check to see if the schedule
  already exists in the database. If it does, populate the schedule with the class events that are
  in the database. Otherwise, show the user an empty schedule template. 

  This method also gets a list of all courses that the user can take for the given semester, and will
  display all necessary course information in the sidebar for the user to search
  */
  async componentDidMount() {
    global.email = String(window.location).split("?")[1]
    global.email = String(global.email).split("&")[0]
    global.email = String(global.email).split("=")[1]
    if(this.state.myRef) {
      var queryString = String(window.location).split("?")[1]
      await axios.get('http://localhost:5000/api/getScheduleInfo?' + queryString) 
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
      })
      await axios.get('http://localhost:5000/api/schedule?' + queryString)
      .then((response) => {
          response.data.forEach(element => {
            var para = document.createElement("li");
            var tag = document.createElement("a");
            para.appendChild(tag);
            var node = document.createTextNode(this.titleCase(element["course_name"]) + " " + element["course_section"]);
            var course = document.createTextNode(element["course_code"]);
            var time = document.createTextNode(" " + element["days"] + " " + element["course_time"] + " - " + element["course_end"])
            var br = document.createElement("br");
            tag.appendChild(course);
            tag.appendChild(br);
            tag.appendChild(time);
            tag.appendChild(br);
            tag.appendChild(node);
            tag.setAttribute(
              "id", element["course_name"] + "*" + element["course_section"] + 
              "*" + element["course_time"] + "*" + element["course_end"] + 
              "!" + element["days"] + "~" + element["course_code"]);
            var element = document.getElementById("courses");
            element.appendChild(para);
          })
          document.getElementById("courses").addEventListener("click", this.addClass);
      })
    }
  }

  // HTML Code for the Schedule Page to display course list and schedule component. 
  render() {
    var {...config} = this.state;
    window.addEventListener("beforeunload", function(e) {
      if(global.formSubmitting) {
        return undefined;
      }
      var confirmationMessage = "Are you sure you want to leave this page?";
      (e || window.event).returnValue = confirmationMessage;
      return confirmationMessage;
    });
    return (
        <div id="main-schedule-div">
            <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                  <Nav.Link href={"/Home?email=" + global.email}>Scheduling</Nav.Link>
                  <Nav.Link href={"/degree?email=" + global.email}>Degree Report</Nav.Link> 
                  <Nav.Link href={"/majors?email=" + global.email}>Majors and Minors</Nav.Link> 
                  <Nav.Link href={"/profile?email=" + global.email}>Profile</Nav.Link> 
              </Nav>
              </Navbar.Collapse>
            </Navbar>
            <div className="container-fluid" id="calendar-view">
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
                      <h2 id="search-label"> Search Courses </h2>
                        <div id="div1">
                        <input type="text" id="myInput" onKeyUp={this.classFilter} placeholder="Search for Class" title="Type in a name"></input>
                        <ul id="courses"></ul>
                        </div>
                    </div>
                </div>
            </div>
            <div id="btns">
              <Button onClick={this.exitSchedule} variant="secondary" type="submit" id="exit-schedule">
                Exit
              </Button>
              <Button onClick={this.saveSchedule} variant="primary" type="submit" id="save-schedule">
                  Save Schedule
              </Button>
              <Button onClick={this.deleteSchedule} variant="secondary" type="submit" id="delete-schedule">
                Delete Schedule
              </Button>
            </div>
        </div>
    );
  }
}

export default Schedule;