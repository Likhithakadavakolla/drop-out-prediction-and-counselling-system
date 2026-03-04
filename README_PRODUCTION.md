# Student Dropout Prediction System

AI-based system to predict student dropout risk and send automated notifications.

## 🚀 Features

- **Risk Prediction**: AI-based dropout risk assessment (HIGH/MEDIUM/LOW)
- **Real-time Dashboard**: View all student performance metrics
- **Email Notifications**: Automated alerts to guardians and mentors
- **Dark/Light Theme**: Toggle between themes with preference saving
- **Responsive Design**: Works on desktop and mobile devices

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- Gmail account with App Password (for email notifications)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   cd drop-out-prediction-and-counselling-system
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv .venv-1
   source .venv-1/bin/activate  # On Windows: .venv-1\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn python-multipart pandas pydantic[email]
   ```

4. **Install Frontend dependencies**
   ```bash
   cd frontend-react
   npm install
   cd ..
   ```

5. **Configure Email Settings**
   - Edit `backend/notifier.py`
   - Update `EMAIL` and `PASSWORD` with your Gmail credentials
   - Generate App Password: https://myaccount.google.com/apppasswords

6. **Configure Environment Variables**
   ```bash
   cp frontend-react/.env.example frontend-react/.env
   # Edit .env if needed
   ```

## ▶️ Running the Application

### Option 1: Using npm start (Recommended)
```bash
npm start
```
This starts both backend (port 8000) and frontend (port 3000) automatically.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
source .venv-1/bin/activate
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend-react
npm start
```

### Option 3: Using Start Script
```bash
./start.sh
```

## 📊 Usage

1. Open http://localhost:3000 in your browser
2. Click "🔍 Predict Risk for All Students" to analyze all students
3. View risk levels (HIGH/MEDIUM/LOW) for each student
4. Click "📧 Notify" button for HIGH RISK students to send email alerts

## 🏗️ Project Structure

```
├── backend/
│   ├── app.py              # FastAPI application
│   └── notifier.py         # Email notification service
├── frontend-react/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── App.css         # Styling
│   └── .env                # Environment variables
├── frontend/
│   └── data/
│       └── student_data.csv  # Student records
├── package.json            # NPM scripts
└── start.sh               # Startup script

```

## 📧 Email Configuration

The system sends emails when HIGH RISK students are identified:

- **Guardian Email**: Alert with student performance details
- **Mentor Email**: Counseling action required notification

**Email format includes:**
- Student ID and performance metrics
- Risk assessment and recommendations
- Action items for intervention

## 🎨 Customization

### Risk Thresholds (backend/app.py)
```python
ATTENDANCE_THRESHOLD_HIGH = 60
MARKS_THRESHOLD_HIGH = 40
ATTEMPTS_THRESHOLD = 3
```

### Theme Colors (frontend-react/src/App.css)
Edit color variables for dark/light themes.

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available: `lsof -ti:8000`
- Verify Python virtual environment is activated

**Email not sending:**
- Verify Gmail App Password is correct
- Check internet connection
- Review backend logs for error messages

**Frontend shows no data:**
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in backend

## 📝 API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 Security Notes

- Never commit `.env` file with real credentials
- Use App Passwords, not actual Gmail passwords
- Regenerate App Passwords regularly
- Keep dependencies updated

## 📄 License

MIT License - see LICENSE file for details
