import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FiUsers,
  FiClock,
  FiCalendar,
  FiAlertCircle,
  FiArrowUpRight,
  FiUserCheck,
  FiUserX,
  FiPlusCircle,
} from "react-icons/fi";

export default function Dashboard() {
  const navigate = useNavigate();

  // =====================================================
  // STATE
  // =====================================================

  const [teammates, setTeammates] = useState([]);

  const [totalEmployees, setTotalEmployees] = useState(0);
  const [presentToday, setPresentToday] = useState(0);
  const [lateArrivals, setLateArrivals] = useState(0);
  const [absentEmployees, setAbsentEmployees] = useState(0);

  const [onTimeRate, setOnTimeRate] = useState(0);
  const [shiftCompletion, setShiftCompletion] = useState(0);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // =====================================================
  // FETCH DASHBOARD DATA
  // =====================================================

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem("access_token");

        if (!token) {
          throw new Error("Please login again.");
        }

        const headers = {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        };

        // =================================================
        // FETCH EMPLOYEES
        // =================================================

        const employeeResponse = await fetch(
          "http://127.0.0.1:8000/employees/",
          {
            headers,
          }
        );

        if (!employeeResponse.ok) {
          throw new Error("Failed to load employees");
        }

        const employeeData = await employeeResponse.json();

        setTotalEmployees(employeeData.length);

        // Convert backend data to Dashboard UI format
        const formattedEmployees = employeeData
          .slice(0, 5)
          .map((employee) => ({
            id: employee.id,

            name: `${employee.first_name || ""} ${
              employee.last_name || ""
            }`.trim(),

            role: employee.designation || "Not Assigned",

            dept: employee.department || "Not Assigned",

            email: employee.email || "",

            status: employee.status
              ? "Active"
              : "Inactive",
          }));

        setTeammates(formattedEmployees);

        // =================================================
        // FETCH ATTENDANCE
        // =================================================

        try {
          const attendanceResponse = await fetch(
            "http://127.0.0.1:8000/attendance/",
            {
              headers,
            }
          );

          if (attendanceResponse.ok) {
            const attendanceData =
              await attendanceResponse.json();

            console.log(
              "Attendance:",
              attendanceData
            );

            // Get today's date
            const today = new Date()
              .toISOString()
              .split("T")[0];

            // Today's attendance records
            const todayAttendance =
              attendanceData.filter((record) => {
                if (!record.date) return false;

                return record.date
                  .toString()
                  .startsWith(today);
              });

            // Present employees
            const present =
              todayAttendance.filter(
                (record) =>
                  record.status === "Present" ||
                  record.status === "present"
              ).length;

            // Late employees
            const late =
              todayAttendance.filter(
                (record) =>
                  record.status === "Late" ||
                  record.status === "late"
              ).length;

            setPresentToday(present);

            setLateArrivals(late);

            // Absent = Total - Present - Late
            const absent =
              employeeData.length -
              present -
              late;

            setAbsentEmployees(
              absent > 0 ? absent : 0
            );

            // On-time percentage
            const totalAttendance =
              present + late;

            if (totalAttendance > 0) {
              const onTime =
                Math.round(
                  (present / totalAttendance) * 100
                );

              setOnTimeRate(onTime);
            }

            // Shift completion
            if (employeeData.length > 0) {
              const completion =
                Math.round(
                  (totalAttendance /
                    employeeData.length) *
                    100
                );

              setShiftCompletion(completion);
            }
          }
        } catch (attendanceError) {
          console.error(
            "Attendance error:",
            attendanceError
          );
        }
      } catch (error) {
        console.error(
          "Dashboard error:",
          error
        );

        setError(
          error.message ||
            "Failed to load dashboard"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return (
      <div className="dashboard-container">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  // =====================================================
  // ERROR
  // =====================================================

  if (error) {
    return (
      <div className="dashboard-container">
        <p>{error}</p>
      </div>
    );
  }

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="dashboard-container">

      {/* Header */}

      <div className="page-header">

        <div>
          <h1>Dashboard Overview</h1>

          <p className="subtext">
            Welcome back! Here is what's happening today.
          </p>
        </div>

        <div className="header-actions">

          <button
            className="btn-secondary"
            onClick={() =>
              navigate("/leaves")
            }
          >
            <FiCalendar />
            View Leave Requests
          </button>

          <button
            className="btn-primary"
            onClick={() =>
              navigate("/employees")
            }
          >
            <FiPlusCircle />
            Manage Staff
          </button>

        </div>

      </div>


      {/* Key Metrics */}

      <div className="metrics-grid">

        {/* Total Employees */}

        <div className="metric-card">

          <div className="metric-icon">
            <FiUsers />
          </div>

          <div className="metric-data">
            <h3>{totalEmployees}</h3>

            <p>Total Employees</p>
          </div>

        </div>


        {/* Present Today */}

        <div className="metric-card">

          <div className="metric-icon success">
            <FiUserCheck />
          </div>

          <div className="metric-data">
            <h3>{presentToday}</h3>

            <p>Present Today</p>
          </div>

        </div>


        {/* Late Arrivals */}

        <div className="metric-card">

          <div className="metric-icon warning">
            <FiClock />
          </div>

          <div className="metric-data">
            <h3>{lateArrivals}</h3>

            <p>Late Arrivals</p>
          </div>

        </div>


        {/* Absent */}

        <div className="metric-card">

          <div className="metric-icon danger">
            <FiUserX />
          </div>

          <div className="metric-data">
            <h3>{absentEmployees}</h3>

            <p>Absent / On Leave</p>
          </div>

        </div>

      </div>


      {/* Dashboard Content */}

      <div className="dashboard-grid">

        {/* Teammates */}

        <div className="table-container grid-card">

          <div className="table-header-tools">

            <h2 className="card-title">
              Teammates
            </h2>

            <button
              className="text-link-btn"
              onClick={() =>
                navigate("/employees")
              }
            >
              View All
              <FiArrowUpRight />
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

              {teammates.length === 0 ? (

                <tr>
                  <td colSpan="4">
                    No employees found.
                  </td>
                </tr>

              ) : (

                teammates.map((emp) => (

                  <tr key={emp.id}>

                    <td>

                      <div className="user-details">

                        <strong className="user-name">
                          {emp.name}
                        </strong>

                        <span className="user-email">
                          {emp.email}
                        </span>

                      </div>

                    </td>


                    <td>
                      {emp.role}
                    </td>


                    <td>

                      <span className="dept-pill">
                        {emp.dept}
                      </span>

                    </td>


                    <td>

                      <span
                        className={`badge ${
                          emp.status === "Active"
                            ? "badge-success"
                            : "badge-danger"
                        }`}
                      >
                        {emp.status}
                      </span>

                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>


        {/* Attendance Overview */}

        <div className="table-container grid-card">

          <div className="table-header-tools">

            <h2 className="card-title">
              Today's Attendance Status
            </h2>

          </div>


          <div className="overview-stats-body">


            {/* On Time */}

            <div className="progress-stat">

              <div className="stat-label">

                <span>
                  On-Time Rate
                </span>

                <strong>
                  {onTimeRate}%
                </strong>

              </div>


              <div className="progress-bar-bg">

                <div
                  className="progress-bar-fill"
                  style={{
                    width: `${onTimeRate}%`,
                  }}
                />

              </div>

            </div>


            {/* Shift Completion */}

            <div className="progress-stat">

              <div className="stat-label">

                <span>
                  Shift Completion
                </span>

                <strong>
                  {shiftCompletion}%
                </strong>

              </div>


              <div className="progress-bar-bg">

                <div
                  className="progress-bar-fill warning"
                  style={{
                    width: `${shiftCompletion}%`,
                  }}
                />

              </div>

            </div>


            {/* Leave Requests */}

            <div className="quick-info-box">

              <FiAlertCircle className="info-icon" />

              <p>
                There are{" "}
                <strong>
                  0 pending leave requests
                </strong>{" "}
                waiting for your approval.
              </p>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}