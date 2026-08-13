import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Users,
  UserCheck,
  UserPlus,
  CalendarDays,
  Clock,
  BriefcaseBusiness,
  ClipboardCheck,
  ArrowUpRight,
} from "lucide-react";

export default function HRDashboard() {
  const navigate = useNavigate();

  // =====================================================
  // STATE
  // =====================================================

  const [employees, setEmployees] = useState([]);
  const [attendance, setAttendance] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // =====================================================
  // FETCH DASHBOARD DATA
  // =====================================================

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError("");

       const token =
  localStorage.getItem("access_token") ||
  localStorage.getItem("token");

        if (!token) {
          throw new Error("Authentication token not found");
        }

        // Fetch Employees and Attendance
        const [employeesResponse, attendanceResponse] =
          await Promise.all([
            fetch("http://127.0.0.1:8000/employees/", {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }),

            fetch("http://127.0.0.1:8000/attendance/", {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }),
          ]);

        // Employees API validation
        if (!employeesResponse.ok) {
          throw new Error("Failed to load employees");
        }

        // Attendance API validation
        if (!attendanceResponse.ok) {
          throw new Error("Failed to load attendance");
        }

        const employeesData =
          await employeesResponse.json();

        const attendanceData =
          await attendanceResponse.json();

        console.log(
          "Dashboard Employees:",
          employeesData
        );

        console.log(
          "Dashboard Attendance:",
          attendanceData
        );

        setEmployees(
          Array.isArray(employeesData)
            ? employeesData
            : []
        );

        setAttendance(
          Array.isArray(attendanceData)
            ? attendanceData
            : []
        );

      } catch (err) {
        console.error(
          "Dashboard API Error:",
          err
        );

        setError(
          err.message ||
          "Failed to load dashboard data"
        );

      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // =====================================================
  // TODAY'S DATE
  // =====================================================

  const today = new Date()
    .toISOString()
    .split("T")[0];

  // =====================================================
  // FILTER TODAY'S ATTENDANCE
  // =====================================================

  const todayAttendance = attendance.filter((record) => {
    if (!record.date) {
      return true;
    }

    return record.date === today;
  });

  // =====================================================
  // ATTENDANCE CALCULATIONS
  // =====================================================

  const presentEmployees =
    todayAttendance.filter((record) =>
      String(record.status || "")
        .toLowerCase()
        .includes("present")
    );

  const lateEmployees =
    todayAttendance.filter((record) =>
      String(record.status || "")
        .toLowerCase()
        .includes("late")
    );

  const absentEmployees =
    todayAttendance.filter((record) =>
      String(record.status || "")
        .toLowerCase()
        .includes("absent")
    );

  const totalEmployees =
    employees.length;

  const presentCount =
    presentEmployees.length;

  const lateCount =
    lateEmployees.length;

  const absentCount =
    absentEmployees.length;

  const attendanceRate =
    totalEmployees > 0
      ? Math.round(
          (presentCount / totalEmployees) * 100
        )
      : 0;

  // =====================================================
  // DASHBOARD STATISTICS
  // =====================================================

  const stats = [
    {
      title: "Total Employees",
      value: totalEmployees,
      change: "Registered employees",
      icon: <Users size={22} />,
      iconClass: "",
    },

    {
      title: "Present Today",
      value: presentCount,
      change: `${attendanceRate}% attendance`,
      icon: <UserCheck size={22} />,
      iconClass: "success",
    },

    {
      title: "Leave Requests",
      value: "0",
      change: "Backend not available",
      icon: <CalendarDays size={22} />,
      iconClass: "warning",
    },

    {
      title: "Open Positions",
      value: "0",
      change: "Backend not available",
      icon: <BriefcaseBusiness size={22} />,
      iconClass: "info",
    },
  ];

  // =====================================================
  // RECENT EMPLOYEE ACTIVITY
  // =====================================================

  const recentEmployees =
    [...employees]
      .sort((a, b) => b.id - a.id)
      .slice(0, 5)
      .map((employee) => ({
        employee:
          `${employee.first_name || ""} ${
            employee.last_name || ""
          }`.trim() || "Unknown Employee",

        action: "Employee profile available",

        time:
          employee.joining_date ||
          employee.join_date ||
          "Recently added",

        status:
          employee.status
            ? "Completed"
            : "Inactive",
      }));

  // =====================================================
  // QUICK ACTIONS
  // =====================================================

  const quickActions = [
    {
      title: "Add Employee",
      description:
        "Create a new employee profile",
      icon: <UserPlus size={20} />,
      path: "/employees",
    },

    {
      title: "Review Leave Requests",
      description:
        "Leave management backend not available",
      icon: <ClipboardCheck size={20} />,
      path: "/leaves",
    },

    {
      title: "View Attendance",
      description:
        "Review today's attendance",
      icon: <Clock size={20} />,
      path: "/attendance",
    },

    {
      title: "Manage Recruitment",
      description:
        "View open job positions",
      icon: <BriefcaseBusiness size={20} />,
      path: "/recruitment",
    },
  ];

  // =====================================================
  // WORKFORCE SUMMARY
  // =====================================================

  const workforceStats = [
    {
      title: "Present",
      value: presentCount,
      className: "workforce-present",
    },

    {
      title: "Late",
      value: lateCount,
      className: "workforce-late",
    },

    {
      title: "Absent",
      value: absentCount,
      className: "workforce-absent",
    },

    {
      title: "Attendance Rate",
      value: `${attendanceRate}%`,
      className: "workforce-rate",
    },
  ];

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return (
      <div className="page-content hr-dashboard">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  // =====================================================
  // ERROR
  // =====================================================

  if (error) {
    return (
      <div className="page-content hr-dashboard">
        <p>{error}</p>
      </div>
    );
  }

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="page-content hr-dashboard">

      {/* PAGE HEADER */}

      <div className="page-header hr-dashboard-header">

        <div>

          <span className="dashboard-eyebrow">
            HR Management
          </span>

          <h1>HR Dashboard</h1>

          <p className="subtext">
            Manage your workforce and monitor HR activities.
          </p>

        </div>

      </div>


      {/* STATISTICS */}

      <div className="metrics-grid">

        {stats.map((stat, index) => (

          <div
            className="metric-card"
            key={index}
          >

            <div
              className={`metric-icon ${stat.iconClass}`}
            >
              {stat.icon}
            </div>

            <div className="metric-data">

              <p>
                {stat.title}
              </p>

              <h3>
                {stat.value}
              </h3>

              <span className="metric-change">
                {stat.change}
              </span>

            </div>

          </div>

        ))}

      </div>


      {/* MAIN GRID */}

      <div className="hr-dashboard-grid">


        {/* RECENT ACTIVITY */}

        <div className="table-container">

          <div className="table-header-tools">

            <div>

              <strong className="dashboard-section-title">
                Recent Employees
              </strong>

              <p className="subtext">
                Latest employee records from the system
              </p>

            </div>

            <button
              type="button"
              className="btn-secondary"
              onClick={() =>
                navigate("/employees")
              }
            >
              View All
              <ArrowUpRight size={16} />
            </button>

          </div>


          <div className="table-responsive">

            <table className="data-table">

              <thead>

                <tr>
                  <th>Employee</th>
                  <th>Activity</th>
                  <th>Joined Date</th>
                  <th>Status</th>
                </tr>

              </thead>


              <tbody>

                {recentEmployees.length > 0 ? (

                  recentEmployees.map(
                    (activity, index) => (

                      <tr key={index}>

                        <td>

                          <strong className="activity-employee">
                            {activity.employee}
                          </strong>

                        </td>

                        <td>
                          {activity.action}
                        </td>

                        <td className="activity-time">
                          {activity.time}
                        </td>

                        <td>

                          <span
                            className={
                              activity.status === "Completed"
                                ? "badge badge-success"
                                : "badge badge-warning"
                            }
                          >
                            {activity.status}
                          </span>

                        </td>

                      </tr>

                    )
                  )

                ) : (

                  <tr>

                    <td
                      colSpan="4"
                      style={{
                        textAlign: "center",
                        padding: "20px",
                      }}
                    >
                      No employees found
                    </td>

                  </tr>

                )}

              </tbody>

            </table>

          </div>

        </div>


        {/* QUICK ACTIONS */}

        <div className="quick-actions-card">

          <div className="quick-actions-header">

            <strong className="dashboard-section-title">
              Quick Actions
            </strong>

            <p className="subtext">
              Frequently used HR actions
            </p>

          </div>


          <div className="quick-actions-list">

            {quickActions.map(
              (action, index) => (

                <button
                  key={index}
                  type="button"
                  className="quick-action-btn"
                  onClick={() =>
                    navigate(action.path)
                  }
                >

                  <div className="quick-action-icon">
                    {action.icon}
                  </div>


                  <div className="quick-action-content">

                    <strong>
                      {action.title}
                    </strong>

                    <span>
                      {action.description}
                    </span>

                  </div>


                  <ArrowUpRight
                    size={16}
                    className="quick-action-arrow"
                  />

                </button>

              )
            )}

          </div>

        </div>

      </div>


      {/* WORKFORCE OVERVIEW */}

      <div className="table-container workforce-container">

        <div className="table-header-tools">

          <div>

            <strong className="dashboard-section-title">
              Today's Workforce Overview
            </strong>

            <p className="subtext">
              Current employee attendance summary
            </p>

          </div>

        </div>


        <div className="workforce-overview">

          {workforceStats.map(
            (item, index) => (

              <div
                key={index}
                className={`workforce-card ${item.className}`}
              >

                <span>
                  {item.title}
                </span>

                <h3>
                  {item.value}
                </h3>

              </div>

            )
          )}

        </div>

      </div>

    </div>
  );
}