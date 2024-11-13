// import logo from "./logo.svg";
import "./App.css";

import React from "react";

// SOLUTION IS HERE

export const EggList = (props) => {
  const list = props.eggs.map((egg, index) => (
    <EasterEgg key={index} name={egg}></EasterEgg>
  ));
  return <ul>{list}</ul>
};

export const EasterEgg = (props) => {
  return <li>{props.name}</li>
};

// TESTS ARE HERE

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <EggList eggs={["Lindt", "Cadbury", "Milka", "Maltesers"]} />
      </header>
    </div>
  );
}

export default App;
