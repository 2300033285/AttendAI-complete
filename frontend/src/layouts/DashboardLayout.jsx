import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function DashboardLayout() {
  const location = useLocation();

  // Map route pathways to page titles for the dynamic Navbar header
  const getPageTitle = (pathname) => {
    switch (pathname) {
      case "/dashboard":
        return "Dashboard Overview";
      case "/employees":
        return "Employee Directory";
      case "/attendance":
        return "Attendance Logs";
      case "/leaves":
        return "Leave Management";
      case "/reports":
        return "Analytics & Reports";
      default:
        return "AttendAI Workspace";
    }
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Navbar title={getPageTitle(location.pathname)} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}