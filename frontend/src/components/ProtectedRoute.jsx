import React from "react";
import {
  Navigate,
  Outlet,
  useLocation,
} from "react-router-dom";

import { useAuth } from "../context/AuthContext";

// =====================================================
// PROTECTED ROUTE
// =====================================================

function ProtectedRoute() {

  const {
    isAuthenticated,
    user,
  } = useAuth();

  const location = useLocation();

  // ===================================================
  // CHECK AUTHENTICATION
  // ===================================================

  if (!isAuthenticated) {

    return (
      <Navigate
        to="/login"
        state={{
          from: location,
        }}
        replace
      />
    );

  }

  // ===================================================
  // GET USER ROLE
  // ===================================================

  const userRole =
    user?.role?.toLowerCase() || "employee";

  // ===================================================
  // HR DASHBOARD PROTECTION
  // ===================================================

  // Employees cannot access the HR Dashboard.

  if (
    location.pathname === "/hr-dashboard" &&
    userRole !== "hr" &&
    userRole !== "admin"
  ) {

    return (
      <Navigate
        to="/dashboard"
        replace
      />
    );

  }

  // ===================================================
  // EMPLOYEE DASHBOARD REDIRECTION
  // ===================================================

  // HR/Admin users are redirected to the HR Dashboard.

  if (
    location.pathname === "/dashboard" &&
    (userRole === "hr" || userRole === "admin")
  ) {

    return (
      <Navigate
        to="/hr-dashboard"
        replace
      />
    );

  }

  // ===================================================
  // ALLOW ACCESS
  // ===================================================

  return <Outlet />;
}

export default ProtectedRoute;