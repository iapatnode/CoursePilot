import React, { useState, useEffect } from 'react'
import { SignUp } from '../Components/Card/SignUp'

export const SignUpPage = ()=> {

    const [name, setName] = useState([])

    useEffect(()=> {
        fetch('/SignUp/').then(response => {
            if(response.ok) {
                return response.json()
            }
        }).then(data => console.log(data))
    }, [])

    return(
        <>
            <SignUp/>
        </>
    )
}

export default SignUpPage