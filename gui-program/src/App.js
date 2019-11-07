import React from 'react';
import { DatePicker, Button, Select } from 'antd';
import './App.css';
import 'antd/dist/antd.css';
import { PythonShell } from 'python-shell';
import { throws } from 'assert';
import process from 'process';
import path from 'path';
import moment from 'moment';
const nativeImage = require('electron').nativeImage

const { Option } = Select;
const { MonthPicker, RangePicker } = DatePicker;
const dateFormat = 'YYYY/MM/DD';
const monthFormat = 'YYYY/MM';
const dateFormatList = ['DD/MM/YYYY', 'DD/MM/YY'];

let pathname = process.cwd()
let workingPath = path.dirname(pathname);
PythonShell.defaultOptions = { scriptPath: workingPath, cwd: workingPath };


function ResultImage({ imagePath }) {
  let image = nativeImage.createFromPath(imagePath)
  return (
    <img src={image.toDataURL()} className="result-plot-image" />
  );
}

class App extends React.Component {

  state = {
    status: "Wait for input",
    choosedAnalysisFunction: "select",
    displayImagePath: null
  }

  // '/Users/mingtianyang/Documents/Penn State/2019fall/EDSGN460/python program/results/Allegheny_daily_pm25_mean_binned.png'

  analysisFunctions = {
    "smellReport": "SmellReport.py",
    "BreatheMeter": "BreatheMeter.py",
    "smellPGHStatistics": "SmellPGHStatistics.py",
    "EJAAnalysis": "EJAAnalysis.py",
    "AppUsage": "AppUsage.py"
  }

  selectFunctionOnChange = (value) => {
    console.log("change")
    this.setState({ choosedAnalysisFunction: value });
  }

  test() {
    let self = this
    let selectedFunction = this.state.choosedAnalysisFunction
    let filePath = this.analysisFunctions[selectedFunction]
    console.log(filePath)
    this.setState({status: "Analysing...", displayImagePath: null})
    PythonShell.run(filePath, null, function (err, results) {
      if (err) throw err;
      let resultFilePath = results.pop();
      let imageFilePath = path.join(workingPath, resultFilePath)
      self.setState({ displayImagePath: imageFilePath, status: "Result" })
      console.log('results', resultFilePath);
    });
  }

  imagePathToDataURL = function (imagePath) {
    console.log()
    let image = nativeImage.createFromPath(imagePath)
    return image.toDataURL
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          {/* <img src={logo} className="App-logo" alt="logo" />
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
          </a> */}
          <div className="element-container">
            <RangePicker
              defaultValue={[moment('2016/06/01', dateFormat), moment('2018/12/31', dateFormat)]}
              format={dateFormat}
            />
          </div>
          <div className="element-container">

            <Select
              showSearch
              style={{ width: 200 }}
              placeholder="Please choose an analysis function"
              optionFilterProp="children"
              onChange={this.selectFunctionOnChange}
              filterOption={(input, option) =>
                option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              <Option value="smellReport">smellReport</Option>

              <Option value="smellPGHStatistics">smellPGHStatistics</Option>
              <Option value="EJAAnalysis">EJAAnalysis</Option>
              <Option value="BreatheMeter">BreatheMeter</Option>
              <Option value="AppUsage">AppUsage</Option>
            </Select>
          </div>

          <div className="element-container">
            <Button type="primary" onClick={() => this.test()}>Analyse</Button>
          </div>

        </header>
        <div>

        </div>
        <div>
          <h2>{this.state.status}</h2>
          {this.state.displayImagePath !== null && (
            <ResultImage imagePath={this.state.displayImagePath} />
          )}
        </div>
      </div>
    );
  }
}

export default App;
