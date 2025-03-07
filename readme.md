# Screenshot to PDF

A simple application that takes periodic screenshots and compiles them into a PDF document. This tool consists of a Python backend server and a Chrome extension for easy control.<br>
NOTE: Incase of an early interrupt before duration, server needs to be stopped too to save the PDF automatically. It adds the functionality of pause/resume as if a new session of snapshots is launched it will append all the snapshots alltogether since the server was launched and saves in one PDF of final output.

## Features

- Take screenshots at customizable intervals
- Set specific duration for capturing screenshots
- Automatically compile screenshots into a PDF
- Control via Chrome extension or command line
- Stop the program any time before duration according to your need
## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
  Or if you already have python installed run the `install_dependencies.bat` file in case of windows OS
  
2. Install the Chrome extension:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the extension folder
   
## Usage

### Server
Run the server:
```
python server.py
```
Or run `run_server.bat` file

### Chrome Extension
1. Click the extension icon
2. Set your desired screenshot interval and duration
3. Click "Start Capturing Screenshots"
4. Use "Stop Capture" to end the process early

### Command Line
You can also use the tool directly from the command line:
```
python main.py -r 10 -d 1800 -o myPDFs -n screenshots.pdf
```

Arguments:
- `-r, --rate`: Screenshot interval in seconds (default: 10)
- `-d, --duration`: Total duration in seconds (default: 1800, i.e., 30 minutes)
- `-o, --output`: Output directory for PDF file (default: myPDFs)
- `-n, --name`: Custom name for the PDF file
