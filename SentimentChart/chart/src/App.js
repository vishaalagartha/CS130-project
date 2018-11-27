import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Chart from './components/Chart';
import data from "./components/data.json";

class App extends Component {
  constructor(){
    super();
    this.state = {
      chartData:{},
      word: data.words[0].name,
      x: data.words[0].x,
      y: data.words[0].y,
      s: data.words[0].s,
    }
  }

  componentWillMount(){
    this.getChartData();
  }

  getChartData(){

    this.setState({
      chartData:{
        labels: this.state.x,
        datasets:[
          {
            label: this.state.word,
            data:this.state.y,
            backgroundColor:this.state.s,
          }
        ]
      }
    });
  }

  render() {
    return (
      <div className="App">
        <Chart chartData={this.state.chartData} word={this.state.word} legendPosition="bottom"/>
      </div>
    );
  }
}

export default App;
