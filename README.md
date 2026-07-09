# አቋራጭ Bus Finder 🚌

A smart bus routing application designed to help people find the best bus routes in Addis Ababa.

The app helps users discover bus stops, search routes, and find convenient ways to travel around the city.

## Features

- 🚌 Search bus routes
- 📍 Find nearby bus stops
- 🗺️ View routes on an interactive map
- 🚏 Explore bus stops and destinations
- 🔎 Find the best travel options

## Tech Stack

### Frontend
- React + TypeScript
- Tailwind CSS
- React Leaflet
- Axios

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- PostGIS

## Project Structure

```text
aqwaraj-bus-finder/
│
├── frontend/   # React frontend
│
└── backend/    # FastAPI backend
```

## Getting Started

### Clone the repository

```bash
git clone https://github.com/yourusername/aqwaraj-bus-finder.git
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Backend Setup

```bash
cd backend

python -m venv venv

# Activate virtual environment

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Environment Variables

Create a `.env` file inside the backend folder:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

## Future Improvements

- Real-time bus tracking
- Route recommendations
- User accounts
- Amharic and English language support
- Mobile application

## License

This project is for learning and development purposes.