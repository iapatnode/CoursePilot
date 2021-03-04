import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

//import {Tabs, Tab} from 'react-bootstrap-tabs'

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

    // useEffect(() => {
    //     axios.get("/api/MajorPage").then(response => {
    //         setSuccess(response.data);
            
    //         console.log(response.data)
    //     })
    // }, []);

    //console.log(success.data)
    //success.major.foreach(element => majorCourses.push({"value": element, "label": element}))
    
    axios.get('http://localhost:5000/api/getMinors').then((response) => {
        console.log(response.data);
        response.data.forEach(element => {
            var name = element["name"];
            var para = document.createElement("li");
            var tag = document.createElement("a");
            para.setAttribute("id", name);
            var node = document.createTextNode(name);
            tag.appendChild(node);
            para.appendChild(tag);
            var element = document.getElementById("MinorList");
            element.appendChild(para);
        });
    })

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
            </div>
            <div class="tab">
                
            </div>
            <div>
                
            </div>



        </div>
        
        </div>
    );
}


export default Majors

