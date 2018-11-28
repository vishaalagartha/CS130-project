import React, { Component } from 'react';
import DatePicker from "react-datepicker";
import moment from "moment";

import './App.css';
import "react-datepicker/dist/react-datepicker.css";

const axios = require('axios');

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      subreddit: "",
      startDate: moment(),
      endDate: moment(),
      words: {}
    };
  }

  // componentDidMount() {
  //   axios.get('https://api.github.com/users/kelvinlzhang')
  //   .then(function(response){
  //     console.log(response.data); // ex.: { user: 'Your User'}
  //     console.log(response.status); // ex.: 200
  //   });  
  // }

  onChangeSubreddit = (e) => {
    this.setState({ subreddit: e.target.value });
  }

  onChangeStartDate = (date) => {
    this.setState({ startDate: date });
    console.log(this.state.startDate.unix());
  }
  
  onChangeEndDate= (date) => {
    this.setState({ endDate: date });
    console.log(this.state.endDate.unix());
  }

  onSubmit = (e) => {
    let data = JSON.stringify({
      subreddit: this.state.subreddit,
      start: this.state.startDate.unix(),
      end: this.state.endDate.unix()
  })
    // axios.get('https://api.github.com/users/kelvinlzhang')
    // .then(function(response){
    //   console.log(response.data); // ex.: { user: 'Your User'}
    //   console.log(response.status); // ex.: 200
    // })  
    axios.post('http://127.0.0.1:8080', data, {
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
      }
    })
    // return axios('http://127.0.0.1:8080', {
    //   method: 'POST',
    //   headers: {
    //     'content-type': 'application/json',
    //   },
    //   data: {
    //     subreddit: this.state.subreddit,
    //     start: this.state.startDate.unix(),
    //     end: this.state.endDate.unix()
    //   }
    // })
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
      </div>
    );
  }
}

export default App;
