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
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import Checkbox from '@material-ui/core/Checkbox';

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
  const [state, setState] = React.useState({
    gilad: false,
    jason: false,
    antoine: false,
  });

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const { gilad, jason, antoine } = state;
  const error = [gilad, jason, antoine].filter((v) => v).length !== 2;

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
              <Form className={classes.root} noValidate autocomplete="off" method="POST" action="/api/search">
                <Form.Group>
                    <Form.Control type="search" name="outlined-search" id="outlined-search" placeholder="Enter Course Name/Code"></Form.Control>
                </Form.Group>      
              </Form>

              <FormControl component="fieldset" className={classes.formControl}>
                <FormLabel component="legend">Assign responsibility</FormLabel>
                <FormGroup>
                  <FormControlLabel
                    control={<Checkbox checked={gilad} onChange={handleChange} name="gilad" />}
                    label="Gilad Gray"
                  />
                  <FormControlLabel
                    control={<Checkbox checked={jason} onChange={handleChange} name="jason" />}
                    label="Jason Killian"
                  />
                  <FormControlLabel
                    control={<Checkbox checked={antoine} onChange={handleChange} name="antoine" />}
                    label="Antoine Llorca"
                  />
                </FormGroup>
                <FormHelperText>Be careful</FormHelperText>
              </FormControl>

              <Button  color="primary">
                Save
              </Button>

              <Button  color="red">
                Cancel
              </Button>
          </div>
        </div>
    </div>
    );
}

export default Schedule