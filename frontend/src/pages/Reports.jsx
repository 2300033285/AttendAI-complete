import React from "react";
import { Download } from "lucide-react";

export default function Reports() {
  return (
    <>
      <div className="page-header">
        <div>
          <h1>Reports & Analytics</h1>
          <p style={{ color: "var(--text-secondary)" }}>
            Analyze trends, attendance patterns, and workforce logs.
          </p>
        </div>
        <button className="btn-primary">
          <Download size={16} /> Export Report
        </button>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-data">
            <h3>92.4%</h3>
            <p>Average Attendance Rate</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-data">
            <h3>4.2%</h3>
            <p>Overall Absence Rate</p>
          </div>
        </div>
      </div>

      <div className="table-container" style={{ padding: "1.5rem" }}>
        <strong style={{ fontSize: "1.1rem", display: "block", marginBottom: "1rem" }}>
          Weekly Attendance Trends
        </strong>
        <div className="chart-bars" style={{ height: "180px", gap: "1rem" }}>
          {[65, 80, 75, 90, 85, 40, 30].map((height, idx) => (
            <div key={idx} className="preview-bar-wrapper">
              <div className="preview-bar" style={{ height: `${height}%` }}></div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}