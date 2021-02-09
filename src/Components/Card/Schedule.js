import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import SchedulePage from '../../Pages/SchedulePage'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import { fade, makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import Drawer from '@material-ui/core/Drawer';
import CssBaseline from '@material-ui/core/CssBaseline';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import MailIcon from '@material-ui/icons/Mail';
import './Schedule-Style.css';
import TextField from '@material-ui/core/TextField';

//import * as React from 'react';
import Paper from '@material-ui/core/Paper';
import { ViewState } from '@devexpress/dx-react-scheduler';
import {
  Scheduler,
  WeekView,
  Appointments,
} from '@devexpress/dx-react-scheduler-material-ui';

const currentDate = '2018-11-01';
const schedulerData = [
  { startDate: '2018-11-01T09:45', endDate: '2018-11-01T11:00', title: 'Meeting' },
  { startDate: '2018-11-01T12:00', endDate: '2018-11-01T13:30', title: 'Go to a gym' },
];

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex-right',
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginRight: drawerWidth,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
}));

export const Schedule = () => {
  const classes = useStyles();
    return(
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
        <div>
            <h1 id="schedule-title">Semester 1</h1>
        </div>
        <div class="row">
          <div className="col-md-9">
            <Paper>
                <Scheduler
                data={schedulerData}
                >
            {/* <ViewState
                currentDate={currentDate}
            /> */}
            <WeekView
                startDayHour={8}
                endDayHour={22}
            />
                    <Appointments />
                </Scheduler>
            </Paper>
          </div>
          <div id="search-container" className="col-md-3">

              <h3>Search Classes</h3>
              {/* <form id="class-search" action="/api/search" method="POST">
                <input type="search" name="classSearch" id="search-bar" class="col-sm-9" placeholder="Search"/>
                <input type="submit" value="Search" class="col-sm-3">
                </input>
              </form> */}
              <form className={classes.root} noValidate autoComplete="off" method="POST" action="/api/search">
                <div>
                <TextField id="outlined-search" name="outlined-search" label="Search class" type="search" variant="outlined"/>
                </div>
              </form>

          </div>
        </div>
    </div>
    );
}

export default Schedule