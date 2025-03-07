#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import subprocess
import os
import sys
import signal
import psutil
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Active capture process
active_process = None
process_pid = None

@app.route('/start_capture', methods=['POST'])
def start_capture():
    global active_process, process_pid
    
    # If a capture is already running, don't start another
    if active_process and active_process.is_alive():
        return jsonify({
            'success': False,
            'message': 'A screenshot capture is already in progress'
        })
    
    # Get parameters from request
    data = request.json
    rate = data.get('rate', 10)
    duration = data.get('duration', 1800)
    output = data.get('output', 'myPDFs')
    name = data.get('name')
    
    # Build command for running main.py
    cmd = [sys.executable, os.path.join(script_dir, 'main.py')]
    cmd.extend(['-r', str(rate)])
    cmd.extend(['-d', str(duration)])
    cmd.extend(['-o', output])
    if name:
        cmd.extend(['-n', name])
    
    # Start screenshot process in a separate thread
    def run_process():
        global active_process, process_pid
        try:
            proc = subprocess.Popen(cmd)
            process_pid = proc.pid
            proc.wait()
        finally:
            active_process = None
            process_pid = None
    
    active_process = threading.Thread(target=run_process)
    active_process.start()
    
    return jsonify({
        'success': True,
        'message': 'Screenshot capture started',
        'params': {
            'rate': rate,
            'duration': duration,
            'output': output,
            'name': name
        }
    })

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    global active_process, process_pid
    
    if not active_process or not active_process.is_alive():
        return jsonify({
            'success': False,
            'message': 'No screenshot capture is currently running'
        })
    
    if process_pid:
        try:
            # Send keyboard interrupt signal (CTRL+C) to the process
            # This allows the main.py script to handle the termination gracefully
            # and create the PDF with the screenshots captured so far
            
            # Get process object
            parent = psutil.Process(process_pid)
            
            # On Windows, we need a different approach since CTRL+C is not as simple
            if os.name == 'nt':  # Windows
                # For Windows, inject a CTRL+C event
                print(f"Sending CTRL+C signal to process {process_pid}")
                os.kill(process_pid, signal.CTRL_C_EVENT)
            else:  # macOS, Linux
                # For Unix systems, send SIGINT (equivalent to CTRL+C)
                print(f"Sending SIGINT signal to process {process_pid}")
                parent.send_signal(signal.SIGINT)
            
            # Wait for a few seconds to allow the process to finish creating the PDF
            time.sleep(5)
            
            # Check if the process is still running after waiting
            if parent.is_running() and parent.status() != psutil.STATUS_ZOMBIE:
                print(f"Process {process_pid} is still running, terminating forcefully")
                # If still running, terminate forcefully
                parent.terminate()
                
                # Wait for process to terminate
                parent.wait(timeout=3)
                
                # If still running after termination attempt, kill it
                if parent.is_running():
                    parent.kill()
            
            return jsonify({
                'success': True,
                'message': 'Screenshot capture stopped and PDF saved successfully'
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            return jsonify({
                'success': False,
                'message': f'Error stopping process: {str(e)}'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Process PID not available'
        })

@app.route('/status', methods=['GET'])
def status():
    if active_process and active_process.is_alive():
        return jsonify({
            'status': 'active',
            'message': 'Screenshot capture is in progress'
        })
    else:
        return jsonify({
            'status': 'inactive',
            'message': 'No screenshot capture in progress'
        })

if __name__ == '__main__':
    print("Screenshot to PDF server is running at http://localhost:5000")
    print("The Chrome extension will connect to this server to start captures.")
    print("Press Ctrl+C to shut down the server.")
    app.run(host='localhost', port=5000)