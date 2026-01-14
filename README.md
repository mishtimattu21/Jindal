# JSPL CSR Dashboard

A professional, comprehensive dashboard for managing and visualizing Corporate Social Responsibility (CSR) data.

## Features

- 📊 **Overview Dashboard**: KPI cards, progress indicators, and data visualizations
- 🏥 **Program-Specific Pages**: Detailed views for each CSR program
- 📝 **Data Entry Forms**: User-friendly forms for entering new data
- 📈 **Interactive Charts**: Donut charts, bar charts, and more using Plotly
- 🎨 **Professional UI**: Modern, clean design with gradient headers and styled components

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

### Important Note: Backend & Frontend
This dashboard uses **Streamlit**, which combines both backend and frontend in a single application. You only need to run **ONE command** - Streamlit handles everything automatically!

### Quick Start

1. **Ensure both Excel files are in the same directory:**
   - `CSR MIS.xlsx`
   - `JSPL CSR Data Input.xlsx`

2. **Install dependencies (first time only):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application (this starts both backend and frontend):**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard:**
   - The terminal will show: `Local URL: http://localhost:8501`
   - Your browser should open automatically
   - If not, manually visit: `http://localhost:8501`

### Alternative Methods

**Windows - Double-click:**
- Simply double-click `run.bat` file

**Using Python directly:**
```bash
python -m streamlit run app.py
```

**Stop the application:**
- Press `Ctrl + C` in the terminal

See `QUICK_START.md` for detailed instructions and troubleshooting.

## Project Structure

```
jindal/
├── app.py                 # Main Streamlit application
├── data_loader.py         # Data loading and processing module
├── requirements.txt       # Python dependencies
├── CSR MIS.xlsx          # Main CSR data file
├── JSPL CSR Data Input.xlsx  # Input data file
└── README.md             # This file
```

## Pages

1. **Overview**: Main dashboard with KPIs and visualizations
2. **Health & Nutrition**: Program-specific data for health programs
3. **Education**: Education program data (coming soon)
4. **Data Entry**: Form for entering new CSR data
5. **Reports**: Reporting and analytics (coming soon)

## Features in Detail

### KPI Dashboard
- Real-time progress indicators
- Status badges (On track, At risk, Delayed)
- Visual progress bars
- Last updated timestamps

### Data Visualization
- Donut charts for categorical data
- Bar charts for comparisons
- Age and income distribution charts
- Gender ratio visualizations

### Data Entry
- Comprehensive forms with validation
- Dropdown menus populated from master data
- Two-column layout for better UX
- Required field indicators

## Customization

The dashboard uses custom CSS for styling. You can modify the styles in the `app.py` file within the `st.markdown()` call that contains the CSS.

## Notes

- The dashboard automatically loads all sheets from both Excel files
- Data is cached for better performance
- The application handles missing data gracefully
- All visualizations are interactive (hover, zoom, etc.)

## Future Enhancements

- Database integration for data persistence
- User authentication
- Export functionality
- Advanced filtering and search
- More chart types
- Real-time data updates
