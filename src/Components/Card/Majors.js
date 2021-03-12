import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import {DropdownButton, Dropdown} from 'react-bootstrap'

import {Tabs, Tab} from 'react-bootstrap-tabs'

//import '@material/react-tab-bar/dist/tab-bar.css';
//import '@material/react-tab-scroller/dist/tab-scroller.css';
//import '@material/react-tab/dist/tab.css';
//import '@material/react-tab-indicator/dist/tab-indicator.css';

//import Tab from '@material/react-tab';
//import TabBar from '@material/react-tab-bar';

export const Majors = () => {

    const [isLoading, setLoading] = useState(true);
    const isFirstRun = useRef(true);
    const [success, setSuccess] = useState(null);
    const majorCourses = []

    var state = {activeIndex: 0};
 
    var handleActiveIndexUpdate = (activeIndex) => this.setState({activeIndex});
    //var minorList = document.createElement("ul")

    // useEffect(() => {
    //     axios.get("/api/MajorPage").then(response => {
    //         setSuccess(response.data);
            
    //         console.log(response.data)
    //     })
    // }, []);

    //console.log(success.data)
    //success.major.foreach(element => majorCourses.push({"value": element, "label": element}))
    var minorList = document.createElement("ul");
    if(isFirstRun.current) {
        axios.get('http://localhost:5000/api/getMinors').then((response) => {
            console.log(response.data);
            response.data.forEach(element => {
                var name = element["name"];
                var para = document.createElement("li");
                var tag = document.createElement("a");
                para.setAttribute("id", name);
                var node = document.createTextNode(name + ", Required Hours: " + element["hoursRemaining"]);
                tag.appendChild(node);
                para.appendChild(tag);
                minorList.appendChild(para);
            });
        })
    }
     var recMinorList = document.createElement("ul");
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
        var parent = document.getElementById("MinorList")
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(minorList);
    }

    function getMinorsRec() {
        var parent = document.getElementById("MinorList")
        if (parent.hasChildNodes()) {
            parent.removeChild(parent.firstChild);
        }
        
       parent.appendChild(recMinorList);
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
            <div class="reqYear">
                Requirement Year
                <button onClick={getMinors}>2017-2018</button>
                <button onClick={getMinors}>2018-2019</button>
                <button onClick={getMinors}>2019-2020</button>
                <button onClick={getMinors}>2020-2021</button>
            </div>
            <div class="tab">
                <Tabs>
                    <Tab label="Majors">Majors</Tab>
                    <Tab label="Minors">Minors
                        <button onClick={getMinors}>Click to show Minors</button>
                        <DropdownButton id="dropdown-basic-button" title="Sort by">
                            <Dropdown.Item onClick={getMinors}>A-Z</Dropdown.Item>
                            <Dropdown.Item onClick={getMinorsRec}>Recommended</Dropdown.Item>
                        </DropdownButton>
                        <div id="MinorList">
                            
                        </div> 
                    
                    </Tab>
                </Tabs>
            </div>
            <div>
                
            </div>



            </div>
        </div>


    );
}


export default Majors





