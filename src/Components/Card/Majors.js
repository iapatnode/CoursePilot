import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import {DropdownButton, Dropdown} from 'react-bootstrap'

import CoolTabs from 'react-cool-tabs';

//import '@material/react-tab-bar/dist/tab-bar.css';
//import '@material/react-tab-scroller/dist/tab-scroller.css';
//import '@material/react-tab/dist/tab.css';
//import '@material/react-tab-indicator/dist/tab-indicator.css';

//import Tab from '@material/react-tab';
//import TabBar from '@material/react-tab-bar';

export const Majors = () => {

    //const [isLoading, setLoading] = useState(true);
    const isFirst = useRef(true);
    //const [success, setSuccess] = useState(null);
    //const majorCourses = []

    var state = {activeIndex: 0};
 
    var handleActiveIndexUpdate = (activeIndex) => this.setState({activeIndex});
    //var minorList = document.createElement("ul")

    // useEffect(() => {
    //     axios.get("/api/MajorPage").then(response => {
    //         setSuccess(response.data);
            
    //         console.log(response.data)
    //     })
    // }, []);
    var majorList = document.getElementById("MajorList");
    var minorList = document.getElementById("MinorList");
   
    function loadMajor(name) {
        var parent = document.getElementById("MajorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        } 
        
    }
    
    var majorList = document.createElement("ul");
    var recMinorList = document.createElement("ul");
    var minorList = document.createElement("ul");

    // var majorListTwo = document.createElement("ul");
    // var majorListThree = document.createElement("ul");
    // var majorListFour = document.createElement("ul");

    // var minorListTwo = document.createElement("ul");
    // var minorListThree = document.createElement("ul");
    // var minorListFour = document.createElement("ul");

    // var recMinorListTwo = document.createElement("ul");
    // var recMinorListThree = document.createElement("ul");
    // var recMinorListFour = document.createElement("ul");
    
    var majors = [];
    if(isFirst.current) {
        axios.get('http://localhost:5000/api/getAllMajorsAndMinors').then((response) => {
            const firstResponse = response.data["2017"];
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
                var classesRequiredString = "Requirements: "
                requirements.forEach(requirement => {
                    var currentRequirementString = "";
                    currentRequirementString += requirement["numHoursRequired"] + " hours from ";
                    requirement["courseList"].forEach(course => {
                        currentRequirementString += course + ", ";
                    })
                    currentRequirementString += "; ";
                    classesRequiredString += currentRequirementString;
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
                        recMinorList.insertBefore(moreInformationNode, para.nextSibling);
                    }
                });
                para.appendChild(tag);
                recMinorList.appendChild(para);
            });



            // const secondResponse = response.data["2018"];
            // const majorResponseTwo = secondResponse["majors"];
            // const minorResponseTwo = secondResponse["minors"];
            // const recMinorResponseTwo = secondResponse["recMinors"]
            // majorResponseTwo.forEach(element => {
            //     majors.push(element);
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("a");
            //     tag.setAttribute("class", "majorButton")
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     //tag.addEventListener("click", this.loadMajor(name));
            //     tag.addEventListener("click", function() {
            //            if (para.nextSibling != null) {
            //                majorListTwo.insertBefore(moreInformationNode, para.nextSibling);
            //            }
            //        });
            //     para.appendChild(tag);
            //     majorListTwo.appendChild(para);
            // });
            // minorResponseTwo.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);

            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //        minorListTwo.insertBefore(moreInformationNode, para.nextSibling);
            //    }
            //});
            //     para.appendChild(tag);
            //     minorListTwo.appendChild(para);
            // });
            // recMinorResponseTwo.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //        recMinorListTwo.insertBefore(moreInformationNode, para.nextSibling);
            //    }
            //});
            //     para.appendChild(tag);
            //     recMinorListTwo.appendChild(para);
            // });


            // const thirdResponse = response.data["2019"];
            // const majorResponseThree = thirdResponse["majors"];
            // const minorResponseThree = thirdResponse["minors"];
            // const recMinorResponseThree = thirdResponse["recMinors"]
            // majorResponseThree.forEach(element => {
            //     majors.push(element);
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("a");
            //     tag.setAttribute("class", "majorButton")
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     //tag.addEventListener("click", this.loadMajor(name));
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //        majorsListThree.insertBefore(moreInformationNode, para.nextSibling);
            //    }
            //});
            //     para.appendChild(tag);
            //     majorListThree.appendChild(para);
            // });
            // minorResponseThree.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);

            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //        minorsListThree.insertBefore(moreInformationNode, para.nextSibling);
            //    }
            //});
            //     para.appendChild(tag);
            //     minorListThree.appendChild(para);
            // });
            // recMinorResponseThree.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //        recMinorsListThree.insertBefore(moreInformationNode, para.nextSibling);
            //    }
            //});
            //     para.appendChild(tag);
            //     recMinorListThree.appendChild(para);
            // });


            // const fourthResponse = response.data["2020"];
            // const majorResponseFour = fourthResponse["majors"];
            // const minorResponseFour = fourthResponse["minors"];
            // const recMinorResponseFour = fourthResponse["recMinors"]
            // majorResponseFour.forEach(element => {
            //     majors.push(element);
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("a");
            //     tag.setAttribute("class", "majorButton")
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     //tag.addEventListener("click", this.loadMajor(name));
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //            majorListFour.insertBefore(moreInformationNode, para.nextSibling);
            //        }});
            //     para.appendChild(tag);
            //     majorListFour.appendChild(para);
            // });
            // minorResponseFour.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);

            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //            minorListFour.insertBefore(moreInformationNode, para.nextSibling);
            //        }});
            //     para.appendChild(tag);
            //     minorListFour.appendChild(para);
            // });
            // recMinorResponseFour.forEach(element => {
            //     var name = element["name"];
            //     var requirements = element["requiredClasses"];
            //     var classesRequiredString = "Requirements: "
            //     requirements.forEach(requirement => {
            //         var currentRequirementString = "";
            //         currentRequirementString += requirement["numHoursRequired"] + " hours from ";
            //         requirement["courseList"].forEach(course => {
            //             currentRequirementString += course + ", ";
            //         })
            //         currentRequirementString += "; ";
            //         classesRequiredString += currentRequirementString;
            //     })
            //     var para = document.createElement("li");
            //     var tag = document.createElement("button");
            //     tag.setAttribute("id", "minorButton");
            //     para.setAttribute("id", name);
            //     var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
            //     var moreInformationNode = document.createTextNode(classesRequiredString);
            //     tag.appendChild(node);
            //     tag.addEventListener("click", function() {
            //    if (para.nextSibling != null) {
            //            recMinorListFour.insertBefore(moreInformationNode, para.nextSibling);
            //        }});
            //     para.appendChild(tag);
            //     recMinorListFour.appendChild(para);
            // });
        })
    }

    
    // if(isFirstRun.current) {
    //     axios.get('http://localhost:5000/api/getMinors').then((response) => {
    //         console.log(response.data);
    //         response.data.forEach(element => {
    //             var name = element["name"];
    //             var para = document.createElement("li");
    //             var tag = document.createElement("a");
    //             para.setAttribute("id", name);
    //             var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
    //             tag.appendChild(node);
    //             para.appendChild(tag);
    //             minorList.appendChild(para);
    //         });
    //     })
    // }
     
    // if (isFirstRun.current) {
    //     axios.get('http://localhost:5000/api/getMinorsRec').then((response) => {
    //             console.log(response.data);
    //             response.data.forEach(element => {
    //                 var name = element["name"];
    //                 var para = document.createElement("li");
    //                 var tag = document.createElement("a");
    //                 para.setAttribute("id", name);
    //                 var node = document.createTextNode(name);
    //                 tag.appendChild(node);
    //                 para.appendChild(tag);
    //                 recMinorList.appendChild(para);
    //             });
    //         })
    // }

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
    function getMinorsTwo() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(minorList);
    }

    function getMinorsRecTwo() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(recMinorList);
    }

    function getMajorsTwo() {
        var parent = document.getElementById("MajorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        } 
        parent.appendChild(majorList);
    }

    function getMinorsThree() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(minorList);
    }

    function getMinorsRecThree() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(recMinorList);
    }

    function getMajorsThree() {
        var parent = document.getElementById("MajorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        } 
        parent.appendChild(majorList);
    }

    function getMinorsFour() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(minorList);
    }

    function getMinorsRecFour() {
        var parent = document.getElementById("MinorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(recMinorList);
    }

    function getMajorsFour() {
        var parent = document.getElementById("MajorList");
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        } 
        parent.appendChild(majorList);
    }

    function getMajorsAndMinors() {
        getMinors();
        getMajors();
    }
    function getMajorsAndMinorsTwo() {
        getMinorsTwo();
        getMajorsTwo();
    }
    function getMajorsAndMinorsThree() {
        getMinorsThree();
        getMajorsThree();
    }
    function getMajorsAndMinorsFour() {
        getMinorsFour();
        getMajorsFour();
    }

    function componentDidMount() {
        getMinors();
        getMajors();
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
        <div class="req-content">
            <div class="reqYear" className="req-buttons">
                <div id="columnTitle" >Requirement Year</div>
                <button onClick={getMajorsAndMinors} className="req-button">2017-2018</button>
                <button onClick={getMajorsAndMinors} className="req-button">2018-2019</button>
                <button onClick={getMajorsAndMinors} className="req-button">2019-2020</button>
                <button onClick={getMajorsAndMinors} className="req-button">2020-2021</button>
            </div>

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
                    <div id="MajorList"> Click on a requirement year to view minors. </div> 
                }
                rightContent={
                    <div>
                        <div id="sortingButton">
                            <DropdownButton id="dropdown-basic-button" title="Sort by">
                                <Dropdown.Item onClick={getMinors}>A-Z</Dropdown.Item>
                                <Dropdown.Item onClick={getMinorsRec}>Recommended</Dropdown.Item>
                            </DropdownButton>
                        </div>

                <div id="MinorList"> Click on a requirement year to view minors. </div> 
                </div>
                }
                
            />


            </div>
            </div>

    );
}


export default Majors





