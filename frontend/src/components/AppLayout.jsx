import React from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import { Outlet } from "react-router-dom";

export default function AppLayout() {
  return (
    <div className="app-layout">
      {/* Fixed Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <Header />
        <main className="page-content">
          <Outlet /> {/* Renders whichever active page route is loaded */}
        </main>
      </div>
    </div>
  );
}