import React, { useEffect, useState } from 'react'
import axios from 'axios'

export const Home = ()=> {
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
        <div>
            <h1> Data Received From Server: </h1>
            <ul>
                <li>{success.name}</li>
                <li>{success.email}</li>
                <li>{success.graduation_year}</li>
            </ul>
        </div>     
    );
}

export default Home