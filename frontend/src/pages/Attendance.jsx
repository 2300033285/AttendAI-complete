import React from "react";
import { QrCode } from "lucide-react";

export default function Attendance() {
  return (
    <>
      <div className="page-header">
        <div>
          <h1>Attendance Tracking</h1>
          <p style={{ color: "var(--text-secondary)" }}>Track real-time check-ins and logs.</p>
        </div>
        <button className="btn-primary">
          <QrCode size={16} /> Generate Check-in QR
        </button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Employee</th>
              <th>Check In</th>
              <th>Check Out</th>
              <th>Total Hours</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Jul 23, 2026</td>
              <td>Arjun Kumar</td>
              <td>08:58 AM</td>
              <td>05:00 PM</td>
              <td>8h 02m</td>
              <td><span className="badge badge-success">Present</span></td>
            </tr>
            <tr>
              <td>Jul 23, 2026</td>
              <td>Sneha Rao</td>
              <td>09:14 AM</td>
              <td>--</td>
              <td>--</td>
              <td><span className="badge badge-warning">Late</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
} 