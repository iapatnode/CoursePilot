import React, { useEffect, useState } from 'react'
import axios from 'axios'

export const Home = ()=> {
    // Fetch the user information from the home page
    const [isLoading, setLoading] = useState(true);
    const [success, setSuccess] = useState();

    useEffect(() => {
        axios.get("/api/home").then(response => {
            setSuccess(response.data);
            setLoading(false);
        });
    }, []);
    
    if (isLoading) {
        return <div> Loading... </div>
    }
    return(
        <div id="main-content">
            <h1> Schedules </h1>
            <div id="schedule-list-view">
                <h2> Name </h2>
                <p> Put the name of all of the user's schedules here </p>
                <h2> Date Modified </h2> 
                <p> Put the date of last modification to the schedule here </p>
            </div>
            <div id="button-container">
                <button type="button" id="auto-generate"> Auto-Generate Schedule </button>
                <button type="button" id="new-schedule"> Create New Schedule </button>
                <button type="button" id="compare-schedule"> Compare Schedules </button>
            </div>
        </div>     
    );
}

export default Home