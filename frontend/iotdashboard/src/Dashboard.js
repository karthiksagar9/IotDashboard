// TemperatureGraph.js
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import { CategoryScale, Chart, LinearScale,PointElement, LineElement} from "chart.js";


import Slider from 'react-rangeslider';
import 'react-rangeslider/lib/index.css';

Chart.register(CategoryScale);

Chart.register(LinearScale);
Chart.register(LineElement);

Chart.register(PointElement);

const Dashboard = () => {
  const [value,setValue]=useState(5);
  const [graphData, setGraphData] = useState({
    labels: [],
    datasets: [],
    
  });
  const time_series_url = process.env.REACT_APP_TIME_SERIES_URL;
  const getGraphData=()=>{
    axios.get(time_series_url+'?interval='+value)
    .then(response => {
      const result = JSON.parse(response.data);
      const labels = result.map(entry => new Date(entry.timestamp).toLocaleString());
      const datasets = [{
        label: 'Average Temperatures (${value} intervals)',
        data: result.map(entry => entry.temperature),
        fill: false,
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      }];

      setGraphData({ labels, datasets });
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
  }

  useEffect(() => {
    
    getGraphData();
    setInterval(getGraphData,60*1000);
    setValue(value);
  }, []);

 

  const handleChange = (value) => {
    setValue(value);
    getGraphData();
  };
  return (
    <div class="row" style={{"padding":20,"height":500,"width":800}}>
        
      <h2>Temperature Time Series Graph</h2>
      <Line data={graphData} />
      <div><Slider
              min={5}
              max={100}
              value={value}
              step={5}
              orientation='horizontal'
              onChange={handleChange}
            />
            <div className='value'>{value}</div>
          </div> 
    </div>
  );
};

export default Dashboard;
