import React from 'react'
import Schedule from '../Components/Card/Schedule'
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';
import { purple } from '@material-ui/core/colors';


const theme = createMuiTheme({
    palette: {
      primary: {
        // Purple and green play nicely together.
        main: purple[500],
      },
      secondary: {
        // This is green.A700 as hex.
        main: '#11cb5f',
      },
    },
  });

export const SchedulePage = ()=> {

    return(
        <ThemeProvider theme={theme}>
            <>
                <Schedule/>
            </>
        </ThemeProvider>
    )
}

export default SchedulePage