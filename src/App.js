import logo from './logo.svg';
import './App.css';
import LoginPage from './Pages/LoginPage'
import SignUpPage from './Pages/SignUpPage'
import HomePage from './Pages/HomePage'
import SchedulePage from './Pages/SchedulePage';
import DegreeReportPage from './Pages/DegreeReportPage';
import MajorsPage from './Pages/MajorsPage';
import ProfilePage from './Pages/ProfilePage';
import { Route, Link, BrowserRouter } from 'react-router-dom'


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Route exact path="/" component={LoginPage}/>
        <Route exact path="/SignUp" component={SignUpPage}/>
        <Route exact path="/Home" component={HomePage}/>
        <Route exact path="/Schedule" component={SchedulePage}/>
        <Route exact path="/Degree" component={DegreeReportPage}/>
        <Route exact path="/Majors" component={MajorsPage}/>
        <Route exact path="/Profile" component={ProfilePage}/>
      </BrowserRouter>
    </div>
  );
}

export default App;
