import logo from './logo.svg';
import './App.css';
import LoginPage from './Pages/LoginPage'
import SignUpPage from './Pages/SignUpPage'
import HomePage from './Pages/HomePage'
import { Route, Link, BrowserRouter } from 'react-router-dom'
import SchedulePage from './Pages/SchedulePage';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Route exact path="/" component={LoginPage}/>
        <Route exact path="/SignUp" component={SignUpPage}/>
        <Route exact path="/Home" component={HomePage}/>
        <Route exact path="/Schedule" component={SchedulePage}/>
      </BrowserRouter>
    </div>
  );
}

export default App;
