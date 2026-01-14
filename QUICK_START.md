# Quick Start Guide - Running the CSR Dashboard

## Understanding the Architecture

This dashboard uses **Streamlit**, which is a Python framework that combines both frontend and backend in a single application. When you run the Streamlit app, it automatically:
- Starts a backend server (Python backend)
- Serves a web frontend (HTML/CSS/JavaScript)
- Handles all data processing and API calls internally

**You only need to run ONE command** - Streamlit handles everything!

## Method 1: Using Command Line (Recommended)

### Step 1: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Open Terminal

### Step 2: Navigate to Project Directory
```bash
cd "C:\Users\Mishti mattu\Desktop\jindal"
```

### Step 3: Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

### Step 5: Access the Dashboard
- The terminal will show a message like:
  ```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
  ```
- Your browser should automatically open
- If not, manually open: `http://localhost:8501`

## Method 2: Using the Batch File (Windows Only)

Simply double-click `run.bat` in the project folder. It will:
1. Install dependencies automatically
2. Start the Streamlit server
3. Open the dashboard in your browser

## Method 3: Using Python Directly

```bash
python -m streamlit run app.py
```

## What Happens When You Run?

1. **Backend Starts**: Python processes your data, handles calculations, and serves API endpoints
2. **Frontend Loads**: Streamlit generates HTML/CSS/JavaScript and serves it to your browser
3. **Data Processing**: The `data_loader.py` module reads all Excel sheets
4. **Dashboard Renders**: All pages, charts, and forms become interactive

## Stopping the Application

- Press `Ctrl + C` in the terminal/command prompt
- Or close the terminal window

## Troubleshooting

### Port Already in Use
If you see "Port 8501 is already in use":
```bash
streamlit run app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install streamlit pandas openpyxl plotly numpy
```

### Excel Files Not Found
Make sure both files are in the same directory:
- `CSR MIS.xlsx`
- `JSPL CSR Data Input.xlsx`

## Development Mode

For development with auto-reload:
```bash
streamlit run app.py --server.runOnSave true
```

## Production Deployment

For production, you can deploy to:
- **Streamlit Cloud**: Free hosting at share.streamlit.io
- **Docker**: Containerize the application
- **Cloud Platforms**: AWS, Azure, GCP with proper configuration

## Architecture Diagram

```
┌─────────────────────────────────────┐
│         Your Browser                 │
│    (Frontend - HTML/CSS/JS)         │
└──────────────┬───────────────────────┘
               │ HTTP Requests
               ▼
┌─────────────────────────────────────┐
│    Streamlit Server (Port 8501)     │
│  ┌───────────────────────────────┐  │
│  │  Python Backend (app.py)     │  │
│  │  - Data Processing            │  │
│  │  - Chart Generation            │  │
│  │  - Form Handling               │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Data Loader (data_loader.py) │  │
│  │  - Excel File Reading          │  │
│  │  - Data Caching                 │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Excel Files (Data Source)      │
│  - CSR MIS.xlsx                     │
│  - JSPL CSR Data Input.xlsx         │
└─────────────────────────────────────┘
```

## Summary

**Single Command to Run Everything:**
```bash
streamlit run app.py
```

That's it! No separate backend or frontend setup needed. Streamlit handles everything automatically.
