# 🎓 AI-Based Student Dropout Prediction & Counselling System

A full-stack web application that predicts student dropout risk using AI and sends automated email notifications to guardians and mentors.

## 🚀 Tech Stack

### Frontend
- **React.js** - Modern, responsive user interface
- **Axios** - HTTP client for API calls
- **CSS3** - Custom styling with gradient themes

### Backend
- **FastAPI** - High-performance Python web framework
- **Python 3.9+** - Backend logic and ML predictions
- **Uvicorn** - ASGI server
- **SMTP** - Email notification system

## 📁 Project Structure

```
drop-out-prediction-and-counselling-system/
├── backend/
│   ├── app.py           # FastAPI backend with prediction API
│   └── notifier.py      # Email notification service
├── frontend-react/      # React frontend application
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styling
│   └── package.json
├── frontend/            # Legacy Streamlit frontend (optional)
│   ├── app.py
│   └── data/
│       └── student_data.csv
└── ml/                  # Machine learning models and data
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to project root:**
   ```bash
   cd drop-out-prediction-and-counselling-system
   ```

2. **Install Python dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

3. **Start the backend server:**
   ```bash
   python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at:
   - API: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to React frontend:**
   ```bash
   cd frontend-react
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The app will open automatically at `http://localhost:3000`

## 📊 Features

### Dashboard
- 📈 **Real-time Statistics** - View total students and risk distribution
- 📋 **Student Data Table** - Comprehensive student performance data
- 🎯 **Risk Prediction** - AI-powered dropout risk analysis
- 📧 **Email Notifications** - Automated alerts to guardians and mentors
- 🎨 **Color-coded Indicators** - Visual risk level identification

### Risk Levels
- 🔴 **HIGH RISK**: Attendance < 60% OR Marks < 40 OR Attempts ≥ 3
- 🟡 **MEDIUM RISK**: Attendance < 75% OR Marks < 60
- 🟢 **LOW RISK**: Good performance across all metrics

## 🔌 API Endpoints

### `GET /`
Health check endpoint

### `GET /students`
Fetch all student data from CSV

**Response:**
```json
[
  {
    "student_id": 1,
    "name": "John Doe",
    "attendance": 85.5,
    "marks": 78.0,
    "attempts": 1,
    "guardian_email": "guardian@example.com",
    "mentor_email": "mentor@example.com"
  }
]
```

### `POST /predict`
Predict dropout risk and send notifications

**Request Body:**
```json
{
  "student_id": 1,
  "attendance": 55.0,
  "marks": 35.0,
  "attempts": 3,
  "guardian_email": "guardian@example.com",
  "mentor_email": "mentor@example.com"
}
```

**Response:**
```json
{
  "student_id": 1,
  "risk_level": "HIGH RISK",
  "message": "Immediate counselling required.",
  "timestamp": "2026-03-04T10:30:00"
}
```

## 🎮 Usage

1. **Start Both Servers:**
   - Backend: `python -m uvicorn backend.app:app --reload`
   - Frontend: `cd frontend-react && npm start`

2. **Access the Dashboard:**
   - Open `http://localhost:3000` in your browser

3. **View Student Data:**
   - The dashboard automatically loads student data from CSV

4. **Predict Risk:**
   - Click "🔍 Predict Risk for All Students"
   - View color-coded risk levels for each student

5. **Send Notifications:**
   - For high-risk students, click "📧 Notify"
   - Emails will be sent to guardians and mentors

## 📧 Email Configuration

Edit `backend/notifier.py` to configure your email settings:

```python
EMAIL = "your-email@gmail.com"
PASSWORD = "your-app-password"  # Use Gmail App Password
```

**Note:** For Gmail, enable 2FA and generate an App Password.

## 🎨 UI Features

- **Gradient Background** - Modern purple gradient design
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Hover Effects** - Interactive cards and buttons
- **Loading States** - Smooth loading animations
- **Color Coding** - Intuitive visual indicators

## 🛠️ Development

### Running in Development Mode

Backend (with auto-reload):
```bash
python -m uvicorn backend.app:app --reload
```

Frontend (with hot reload):
```bash
cd frontend-react && npm start
```

### Building for Production

Frontend:
```bash
cd frontend-react
npm run build
```

This creates an optimized production build in `frontend-react/build/`

## 🔐 Security Notes

- Change email credentials in `backend/notifier.py`
- Use environment variables for sensitive data in production
- Enable CORS only for trusted origins
- Implement authentication for production use

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributors

Developed for student welfare and dropout prevention initiatives.

## 🆘 Support

For issues or questions, please create an issue in the repository.

---

Made with ❤️ for educational institutions
