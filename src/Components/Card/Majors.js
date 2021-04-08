import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import {DropdownButton, Dropdown} from 'react-bootstrap'
import CoolTabs from 'react-cool-tabs';
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'
import Accordion from 'react-bootstrap/Accordion'
import Card from 'react-bootstrap/Card'

export const Majors = () => {

    //const [isLoading, setLoading] = useState(true);
    const isFirst = useRef(true);
    //const [success, setSuccess] = useState(null);
    //const majorCourses = []

    var state = {activeIndex: 0};
 
    
    var majorList = document.createElement("ul");
    var recMinorList = document.createElement("ul");
    var minorList = document.createElement("ul");

    

    function getMajorsAndMinorsData(requirementYear) {
        var email = String(window.location).split("?")[1];
        email = String(email).split("=")[1]
        console.log(email);
        axios.get('http://localhost:5000/api/getAllMajorsAndMinors?email=' + email).then((response) => {
            const firstResponse = response.data[requirementYear];
            const majorResponse = firstResponse["majors"];
            const minorResponse = firstResponse["minors"];
            const recMinorResponse = firstResponse["recMinors"]
            majorResponse.forEach(element => {
                //majors.push(element);
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var majorInformationNode = document.createElement("li");
                var majorTitle = document.createElement("div");
                majorTitle.setAttribute("id", "columnTitle");
                majorTitle.appendChild(document.createTextNode("Requirements:"));

                //var classesRequiredString = "Requirements: "
                majorInformationNode.appendChild(majorTitle);
                requirements.forEach(requirement => {
                    var currentRequirementString = "";
                    currentRequirementString += requirement["name"] + ": ";

                    var listLength = requirement["courseList"].length;
                    if (listLength == 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength == listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                        })
                    }
                    
                    currentRequirementString += "; ";
                    //classesRequiredString += currentRequirementString;
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.setAttribute("id", "requirementInformation");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    majorInformationNode.appendChild(currentRequirementNode);
                })
                var para = document.createElement("li");
                var tag = document.createElement("a");
                tag.setAttribute("class", "majorButton")
                para.setAttribute("id", name);
                
                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                //var moreInformationNode = document.createTextNode(classesRequiredString);
                tag.appendChild(node);
                //tag.addEventListener("click", this.loadMajor(name));
                tag.addEventListener("click", function() {
                    if (para.nextSibling != null) {
                        //majorList.insertBefore(moreInformationNode, para.nextSibling);
                        majorList.insertBefore(majorInformationNode, para.nextSibling);
                    }
                });
                para.appendChild(tag);
                majorList.appendChild(para);
            });
            minorResponse.forEach(element => {
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var classesRequiredString = "Requirements: ";
                var minorInformationNode = document.createElement("li");
                var minorTitle = document.createElement("div")
                minorTitle.setAttribute("id", "columnTitle");
                minorTitle.appendChild(document.createTextNode("Requirements: "));


                minorInformationNode.appendChild(minorTitle);
                requirements.forEach(requirement => {
                    var currentRequirementString = "";

                    var listLength = requirement["courseList"].length;
                    if (listLength == 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength == listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                            
                        })
                    }

                    
                    
                    currentRequirementString += "; ";
                    //classesRequiredString += currentRequirementString;
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.setAttribute("id", "requirementInformation");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    minorInformationNode.appendChild(currentRequirementNode);
                })
                var para = document.createElement("li");
                var tag = document.createElement("button");
                tag.setAttribute("id", "minorButton");
                para.setAttribute("id", name);
                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);

                var moreInformationNode = document.createTextNode(classesRequiredString);
                tag.appendChild(node);
                tag.addEventListener("click", function() {
                    if (para.nextSibling != null) {
                        minorList.insertBefore(minorInformationNode, para.nextSibling);
                    }
                });
                para.appendChild(tag);
                minorList.appendChild(para);
            });
            recMinorResponse.forEach(element => {
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var classesRequiredString = "Requirements: ";
                var minorInformationNode = document.createElement("li");
                var minorTitle = document.createElement("div")
                minorTitle.setAttribute("id", "columnTitle");
                minorTitle.appendChild(document.createTextNode("Requirements: "));


                minorInformationNode.appendChild(minorTitle);
                requirements.forEach(requirement => {
                    var currentRequirementString = "";

                    var listLength = requirement["courseList"].length;
                    if (listLength == 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength == listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                            
                        })
                    }

                    
                    
                    currentRequirementString += "; ";
                    //classesRequiredString += currentRequirementString;
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.setAttribute("id", "requirementInformation");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    minorInformationNode.appendChild(currentRequirementNode);
                })
                var para = document.createElement("li");
                var tag = document.createElement("button");
                tag.setAttribute("id", "minorButton");
                para.setAttribute("id", name);
                // var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                var node = document.createTextNode(name );

                var moreInformationNode = document.createTextNode(classesRequiredString);
                tag.appendChild(node);
                tag.addEventListener("click", function() {
                    if (para.nextSibling != null) {
                        recMinorList.insertBefore(minorInformationNode, para.nextSibling);
                    }
                });
                para.appendChild(tag);
                recMinorList.appendChild(para);
            });
        })
    }

    function getMinors() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(minorList);
    }

    function getMinorsRec() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(recMinorList);
    }

    function getMajors() {
        var parent = document.getElementById("MajorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        } 
        parent.appendChild(majorList);
    }

    function getMajorsAndMinors(requirementYear) {
        getMajorsAndMinorsData(requirementYear);
        getMinors();
        getMajors();
    }

      /*
  ClassFilter() --> Helper function used to display courses that the user searches for using the 
  searchbar on the side column. Courses that match the pattern that the user enters are displayed, 
  while all others are hidden. 
  */
  function majorFilter() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    console.log(input)
    filter = input.value.toUpperCase();
    ul = document.getElementById("MajorList");
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
  MinorFilter() --> Helper function used to display courses that the user searches for using the 
  searchbar on the side column. Courses that match the pattern that the user enters are displayed, 
  while all others are hidden. 
  */
  function minorFilter() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("minorInput");
    console.log(input)
    filter = input.value.toUpperCase();
    ul = document.getElementById("MinorList");
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

    return (
        <div id="main-content">
           <Navbar bg="dark" variant="dark" expand="lg">
              <Navbar.Brand><Image src={Logo} style={{height: 50}}/></Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                  <Nav.Link href={"/home?" + String(window.location).split("?")[1]}>Scheduling</Nav.Link>
                  <Nav.Link href={"/degree?" + String(window.location).split("?")[1]}>Degree Report</Nav.Link> 
                  <Nav.Link href={"/majors?" + String(window.location).split("?")[1]}>Majors and Minors</Nav.Link> 
                  <Nav.Link href={"/profile?" + String(window.location).split("?")[1]}>Profile</Nav.Link> 
              </Nav>
              </Navbar.Collapse>
            </Navbar>
        <div class="req-content">
            <div class="reqYear" className="req-buttons">
                <div id="columnTitle" >Requirement Year</div>
                <button onClick={() => {getMajorsAndMinors("2017")}} className="req-button">2017-2018</button>
                {/* <button onClick={() => {getMajorsAndMinors("2018")}} className="req-button">2018-2019</button>
                <button onClick={() => {getMajorsAndMinors("2019")}} className="req-button">2019-2020</button>
                <button onClick={() => {getMajorsAndMinors("2020")}} className="req-button">2020-2021</button> */}
            </div>

            <h2> Search Majors </h2>
                <div id="div1">
                <input type="text" id="myInput" onKeyUp={majorFilter} placeholder="Search for Major" title="Type in a name"></input>
                <ul id="courses"></ul>
                </div>

            <h2> Search Minors </h2>
                <div id="div1">
                <input type="text" id="minorInput" onKeyUp={minorFilter} placeholder="Search for Minor" title="Type in a name"></input>
                <ul id="courses"></ul>
                </div>

                <Accordion defaultActiveKey="0">
  <Card>
    <Accordion.Toggle as={Card.Header} eventKey="0">
      Click me!
    </Accordion.Toggle>
    <Accordion.Collapse eventKey="0">
      <Card.Body>Hello! I'm the body</Card.Body>
    </Accordion.Collapse>
  </Card>
  <Card>
    <Accordion.Toggle as={Card.Header} eventKey="1">
      Click me!
    </Accordion.Toggle>
    <Accordion.Collapse eventKey="1">
      <Card.Body>Hello! I'm another body</Card.Body>
    </Accordion.Collapse>
  </Card>
</Accordion>
            <CoolTabs
                tabKey={'1'}
                style={{ width:  1500, height:  650, background:  'blue', margin: 20,}}
                tabsHeaderStyle={{height: 100}}
                activeTabStyle={{ background:  'purple', color:  'white' }}
                unActiveTabStyle={{ background:  'white', color:  'black'}}
                leftContentStyle={{ background:  'white' }}
                rightContentStyle={{ background:  'white' }}

                leftTabTitleStyle={{fontSize: 40}}
                rightTabTitleStyle={{fontSize: 40}}
                
                leftTabTitle={'Majors'}
                rightTabTitle={'Minors'}
                leftContent={
                    <div id="MajorList"> Click on a requirement year to view minors. It can take up to 10 seconds to display. </div> 
                }
                rightContent={
                    <div>
                        <div id="sortingButton">

                            <DropdownButton id="dropdown-basic-button" title="Sort by">
                                <Dropdown.Item onClick={getMinors}>A-Z</Dropdown.Item>

                                <Dropdown.Item onClick={getMinorsRec}>Recommended</Dropdown.Item>
                            </DropdownButton>
                        </div>
                

                <div id="MinorList"> Click on a requirement year to view minors. It can take up to 10 seconds to display. </div> 
                </div>
                }
                
            />


            </div>
            </div>

    );
}


export default Majors





