import logo from './logo.svg';
import './App.css';
import Login from './Containers/Login'
import SignUp from './Containers/SignUp'
import { Route, Link } from 'react-router-dom'

function App() {
  return (
    <div className="App">
      <Route exact path="/" component={Login}/>
      <Route exact path="/SignUp" component={SignUp}/>
    </div>
  );
}

export default App;
