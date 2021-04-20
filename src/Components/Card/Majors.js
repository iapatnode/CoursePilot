import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import {DropdownButton, Dropdown} from 'react-bootstrap'
import CoolTabs from 'react-cool-tabs';
import Image from 'react-bootstrap/Image'
import Logo from '../static/images/logo.jpg'

export const Majors = () => {

    const isFirst = useRef(true);

    var state = {activeIndex: 0};

    var majorList = document.createElement("div");
    var recMinorList = document.createElement("div");
    var minorList = document.createElement("div");

    majorList.setAttribute("class", "majorminorlist");
    recMinorList.setAttribute("class", "majorminorlist");
    minorList.setAttribute("class", "majorminorlist");

    function getMajorsAndMinorsData(requirementYear) {
        while (majorList.hasChildNodes()) {
            majorList.removeChild(majorList.firstChild);
        }
        while (recMinorList.hasChildNodes()) {
            recMinorList.removeChild(recMinorList.firstChild);
        }
        while (minorList.hasChildNodes()) {
            minorList.removeChild(minorList.firstChild);
        }
        var email = String(window.location).split("?")[1];
        email = String(email).split("=")[1]
        axios.get('http://coursepilot.gcc.edu:5000/api/getAllMajorsAndMinors?email=' + email).then((response) => {
            const firstResponse = response.data[requirementYear];
            const majorResponse = firstResponse["majors"];
            const minorResponse = firstResponse["minors"];
            const recMinorResponse = firstResponse["recMinors"]
            majorResponse.forEach(element => {
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var majorRequirementsInformation = document.createElement("div");
                majorRequirementsInformation.appendChild(document.createTextNode("Requirements:"));
                requirements.forEach(requirement => {
                    var currentRequirementString = "";
                    currentRequirementString += requirement["name"] + ": ";
                    var listLength = requirement["courseList"].length;
                    if (listLength === 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength === listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                        })
                    }
                    currentRequirementString += "; ";
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    majorRequirementsInformation.appendChild(currentRequirementNode);
                })

                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                var majorTitleButton = document.createElement("button");
                majorTitleButton.setAttribute("class", "accordion");
                majorTitleButton.appendChild(node);
                var majorPanel = document.createElement("div");
                majorPanel.setAttribute("class", "panel");
                majorPanel.appendChild(majorRequirementsInformation);

                majorTitleButton.addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.display === "block") {
                        panel.style.display = "none";
                      } else {
                        panel.style.display = "block";
                      }
                });

                majorList.appendChild(majorTitleButton);
                majorList.appendChild(majorPanel);
            });
            minorResponse.forEach(element => {
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var minorRequirementsInformation = document.createElement("div");
                minorRequirementsInformation.appendChild(document.createTextNode("Requirements:"));
                requirements.forEach(requirement => {
                    var currentRequirementString = "";
                    currentRequirementString += requirement["name"] + ": ";
                    var listLength = requirement["courseList"].length;
                    if (listLength === 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength === listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                        })
                    }
                    currentRequirementString += "; ";
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    minorRequirementsInformation.appendChild(currentRequirementNode);
                })

                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                var minorTitleButton = document.createElement("button");
                minorTitleButton.setAttribute("class", "accordion");
                minorTitleButton.appendChild(node);
                var minorPanel = document.createElement("div");
                minorPanel.setAttribute("class", "panel");
                minorPanel.appendChild(minorRequirementsInformation);

                minorTitleButton.addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.display === "block") {
                        panel.style.display = "none";
                      } else {
                        panel.style.display = "block";
                      }
                });

                minorList.appendChild(minorTitleButton);
                minorList.appendChild(minorPanel);
            });
            recMinorResponse.forEach(element => {
                var name = element["name"];
                var requirements = element["requiredClasses"];
                var recMinorRequirementsInformation = document.createElement("div");
                recMinorRequirementsInformation.appendChild(document.createTextNode("Requirements:"));
                requirements.forEach(requirement => {
                    var currentRequirementString = "";
                    currentRequirementString += requirement["name"] + ": ";
                    var listLength = requirement["courseList"].length;
                    if (listLength === 0) {
                        currentRequirementString += requirement["numHoursRequired"] + " hours";
                    }
                    else {
                        var currentLength = 0;
                        currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                        requirement["courseList"].forEach(course => {
                            currentLength++;
                            if (currentLength === listLength) {
                                currentRequirementString += course;
                            }
                            else {
                                currentRequirementString += course + ", ";
                            }
                        })
                    }
                    currentRequirementString += "; ";
                    var currentRequirementNode = document.createElement("div");
                    currentRequirementNode.appendChild(document.createTextNode(currentRequirementString));
                    recMinorRequirementsInformation.appendChild(currentRequirementNode);
                })

                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                var recMinorTitleButton = document.createElement("button");
                recMinorTitleButton.setAttribute("class", "accordion");
                recMinorTitleButton.appendChild(node);
                var recMinorPanel = document.createElement("div");
                recMinorPanel.setAttribute("class", "panel");
                recMinorPanel.appendChild(recMinorRequirementsInformation);

                recMinorTitleButton.addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    if (panel.style.display === "block") {
                        panel.style.display = "none";
                      } else {
                        panel.style.display = "block";
                      }
                });

                recMinorList.appendChild(recMinorTitleButton);
                recMinorList.appendChild(recMinorPanel);
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
    MajorFilter() --> Helper function used to display majors that the user searches for using the 
    searchbar. Majors that match the pattern that the user enters are displayed, while all others are hidden. 
  */
  function majorFilter() {
    var input, filter, ul, li, a, i, txtValue, panel;
    input = document.getElementById("majorInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("MajorList");
    li = ul.getElementsByClassName("accordion");
    panel = ul.getElementsByClassName("panel");
    
    for (i = 0; i < li.length; i++) {
        a = li[i].innerHTML.split(",")[0];
        txtValue = a;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
  }

  /*
    MinorFilter() --> Helper function used to display minors that the user searches for using the 
    searchbar. Minors that match the pattern that the user enters are displayed, while all others are hidden. 
  */
  function minorFilter() {
    var input, filter, ul, li, a, i, txtValue, panel;
    input = document.getElementById("minorInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("MinorList");
    li = ul.getElementsByClassName("accordion");
    panel = ul.getElementsByClassName("panel");
    
    for (i = 0; i < li.length; i++) {
        a = li[i].innerHTML.split(",")[0];
        txtValue = a;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            panel[i].style.display = "";
        } else {
            li[i].style.display = "none";
            panel[i].style.display = "none";
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
                <button onClick={() => {getMajorsAndMinors("2018")}} className="req-button">2018-2019</button>
                <button onClick={() => {getMajorsAndMinors("2019")}} className="req-button">2019-2020</button>
                <button onClick={() => {getMajorsAndMinors("2020")}} className="req-button">2020-2021</button>
            </div>

            <CoolTabs
                tabKey={'1'}
                style={{ width:  1500, height:  650, background:  'white', margin: 20,}}
                tabsHeaderStyle={{height: 100, bottom: 15}}
                activeTabStyle={{ background:  '#926DD6', color:  'white' }}
                unActiveTabStyle={{ background:  'white', color:  'black'}}
                leftContentStyle={{ background:  'white' }}
                rightContentStyle={{ background:  'white' }}

                leftTabTitleStyle={{fontSize: 40}}
                rightTabTitleStyle={{fontSize: 40}}
                
                leftTabTitle={'Majors'}
                rightTabTitle={'Minors'}
                leftContent={
                    <div>      
                        <div id="major-search-container">
                            <h2> Search Majors </h2>
                            <input type="text" id="majorInput" onKeyUp={majorFilter} placeholder="Search for Major" title="Type in a name"></input>
                            <ul id="courses"></ul>
                        </div>
                        <div id="MajorList"> Click on a requirement year to view minors. It can take up to 10 seconds to display. </div> 
                    </div>
                }
                rightContent={
                    <div>
                        <div id="sortingButton">

                        <DropdownButton id="dropdown-basic-button" title="Sort by">
                            <Dropdown.Item onClick={getMinors}>A-Z</Dropdown.Item>

                            <Dropdown.Item onClick={getMinorsRec}>Recommended</Dropdown.Item>
                        </DropdownButton>
                        </div>
                        
                        <div id="minor-search-container">
                        <h2> Search Minors </h2>
                            <input type="text" id="minorInput" onKeyUp={minorFilter} placeholder="Search for Minor" title="Type in a name"></input>
                            <ul id="courses"></ul>
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