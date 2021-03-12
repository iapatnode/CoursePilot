import React, { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import '../static/styles/Majors-Style.css'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'

import {Tabs, Tab} from 'react-bootstrap-tabs'

function MinorList() {
    var minorList = document.createElement("ul");
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
            minorList.appendChild(para);
        });
    });
    return minorList;
}
export default MinorList;