document.addEventListener('DOMContentLoaded', function() {
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  const statusMsg = document.getElementById('statusMsg');
  
  // Check the status when popup opens
  checkStatus();
  
  startButton.addEventListener('click', function() {
    // Get form values
    const rate = document.getElementById('rate').value;
    const durationMinutes = document.getElementById('duration').value;
    const duration = durationMinutes * 60; // Convert to seconds
    const output = document.getElementById('output').value;
    const name = document.getElementById('name').value;
    
    // Construct API request to local server
    const url = 'http://localhost:5000/start_capture';
    const params = {
      rate: rate,
      duration: duration,
      output: output,
      name: name || null
    };
    
    // Show loading status
    statusMsg.textContent = 'Starting screenshot capture...';
    statusMsg.className = 'status';
    statusMsg.style.display = 'block';
    
    // Send request to local Python server
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        statusMsg.textContent = 'Screenshot capture started successfully!';
        statusMsg.className = 'status success';
        updateButtonVisibility(true);
      } else {
        statusMsg.textContent = `Error: ${data.message}`;
        statusMsg.className = 'status error';
      }
    })
    .catch(error => {
      statusMsg.textContent = `Error: Cannot connect to local server. Make sure the Python server is running.`;
      statusMsg.className = 'status error';
      console.error('Error:', error);
    });
  });
  
  stopButton.addEventListener('click', function() {
    const url = 'http://localhost:5000/stop_capture';
    
    statusMsg.textContent = 'Stopping capture and saving PDF...';
    statusMsg.className = 'status';
    statusMsg.style.display = 'block';
    
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        statusMsg.textContent = 'Capture stopped and PDF saved successfully.';
        statusMsg.className = 'status success';
        updateButtonVisibility(false);
      } else {
        statusMsg.textContent = `Error: ${data.message}`;
        statusMsg.className = 'status error';
        checkStatus(); // Double-check status
      }
    })
    .catch(error => {
      statusMsg.textContent = `Error: Cannot connect to local server. Make sure the Python server is running.`;
      statusMsg.className = 'status error';
      console.error('Error:', error);
    });
  });
  
  function checkStatus() {
    fetch('http://localhost:5000/status', {
      method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'active') {
        updateButtonVisibility(true);
        statusMsg.textContent = 'A screenshot capture is currently running.';
        statusMsg.className = 'status success';
        statusMsg.style.display = 'block';
      } else {
        updateButtonVisibility(false);
      }
    })
    .catch(error => {
      console.error('Error checking status:', error);
    });
  }
  
  function updateButtonVisibility(isCapturing) {
    if (isCapturing) {
      startButton.style.display = 'none';
      stopButton.style.display = 'block';
    } else {
      startButton.style.display = 'block';
      stopButton.style.display = 'none';
    }
  }
});