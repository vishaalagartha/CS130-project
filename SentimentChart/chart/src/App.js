import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Chart from './components/Chart';
import data from "./components/data.json";

//REFERENCE FOR JSON PURPOSES:
// {'score': vs, 'vote': vote, 'timestamp': timestamp, 'word': word}

class App extends Component {
  constructor(){
    super();
    this.state = {
      chartData:{},
      word: data.words[0].word, // this.props .. passed down from WordCloud
      x: data.words[0].timestamps,
      y: data.words[0].y, //need to calculate
      s: data.words[0].score, //score
    }
  }

  componentWillMount(){
    this.getChartData();
  }

  getChartData(){

    // var ts = Math.round((new Date()).getTime() / 1000);
    //
    // console.log('hello', Date.now());




    //TIME RANGE DIVIDING

    var ts = this.state.x;
    var date = [];
    var sent = this.state.s;
    date.length = ts.length/2;






    //SENTIMENT COLOR ASSIGNMENT
    var sentiments = this.state.s;
    var colors = [];
    colors.length = sentiments.length;

    var i;
    for(i = 0; i < sentiments.length; i++){
      if(sentiments[i] <= -0.8){
        colors[i] = "rgba(92, 10, 10, 1)";
      }
      else if(sentiments[i] > -0.8 && sentiments[i] <= -0.6){
        colors[i] = "rgba(137, 15, 15, 1)";
      }
      else if(sentiments[i] > -0.6 && sentiments[i] <= -0.4){
          colors[i] = "rgba(201, 16, 16, 1)";
      }
      else if(sentiments[i] > -0.4 && sentiments[i] <= -0.2){
        colors[i] = "rgba(242, 140, 140, 1)";
      }
      else if(sentiments[i] > -0.2 && sentiments[i] <= 0){
          colors[i] = "rgba(255, 230, 230, 1)";
      }
      else if(sentiments[i] > 0 && sentiments[i] <= 0.2){
        colors[i] = "rgba(159, 237, 120, 1)";
      }
      else if(sentiments[i] > 0.2 && sentiments[i] <= 0.4){
          colors[i] = "rgba(95, 224, 31, 1)";
      }
      else if(sentiments[i] > 0.4 && sentiments[i] <= 0.6){
        colors[i] = "rgba(56, 132, 18, 1)";
      }
      else if(sentiments[i] > 0.6 && sentiments[i] <= 0.8){
          colors[i] = "rgba(25, 73, 1, 1)";
      }
      else if(sentiments[i] > 0.8 && sentiments[i] <= 1){
        colors[i] = "rgba(17, 50, 1, 1)";
      }


    }

    this.setState({
      chartData:{
        labels: this.state.x,
        datasets:[
          {
            label: this.state.word,
            data:this.state.y,
            backgroundColor: colors,
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
