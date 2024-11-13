import logo from "./logo.svg";
import "./App.css";
import React from "react";

export class States extends React.Component {
  constructor(props) {
    super();
    this.state = {
      united: (props.united),
    };
  }

  unite() {
    this.setState({
      united: false,
    });
  }

  render() {
    let message = this.state.united
      ? "Code for everyone"
      : "Make America code again";
    return <div className="status">{message}</div>;
  }
}

function Root(props) {
  let united = true;
  const onClick = () => {
    united = !united;
  }
  return (
    <div>
      <button onClick={onClick}>Change state</button>
      <States united={united}></States>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Root></Root>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
