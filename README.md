# StudySmart Schedule Optimizer

An intelligent study schedule optimizer that helps students manage their time effectively by analyzing coursework, deadlines, personal productivity patterns, and learning preferences.

## Features

- Task Priority Algorithm: Prioritizes assignments based on deadlines, difficulty, and importance
- Productivity Pattern Analysis: Tracks and analyzes optimal study times
- Spaced Repetition Integration: Suggests review sessions at optimal intervals
- Calendar Integration: Syncs with Google Calendar and academic schedules

## Tech Stack

- Backend: Python, Django, Django REST Framework
- Frontend: React, JavaScript
- Database: PostgreSQL
- Machine Learning: scikit-learn, pandas
- Calendar Integration: Google Calendar API

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/studysmart
GOOGLE_CALENDAR_CLIENT_ID=your-client-id
GOOGLE_CALENDAR_CLIENT_SECRET=your-client-secret
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Project Structure

```
studysmart/
├── backend/                 # Django backend
│   ├── api/                # REST API endpoints
│   ├── core/               # Core application logic
│   ├── scheduler/          # Scheduling algorithms
│   └── users/              # User management
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── services/      # API services
└── requirements.txt        # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License # studysmart
