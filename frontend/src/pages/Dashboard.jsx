import React from "react";
import { useNavigate } from "react-router-dom";
import { 
  FiUsers, 
  FiClock, 
  FiCalendar, 
  FiAlertCircle, 
  FiArrowUpRight,
  FiUserCheck,
  FiUserX,
  FiPlusCircle
} from "react-icons/fi";

export default function Dashboard() {
  const navigate = useNavigate();

  // Teammates Data (matches Employees.jsx structure)
  const teammates = [
    { id: "EMP-001", name: "Sarah Jenkins", role: "Product Designer", dept: "Design", email: "sarah.j@attendai.com", status: "Active", joinDate: "Jan 15, 2023" },
    { id: "EMP-002", name: "Alex Rivera", role: "Frontend Developer", dept: "Engineering", email: "alex.r@attendai.com", status: "Active", joinDate: "Mar 01, 2023" },
    { id: "EMP-003", name: "Michael Chen", role: "Backend Engineer", dept: "Engineering", email: "m.chen@attendai.com", status: "On Leave", joinDate: "Nov 10, 2022" },
    { id: "EMP-004", name: "Emily Watson", role: "HR Specialist", dept: "Human Resources", email: "emily.w@attendai.com", status: "Active", joinDate: "Feb 20, 2024" },
    { id: "EMP-005", name: "David Kim", role: "Marketing Lead", dept: "Marketing", email: "david.k@attendai.com", status: "Inactive", joinDate: "Aug 05, 2021" },
  ];

  return (
    <div className="dashboard-container">
      {/* 1. Header & Welcome Message */}
      <div className="page-header">
        <div>
          <h1>Dashboard Overview</h1>
          <p className="subtext">Welcome back! Here is what's happening today.</p>
        </div>
        <div className="header-actions">
          <button className="btn-secondary" onClick={() => navigate("/leaves")}>
            <FiCalendar /> View Leave Requests
          </button>
          <button className="btn-primary" onClick={() => navigate("/employees")}>
            <FiPlusCircle /> Manage Staff
          </button>
        </div>
      </div>

      {/* 2. Key Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon"><FiUsers /></div>
          <div className="metric-data">
            <h3>148</h3>
            <p>Total Employees</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon success"><FiUserCheck /></div>
          <div className="metric-data">
            <h3>124</h3>
            <p>Present Today</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon warning"><FiClock /></div>
          <div className="metric-data">
            <h3>8</h3>
            <p>Late Arrivals</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon danger"><FiUserX /></div>
          <div className="metric-data">
            <h3>16</h3>
            <p>Absent / On Leave</p>
          </div>
        </div>
      </div>

      {/* 3. Dashboard Content Grid (Two Columns) */}
      <div className="dashboard-grid">
        
        {/* Left Column: Teammates Table */}
        <div className="table-container grid-card">
          <div className="table-header-tools">
            <h2 className="card-title">Teammates</h2>
            <button className="text-link-btn" onClick={() => navigate("/employees")}>
              View All <FiArrowUpRight />
            </button>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Employee Name</th>
                <th>Role</th>
                <th>Department</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {teammates.map((emp) => (
                <tr key={emp.id}>
                  <td>
                    <div className="user-details">
                      <strong className="user-name">{emp.name}</strong>
                      <span className="user-email">{emp.email}</span>
                    </div>
                  </td>
                  <td>{emp.role}</td>
                  <td>
                    <span className="dept-pill">{emp.dept}</span>
                  </td>
                  <td>
                    <span className={`badge ${
                      emp.status === "Active" ? "badge-success" : 
                      emp.status === "On Leave" ? "badge-warning" : "badge-danger"
                    }`}>
                      {emp.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Right Column: Quick Attendance Overview */}
        <div className="table-container grid-card">
          <div className="table-header-tools">
            <h2 className="card-title">Today's Attendance Status</h2>
          </div>

          <div className="overview-stats-body">
            <div className="progress-stat">
              <div className="stat-label">
                <span>On-Time Rate</span>
                <strong>88%</strong>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: "88%" }}></div>
              </div>
            </div>

            <div className="progress-stat">
              <div className="stat-label">
                <span>Shift Completion</span>
                <strong>65%</strong>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill warning" style={{ width: "65%" }}></div>
              </div>
            </div>

            <div className="quick-info-box">
              <FiAlertCircle className="info-icon" />
              <p>There are <strong>3 pending leave requests</strong> waiting for your approval.</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}