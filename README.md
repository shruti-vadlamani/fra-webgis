# FRA WebGIS & Vanachitra.AI Integration

## Project Overview
Integrated Forest Rights Act (FRA) Atlas and WebGIS-based Decision Support System (DSS) for monitoring FRA implementation across Madhya Pradesh, Tripura, Odisha, and Telangana.

## Features

### 🌐 React Frontend (Vanachitra.AI)
- **Landing Page**: Nature-themed interface with animated forest elements
- **Document Upload**: AI-powered OCR and NER simulation for FRA documents
- **Custom Icons**: Professional iconography for mapping and document processing
- **Responsive Design**: Mobile-friendly forest-themed UI

### 🗺️ Flask Backend (FRA WebGIS)
- **Interactive WebGIS**: Spatial visualization of FRA claims and boundaries
- **Decision Support System**: Scheme eligibility analysis and recommendations
- **API Endpoints**: RESTful APIs for FRA data management
- **Asset Mapping**: Computer vision integration for satellite imagery analysis

## Architecture
- **Frontend**: React 19.1.1 with React Router for SPA navigation
- **Backend**: Flask with geospatial data processing capabilities
- **Integration**: React built and served by Flask for single-port deployment
- **Data**: GeoJSON format for spatial data, JSON for analytics

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd fra
```

2. Install Python dependencies:
```bash
cd fradss
pip install -r requirements.txt
```

3. Install React dependencies (if making frontend changes):
```bash
cd vanachitra-prototype
npm install
```

### Running the Application
```bash
cd fradss
python app_fra_webgis.py
```

Access the application at: `http://127.0.0.1:5001`

## Routes
- `/` - React frontend (Vanachitra.AI landing page)
- `/upload` - Document upload interface (React)
- `/webgis` - Interactive WebGIS interface (Flask template)
- `/api/*` - REST API endpoints for FRA data

## Project Structure
```
fra/
├── fradss/                     # Flask backend
│   ├── app_fra_webgis.py      # Main Flask application
│   ├── static/                # Static assets for WebGIS
│   ├── templates/             # Flask templates
│   ├── scripts/               # Data processing scripts
│   └── react_build/           # Built React app (auto-generated)
├── vanachitra-prototype/       # React frontend source
│   ├── src/                   # React source code
│   ├── public/                # Public assets
│   └── build/                 # Production build (auto-generated)
└── README.md                  # This file
```

## Development Workflow

### Making Frontend Changes
1. Edit React components in `vanachitra-prototype/src/`
2. Build the React app: `npm run build`
3. Copy build to Flask: `xcopy "build" "../fradss/react_build" /E /I /H /Y`
4. Restart Flask server

### Making Backend Changes
1. Edit Flask files in `fradss/`
2. Restart the Flask server

## Target States
- **Madhya Pradesh**: Tribal communities and forest resource management
- **Tripura**: Indigenous rights and land mapping
- **Odisha**: Coastal and forest land management
- **Telangana**: Agricultural and forest asset mapping

## Technologies Used
- **Frontend**: React, React Router, CSS3 animations
- **Backend**: Flask, Pandas, NumPy, Psycopg2
- **Data**: GeoJSON, JSON, CSV
- **Maps**: Web-based GIS with interactive layers
- **AI/ML**: Simulated OCR/NER for document processing

## Contributing
This is a prototype for the Smart India Hackathon 2025. For contributions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test integration
5. Submit a pull request

## License
MIT License - see LICENSE file for details

## Contact
For questions about this prototype, please reach out to the development team.

---
*Developed for Smart India Hackathon 2025 - Forest Rights Act Implementation*