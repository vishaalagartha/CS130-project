import React, { Component } from 'react';
import DatePicker from "react-datepicker";
import sketch from './sketch'
import p5 from 'p5'
import './App.css';
import "react-datepicker/dist/react-datepicker.css";

const axios = require('axios');

class P5Wrapper extends React.Component {
  componentDidMount() {
    const { sketch, ...rest } = this.props;
    this.canvas = new p5(sketch(rest), this.wrapper);
  }

  componentWillReceiveProps(newProps) {
    const { sketch, ...rest } = newProps;

    if (this.props.sketch !== newProps.sketch) {
      this.canvas.remove();
      this.canvas = new p5(newProps.sketch(rest), this.wrapper);
    }

    if (typeof this.canvas.onNewProps === "function") {
      this.canvas.onNewProps(newProps);
    }
  }

  componentWillUnmount() {
    this.canvas.remove();
  }

  render() {
    return <div ref={(wrapper) => this.wrapper = wrapper} />;
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      subreddit: "",
      startDate: new Date(),
      endDate: new Date(),
      words: {}
    };

    this.onChangeSubreddit = this.onChangeSubreddit.bind(this);
    this.onChangeStartDate = this.onChangeStartDate.bind(this);
    this.onChangeEndDate = this.onChangeEndDate.bind(this);
  }

  onChangeSubreddit = (e) => {
    this.setState({ subreddit: e.target.value });
  }

  onChangeStartDate = (date) => {
    this.setState({ startDate: date });
    console.log((this.state.startDate.getTime() / 1000).toFixed(0));
  }
  
  onChangeEndDate= (date) => {
    this.setState({ endDate: date });
    console.log((this.state.startDate.getTime() / 1000).toFixed(0));
  }

  onSubmit = (e) => {
    e.preventDefault();

    let data = JSON.stringify({
      subreddit: this.state.subreddit,
      start: parseInt((this.state.startDate.getTime() / 1000).toFixed(0)),
      end: parseInt((this.state.startDate.getTime() / 1000).toFixed(0))
    })
    
    axios.post('http://127.0.0.1:8080', data, {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
      },
      timeout: 60000
    })
    .then((res) => res.json())
    .then((data) => {
      this.setState({
        words: data
      });
      console.log(data)
    });
  }

  render() {
    return (
      <div className="App">
        <form onSubmit={this.onSubmit}>
          <input value={this.state.subreddit} onChange={this.onChangeSubreddit} />
          <DatePicker
            selected={this.state.startDate}
            onChange={this.onChangeStartDate}
          />
          <DatePicker
            selected={this.state.endDate}
            onChange={this.onChangeEndDate}
          />
          <button>Submit</button>
        </form>
        <P5Wrapper sketch={sketch}/>
      </div>
    );
  }
}

export default App;
