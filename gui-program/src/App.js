import React from 'react';
import { DatePicker, Button, Select } from 'antd';
import './App.css';
import fs from 'fs'
import 'antd/dist/antd.css';
import { PythonShell } from 'python-shell';
import process from 'process';
import path from 'path';
import moment from 'moment';
import { CsvToHtmlTable } from 'react-csv-to-table';

const nativeImage = require('electron').nativeImage

const { Option } = Select;
const { RangePicker } = DatePicker;
const dateFormat = 'YYYY/MM/DD';

let pathname = process.cwd()
let workingPath = path.dirname(pathname);
PythonShell.defaultOptions = { scriptPath: workingPath, cwd: workingPath };


function ResultImage({ imagePath }) {
  let image = nativeImage.createFromPath(imagePath)
  return (
    <img src={image.toDataURL()} alt="results" className="result-plot-image" />
  );
}


function ResultCSV({ csvPath }) {
  var contents = fs.readFileSync(csvPath, 'utf8');
  return (
    <CsvToHtmlTable data={contents} csvDelimiter="," tableClassName="table table-striped table-hover" />
  );
}

const app_status = {
  WAIT: 'Wait for input',
  ANALYSING: "Analysing...",
  SHOW_IMAGE_RESULT: "Image Result",
  SHOW_DATA_RESULT: "Dataset Result",
  ERROR: "Error Occured"
}

class App extends React.Component {

  state = {
    status: app_status.WAIT,
    choosedAnalysisFunction: "select",
    displayImagePath: null,
    displayCsvPath: null
  }

  // '/Users/mingtianyang/Documents/Penn State/2019fall/EDSGN460/python program/results/Allegheny_daily_pm25_mean_binned.png'

  analysisFunctions = {
    "BreatheMeter": "BreatheMeter.py",
    "smellPGHStatistics": "SmellPGHStatistics.py",
    "EJAAnalysis": "EJAAnalysis.py",
    "AppUsage": "AppUsage.py",
    "SmellValueAndPM25": "SmellValueAndPM25.py"
  }

  selectFunctionOnChange = (value) => {
    this.setState({ choosedAnalysisFunction: value });
  }

  analyse() {
    let self = this
    let selectedFunction = this.state.choosedAnalysisFunction
    let filePath = this.analysisFunctions[selectedFunction]
    // console.log(filePath)
    this.setState({ status: app_status.ANALYSING, displayImagePath: null, displayCsvPath: null })
    PythonShell.run(filePath, null, function (err, results) {
      if (err) {
        self.setState({ displayImagePath: null, displayCsvPath: null, status: app_status.ERROR })
      } else {
        let resultFilePath = results.pop();
        let ext = path.extname(resultFilePath);
        let fullFilePath = path.join(workingPath, resultFilePath)
        if (ext === '.csv') {
          self.setState({ displayCsvPath: fullFilePath, status: app_status.SHOW_DATA_RESULT })
        } else {
          self.setState({ displayImagePath: fullFilePath, status: app_status.SHOW_IMAGE_RESULT })
          console.log('results', resultFilePath);
        }
      }
    });
  }

  clear() {
    this.setState({ displayCsvPath: null, displayImagePath: null })
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
          <div className="logo_header">
            <img src={'/logo_BreatheProject3-1024x483.png'} id="breatheproject-logo" alt="breatheproject logo" />
            <img src={'/PS_HOR_RGB_2C.png'} id="pennstate-logo" alt="pennstate logo" />

          </div>
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
          <div className="form_section">
            <div className="element-container">
              <RangePicker
                defaultValue={[moment('2016/06/01', dateFormat), moment('2018/12/31', dateFormat)]}
                format={dateFormat}
              />
            </div>
            <div className="element-container">
              <Select
                showSearch
                style={{ width: 400 }}
                placeholder="Please choose an analysis function"
                optionFilterProp="children"
                onChange={this.selectFunctionOnChange}
                filterOption={(input, option) =>
                  option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                }
              >
                <Option value="SmellValueAndPM25">SmellValueAndPM25</Option>
                <Option value="smellPGHStatistics">smellPGHStatistics</Option>
                <Option value="EJAAnalysis">EJAAnalysis</Option>
                <Option value="BreatheMeter">BreatheMeter</Option>
                <Option value="AppUsage">AppUsage</Option>
              </Select>
            </div>

            <div className="element-container">
              <Button type="primary" onClick={() => this.analyse()} disabled={this.state.status === app_status.ANALYSING}>Analyse</Button>
              <Button onClick={() => this.clear()} style={{ marginLeft: "8px" }} disabled={this.state.status === app_status.ANALYSING}>Clear</Button>
            </div>
          </div>



        </header>
        <div>

        </div>
        <div>
          <h2>{this.state.status}</h2>
          {this.state.displayImagePath !== null && (
            <ResultImage imagePath={this.state.displayImagePath} />
          )}

          {this.state.displayCsvPath !== null && (
            <ResultCSV csvPath={this.state.displayCsvPath} />
          )}
        </div>
      </div>
    );
  }
}

export default App;
