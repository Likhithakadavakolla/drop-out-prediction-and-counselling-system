import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import './App.css';

// Constants
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
const RISK_LEVELS = {
  HIGH: 'HIGH RISK',
  MEDIUM: 'MEDIUM RISK',
  LOW: 'LOW RISK'
};
const THRESHOLDS = {
  ATTENDANCE_HIGH: 60,
  ATTENDANCE_MEDIUM: 75,
  MARKS_HIGH: 40,
  MARKS_MEDIUM: 60,
  ATTEMPTS: 3
};

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState({});
  const [notifying, setNotifying] = useState({});
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  const [isAnimating, setIsAnimating] = useState(false);

  const toggleTheme = useCallback(() => {
    setIsAnimating(true);
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
    setTimeout(() => setIsAnimating(false), 700);
  }, []);

  const fetchStudents = useCallback(async () => {
    try {
      const { data } = await axios.get(`${API_URL}/students`);
      const studentsData = Array.isArray(data) ? data : [];
      setStudents(studentsData);
    } catch (error) {
      console.error('Failed to fetch students:', error.message);
      alert('Failed to load student data. Please ensure the backend server is running on port 8000.');
      setStudents([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Simple reliable cursor
  useEffect(() => {
    const cursor = document.createElement('div');
    cursor.className = 'cursor-dot';
    cursor.style.position = 'fixed';
    cursor.style.pointerEvents = 'none';
    cursor.style.zIndex = '99999';
    document.body.appendChild(cursor);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    const moveCursor = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      // Check for hover
      const target = e.target;
      if (target && target.closest) {
        const isHovering = target.closest('button, a, .stat-card, tr, input, textarea');
        cursor.classList.toggle('hover', !!isHovering);
      }
    };

    const updateCursor = () => {
      // Smooth following
      cursorX += (mouseX - cursorX) * 0.2;
      cursorY += (mouseY - cursorY) * 0.2;
      
      cursor.style.left = cursorX + 'px';
      cursor.style.top = cursorY + 'px';
      
      requestAnimationFrame(updateCursor);
    };

    document.addEventListener('mousemove', moveCursor);
    updateCursor();

    return () => {
      document.removeEventListener('mousemove', moveCursor);
      cursor.remove();
    };
  }, [theme]);

  const predictRisk = useCallback((student) => {
    const { attendance, marks, attempts } = student;
    
    if (attendance < THRESHOLDS.ATTENDANCE_HIGH || marks < THRESHOLDS.MARKS_HIGH || attempts >= THRESHOLDS.ATTEMPTS) {
      return { level: RISK_LEVELS.HIGH, color: '#ef4444', bgColor: '#fee2e2' };
    }
    
    if (attendance < THRESHOLDS.ATTENDANCE_MEDIUM || marks < THRESHOLDS.MARKS_MEDIUM) {
      return { level: RISK_LEVELS.MEDIUM, color: '#f59e0b', bgColor: '#fed7aa' };
    }
    
    return { level: RISK_LEVELS.LOW, color: '#10b981', bgColor: '#d1fae5' };
  }, []);

  const handlePredictAll = useCallback(() => {
    const newPredictions = {};
    students.forEach(student => {
      newPredictions[student.student_id] = predictRisk(student);
    });
    setPredictions(newPredictions);
  }, [students, predictRisk]);

  const handleNotify = useCallback(async (student) => {
    setNotifying(prev => ({ ...prev, [student.student_id]: true }));
    
    try {
      // Set 30 second timeout for email sending
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      
      const { data } = await axios.post(`${API_URL}/predict`, {
        student_id: student.student_id,
        attendance: student.attendance,
        marks: student.marks,
        attempts: student.attempts,
        guardian_email: student.guardian_email,
        mentor_email: student.mentor_email
      }, {
        signal: controller.signal,
        timeout: 30000
      });
      
      clearTimeout(timeoutId);
      
      if (data.email_sent) {
        alert(`✅ Notifications sent successfully!\n\nStudent: ${student.name}\nGuardian: ${student.guardian_email}\nMentor: ${student.mentor_email}`);
      } else {
        alert(`❌ Email failed: ${data.error || 'Unknown error'}\n\nPlease check backend email configuration.`);
      }
    } catch (error) {
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        alert(`⏱️ Request timed out (30s)\n\nEmail is taking too long. This could be due to:\n• Slow network connection\n• Email server issues\n\nThe email may still be sent in the background.`);
      } else {
        alert(`❌ Request failed: ${error.message}\n\nEnsure:\n• Backend is running\n• Email credentials are valid\n• Network connection is active`);
      }
    } finally {
      setNotifying(prev => ({ ...prev, [student.student_id]: false }));
    }
  }, []);

  // Memoized stats calculation
  const stats = useMemo(() => {
    const predictionValues = Object.values(predictions);
    return {
      high: predictionValues.filter(p => p.level === RISK_LEVELS.HIGH).length,
      medium: predictionValues.filter(p => p.level === RISK_LEVELS.MEDIUM).length,
      low: predictionValues.filter(p => p.level === RISK_LEVELS.LOW).length
    };
  }, [predictions]);

  // Memoized badge style calculation
  const getBadgeClass = useCallback((value, highThreshold, mediumThreshold) => {
    if (value >= mediumThreshold) return 'badge-success'; // >= 75: Green (Good)
    if (value >= highThreshold) return 'badge-warning';   // 60-74: Orange (Warning)
    return 'badge-danger';                                // < 60: Red (Critical)
  }, []);

  if (loading) {
    return (
      <div className={`loading-container ${theme}`}>
        <div className="spinner"></div>
        <p>Loading student data...</p>
      </div>
    );
  }

  return (
    <div className={`App ${theme} ${isAnimating ? 'animating' : ''}`}>
      <header className="app-header">
        <div className="header-content">
          <div>
            <h1>🎓 AI-Based Student Dropout Prediction System</h1>
            <p>Monitor student performance and predict dropout risk in real-time</p>
          </div>
          <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}>
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>
      </header>

      <div className="container">
        <div className="stats-section">
          <div className="stat-card">
            <h3>Total Students</h3>
            <p className="stat-number">{students.length}</p>
          </div>
          <div className="stat-card">
            <h3>High Risk</h3>
            <p className="stat-number stat-danger">{stats.high}</p>
          </div>
          <div className="stat-card">
            <h3>Medium Risk</h3>
            <p className="stat-number stat-warning">{stats.medium}</p>
          </div>
          <div className="stat-card">
            <h3>Low Risk</h3>
            <p className="stat-number stat-success">{stats.low}</p>
          </div>
        </div>

        <div className="actions-section">
          <button className="btn btn-primary" onClick={handlePredictAll}>
            🔍 Predict Risk for All Students
          </button>
        </div>

        <div className="table-section">
          <h2>📊 Student Dashboard</h2>
          <div className="table-wrapper">
            <table className="student-table">
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Attendance %</th>
                  <th>Marks</th>
                  <th>Attempts</th>
                  <th>Guardian Email</th>
                  <th>Mentor Email</th>
                  <th>Risk Level</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {students.map(student => {
                  const risk = predictions[student.student_id];
                  const isHighRisk = risk && risk.level === RISK_LEVELS.HIGH;
                  
                  return (
                    <tr key={student.student_id}>
                      <td>{student.student_id}</td>
                      <td className="student-name">{student.name}</td>
                      <td>
                        <span className={getBadgeClass(student.attendance, THRESHOLDS.ATTENDANCE_HIGH, THRESHOLDS.ATTENDANCE_MEDIUM)}>
                          {student.attendance}%
                        </span>
                      </td>
                      <td>
                        <span className={getBadgeClass(student.marks, THRESHOLDS.MARKS_HIGH, THRESHOLDS.MARKS_MEDIUM)}>
                          {student.marks}
                        </span>
                      </td>
                      <td>
                        <span className={student.attempts >= THRESHOLDS.ATTEMPTS ? 'badge-danger' : 'badge-success'}>
                          {student.attempts}
                        </span>
                      </td>
                      <td className="email-cell" title={student.guardian_email}>{student.guardian_email}</td>
                      <td className="email-cell" title={student.mentor_email}>{student.mentor_email}</td>
                      <td>
                        {risk ? (
                          <span 
                            className="risk-badge"
                            style={{ 
                              color: risk.color, 
                              backgroundColor: risk.bgColor,
                            }}
                          >
                            {risk.level}
                          </span>
                        ) : (
                          <span className="not-predicted">Not predicted yet</span>
                        )}
                      </td>
                      <td>
                        {isHighRisk && (
                          <button 
                            className="btn btn-notify"
                            onClick={() => handleNotify(student)}
                            disabled={notifying[student.student_id]}
                            aria-label={`Send notification for ${student.name}`}
                          >
                            {notifying[student.student_id] ? '📤 Sending...' : '📧 Notify'}
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {isAnimating && <div className="theme-transition-overlay"></div>}
    </div>
  );
}

export default App;
