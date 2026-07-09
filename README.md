<<<<<<< HEAD
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
=======
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])

```
>>>>>>> 606b7e3f5e6915e590b80104f67133ef5f1dc8e9
