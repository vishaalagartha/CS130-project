import React, {Component} from 'react';
import {Bar, Line, Pie} from 'react-chartjs-2';
// import data from './data.json';

const x = ['January 2017', 'February 2017', 'March 2017', 'April 2017', 'May 2017', 'June 2017', 'July 2017', 'August 2017'];
const y = [123, 115, 120, 153, 106, 132, 143, 152];

const sent = [1, 2, 3, 4, 5, 6, 7, 8];

  //have like a switch statement and pre-determine sentiment color range


class Chart extends Component{

  constructor(props){
    super(props);
    this.state = {
      chartData: {

          labels: x,
          datasets:[{


            label:'frequency',

            data: y,

            backgroundColor:[
              'rgba(137, 15, 15, 1)',
              'rgba(201, 16, 16, 1)',
              'rgba(242, 140, 140, 1)',
              'rgba(182, 244, 151, 1)',
              'rgba(122, 188, 88, 1)',
              'rgba(71, 145, 34, 1)',
              'rgba(56, 132, 18, 1)',
              'rgba(25, 73, 1, 1)',

            ],
            borderWidth:1,
            borderColor:'#777',
            hoverBorderWidth:3,
            hoverBorderColor:'#000',


          }]

      }
    }
  }

  render(){
    return (
      //JSX but pretty much HTML
      <div className="chart">
        <Bar
          data={this.state.chartData}
          options={{
            title:{
              display:true,
              text: 'potato',
              fontSize: 25
            },
            legend:{
              display: true,
              position: 'right'
            },
            scales :{
              xAxes: [{
                barPercentage: 1,
                categoryPercentage: 1
            }]
          }
          }}
        />
      </div>
    )
  }

}

export default Chart;
