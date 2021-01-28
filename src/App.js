import logo from './logo.svg';
import './App.css';
import LoginPage from './Pages/LoginPage'
import SignUpPage from './Pages/SignUpPage'
import { Route, Link, BrowserRouter } from 'react-router-dom'

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Route exact path="/" component={LoginPage}/>
        <Route exact path="/SignUp/" component={SignUpPage}/>
      </BrowserRouter>
    </div>
  );
}

export default App;
