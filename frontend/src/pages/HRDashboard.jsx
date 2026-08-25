import React from "react";
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
  // HR DASHBOARD STATISTICS
  // =====================================================

  const stats = [
    {
      title: "Total Employees",
      value: "250",
      change: "+12 this month",
      icon: <Users size={22} />,
      iconClass: "",
    },
    {
      title: "Present Today",
      value: "230",
      change: "92% attendance",
      icon: <UserCheck size={22} />,
      iconClass: "success",
    },
    {
      title: "Leave Requests",
      value: "18",
      change: "5 pending approval",
      icon: <CalendarDays size={22} />,
      iconClass: "warning",
    },
    {
      title: "Open Positions",
      value: "8",
      change: "3 new this week",
      icon: <BriefcaseBusiness size={22} />,
      iconClass: "info",
    },
  ];

  // =====================================================
  // RECENT HR ACTIVITY
  // =====================================================

  const recentActivity = [
    {
      employee: "Ananya Reddy",
      action: "Leave request submitted",
      time: "10 minutes ago",
      status: "Pending",
    },
    {
      employee: "Rahul Sharma",
      action: "Joined the organization",
      time: "1 hour ago",
      status: "Completed",
    },
    {
      employee: "Priya Kumar",
      action: "Attendance correction requested",
      time: "2 hours ago",
      status: "Pending",
    },
    {
      employee: "Arjun Rao",
      action: "Profile information updated",
      time: "3 hours ago",
      status: "Completed",
    },
  ];

  // =====================================================
  // QUICK ACTIONS
  // =====================================================

  const quickActions = [
    {
      title: "Add Employee",
      description: "Create a new employee profile",
      icon: <UserPlus size={20} />,
      path: "/employees",
    },
    {
      title: "Review Leave Requests",
      description: "Check pending leave requests",
      icon: <ClipboardCheck size={20} />,
      path: "/leaves",
    },
    {
      title: "View Attendance",
      description: "Review today's attendance",
      icon: <Clock size={20} />,
      path: "/attendance",
    },
    {
  title: "Manage Recruitment",
  description: "View open job positions",
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
      value: "230",
      className: "workforce-present",
    },
    {
      title: "Late",
      value: "8",
      className: "workforce-late",
    },
    {
      title: "Absent",
      value: "12",
      className: "workforce-absent",
    },
    {
      title: "Attendance Rate",
      value: "92%",
      className: "workforce-rate",
    },
  ];

  return (
    <div className="page-content hr-dashboard">

      {/* =================================================
          PAGE HEADER
      ================================================= */}

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

      {/* =================================================
          STATISTICS CARDS
      ================================================= */}

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
              <p>{stat.title}</p>

              <h3>{stat.value}</h3>

              <span className="metric-change">
                {stat.change}
              </span>
            </div>
          </div>
        ))}

      </div>

      {/* =================================================
          MAIN HR DASHBOARD GRID
      ================================================= */}

      <div className="hr-dashboard-grid">

        {/* =================================================
            RECENT ACTIVITY
        ================================================= */}

        <div className="table-container">

          <div className="table-header-tools">

            <div>
              <strong className="dashboard-section-title">
                Recent HR Activity
              </strong>

              <p className="subtext">
                Latest employee and HR activities
              </p>
            </div>

            <button
              type="button"
              className="btn-secondary"
              onClick={() => navigate("/reports")}
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
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>

                {recentActivity.map((activity, index) => (
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
                ))}

              </tbody>

            </table>

          </div>

        </div>

        {/* =================================================
            QUICK ACTIONS
        ================================================= */}

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

            {quickActions.map((action, index) => (
              <button
                key={index}
                type="button"
                className="quick-action-btn"
                onClick={() => navigate(action.path)}
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
            ))}

          </div>

        </div>

      </div>

      {/* =================================================
          WORKFORCE OVERVIEW
      ================================================= */}

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

          {workforceStats.map((item, index) => (
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
          ))}

        </div>

      </div>

    </div>
  );
}