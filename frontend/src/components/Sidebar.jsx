import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Clock,
  CalendarDays,
  BarChart3,
  LogOut,
  BriefcaseBusiness,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Sidebar() {
  const navigate = useNavigate();
  const { user } = useAuth();

  // =====================================================
  // USER ROLE
  // =====================================================

  const userRole = user?.role?.toLowerCase() || "employee";

  const isHR =
    userRole === "hr" ||
    userRole === "admin" ||
    userRole === "human resources";

  // =====================================================
  // NAVIGATION ITEMS
  // =====================================================

  const navItems = [
    {
      label: "Dashboard",
      path: isHR ? "/hr-dashboard" : "/dashboard",
      icon: LayoutDashboard,
    },

    {
      label: "Employees",
      path: "/employees",
      icon: Users,
    },

    {
      label: "Attendance",
      path: "/attendance",
      icon: Clock,
    },

    {
      label: "Shift Management",
      path: isHR ? "/hr-shifts" : "/employee-shifts",
      icon: BriefcaseBusiness,
    },

    {
      label: "Leave Requests",
      path: "/leaves",
      icon: CalendarDays,
    },

    {
      label: "Reports",
      path: "/reports",
      icon: BarChart3,
    },
  ];

  // =====================================================
  // LOGOUT
  // =====================================================

  const handleLogout = () => {
    // Clear authentication/session information
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    navigate("/login");
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <aside className="sidebar">

      {/* =================================================
          LOGO / BRAND
      ================================================= */}

      <div
        className="sidebar-brand"
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "1.5rem 1.25rem",
        }}
      >

        {/* LOGO */}

        <div
          style={{
            width: "38px",
            height: "38px",
            borderRadius: "10px",
            background: "var(--primary)",
            color: "#ffffff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: "800",
            fontSize: "16px",
          }}
        >
          A
        </div>

        {/* NAME */}

        <div>
          <h2
            style={{
              margin: 0,
              fontSize: "18px",
              fontWeight: "700",
            }}
          >
            AttendAI
          </h2>

          <p
            style={{
              margin: "2px 0 0",
              fontSize: "11px",
              color: "#94a3b8",
            }}
          >
            Workforce Management
          </p>
        </div>

      </div>


      {/* =================================================
          NAVIGATION
      ================================================= */}

      <nav className="sidebar-nav">

        {navItems.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >

              <Icon size={18} />

              <span>{item.label}</span>

            </NavLink>
          );
        })}

      </nav>


      {/* =================================================
          USER ROLE INDICATOR
      ================================================= */}

      <div
        style={{
          marginTop: "auto",
          padding: "1rem",
        }}
      >

        <div
          style={{
            padding: "10px 12px",
            borderRadius: "10px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            marginBottom: "12px",
          }}
        >

          <p
            style={{
              margin: 0,
              fontSize: "10px",
              color: "#94a3b8",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            Logged in as
          </p>

          <p
            style={{
              margin: "3px 0 0",
              fontSize: "13px",
              fontWeight: "600",
              color: "#334155",
              textTransform: "capitalize",
            }}
          >
            {isHR ? "HR / Admin" : "Employee"}
          </p>

        </div>


        {/* =================================================
            LOGOUT
        ================================================= */}

        <button
          className="nav-item"
          onClick={handleLogout}
          type="button"
          style={{
            width: "100%",
            color: "#dc2626",
            border: "none",
            background: "transparent",
            cursor: "pointer",
            textAlign: "left",
          }}
        >

          <LogOut size={18} />

          <span>Log Out</span>

        </button>

      </div>

    </aside>
  );
}