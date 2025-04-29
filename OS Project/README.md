# Virtual Memory Manager Simulation

A web application that simulates virtual memory management using different page replacement algorithms.

## Features

- Input a page reference string (sequence of page numbers)
- Set the number of available memory frames
- Choose between FIFO and LRU page replacement algorithms
- View step-by-step simulation results
- See memory state changes and page fault statistics
- Visual chart showing page faults over time

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a comma-separated list of page numbers (e.g., 1,2,3,4,1,2,5,1,2,3,4,5)
2. Specify the number of memory frames available
3. Select the desired page replacement algorithm (FIFO or LRU)
4. Click "Run Simulation" to see the results

## Technologies Used

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Charts: Chart.js
