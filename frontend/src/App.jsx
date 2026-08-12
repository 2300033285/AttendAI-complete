import React from "react";
import {
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

// =====================================================
// LAYOUT
// =====================================================

import DashboardLayout from "./layouts/DashboardLayout";

// =====================================================
// PUBLIC PAGES
// =====================================================

import Welcome from "./pages/Welcome";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";

// =====================================================
// PROTECTED PAGES
// =====================================================

import Dashboard from "./pages/Dashboard";
import HRDashboard from "./pages/HRDashboard";
import Employees from "./pages/Employees";
import Attendance from "./pages/Attendance";
import Leaves from "./pages/Leaves";
import Reports from "./pages/Reports";
import Recruitment from "./pages/Recruitment";

// =====================================================
// SHIFT MANAGEMENT
// =====================================================

// Employee can VIEW their assigned shift
import EmployeeShifts from "./pages/EmployeeShifts";

// HR can VIEW and ASSIGN employee shifts
import HRShifts from "./pages/HRShifts";

// =====================================================
// AUTH PROTECTION
// =====================================================

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Routes>

      {/* =================================================
          PUBLIC ROUTES
      ================================================= */}

      <Route
        path="/"
        element={<Welcome />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      {/* =================================================
          FORGOT PASSWORD
      ================================================= */}

      <Route
        path="/forgot-password"
        element={<ForgotPassword />}
      />

      {/* =================================================
          PROTECTED APPLICATION
      ================================================= */}

      <Route element={<ProtectedRoute />}>

        <Route element={<DashboardLayout />}>

          {/* =================================================
              EMPLOYEE DASHBOARD
          ================================================= */}

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          {/* =================================================
              HR DASHBOARD
          ================================================= */}

          <Route
            path="/hr-dashboard"
            element={<HRDashboard />}
          />

          {/* =================================================
              EMPLOYEES
          ================================================= */}

          <Route
            path="/employees"
            element={<Employees />}
          />

          {/* =================================================
              ATTENDANCE
          ================================================= */}

          <Route
            path="/attendance"
            element={<Attendance />}
          />

          {/* =================================================
              LEAVE MANAGEMENT
          ================================================= */}

          <Route
            path="/leaves"
            element={<Leaves />}
          />

          {/* =================================================
              REPORTS
          ================================================= */}

          <Route
            path="/reports"
            element={<Reports />}
          />

          {/* =================================================
              RECRUITMENT
          ================================================= */}

          <Route
            path="/recruitment"
            element={<Recruitment />}
          />

          {/* =================================================
              EMPLOYEE SHIFT MANAGEMENT
              
              Employee can see:
              - Employee Name
              - Designation
              - Shift Time
              - Status
          ================================================= */}

          <Route
            path="/employee-shifts"
            element={<EmployeeShifts />}
          />

          {/* =================================================
              HR SHIFT MANAGEMENT
              
              HR can see:
              - Employee Name
              - Designation
              - Shift Time
              - Status
              - Assign Shift
              - Change Shift
          ================================================= */}

          <Route
            path="/hr-shifts"
            element={<HRShifts />}
          />

        </Route>

      </Route>

      {/* =================================================
          FALLBACK
      ================================================= */}

      <Route
        path="*"
        element={
          <Navigate
            to="/"
            replace
          />
        }
      />

    </Routes>
  );
}

export default App;