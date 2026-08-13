import React, { useEffect, useState } from "react";
import { QrCode, RefreshCw } from "lucide-react";
import "./Attendance.css";

const API_URL = "http://127.0.0.1:8000";

export default function Attendance() {
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAttendance = async () => {
    try {
      setLoading(true);
      setError("");

      const token = localStorage.getItem("access_token");

      const response = await fetch(`${API_URL}/attendance/`, {
        headers: {
          "Content-Type": "application/json",
          ...(token && {
            Authorization: `Bearer ${token}`,
          }),
        },
      });

      if (!response.ok) {
        throw new Error("Failed to load attendance records");
      }

      const data = await response.json();

      setAttendanceRecords(data);
    } catch (err) {
      console.error("Attendance error:", err);

      setError("Failed to load attendance records");

      setAttendanceRecords([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttendance();
  }, []);

  const formatDate = (date) => {
    if (!date) return "--";

    const newDate = new Date(date);

    return newDate.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const formatTime = (time) => {
    if (!time) return "--";

    try {
      const [hours, minutes, seconds] = time.split(":");

      const date = new Date();
      date.setHours(hours, minutes, seconds || 0);

      return date.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    } catch {
      return time;
    }
  };

  const getTotalHours = (checkIn, checkOut) => {
    if (!checkIn || !checkOut) {
      return "--";
    }

    if (
      checkIn === "00:00:00" ||
      checkOut === "00:00:00"
    ) {
      return "--";
    }

    const start = new Date(`1970-01-01T${checkIn}`);
    const end = new Date(`1970-01-01T${checkOut}`);

    let difference = end - start;

    if (difference < 0) {
      difference += 24 * 60 * 60 * 1000;
    }

    const hours = Math.floor(
      difference / (1000 * 60 * 60)
    );

    const minutes = Math.floor(
      (difference % (1000 * 60 * 60)) /
        (1000 * 60)
    );

    return `${hours}h ${minutes}m`;
  };

  const getStatusClass = (status) => {
    const value = status?.toLowerCase();

    if (value === "present") {
      return "status-present";
    }

    if (value === "late") {
      return "status-late";
    }

    if (value === "absent") {
      return "status-absent";
    }

    return "";
  };

  const generateQR = () => {
    alert("Check-in QR generation will be added next.");
  };

  return (
    <div className="attendance-page">

      <div className="attendance-header">

        <div>
          <h1>Attendance Tracking</h1>

          <p>
            Track real-time check-ins and logs.
          </p>
        </div>

        <button
          className="qr-button"
          onClick={generateQR}
        >
          <QrCode size={17} />

          Generate Check-in QR
        </button>

      </div>

      {error && (
        <div className="attendance-error">
          {error}
        </div>
      )}

      {loading && (
        <div className="attendance-loading">
          Loading attendance records...
        </div>
      )}

      {!loading &&
        !error &&
        attendanceRecords.length > 0 && (

          <div className="attendance-card">

            <table className="attendance-table">

              <thead>
                <tr>
                  <th>DATE</th>
                  <th>EMPLOYEE</th>
                  <th>CHECK IN</th>
                  <th>CHECK OUT</th>
                  <th>TOTAL HOURS</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>

                {attendanceRecords.map((record) => (

                  <tr key={record.id}>

                    <td>
                      {formatDate(record.date)}
                    </td>

                    <td>
                      User #{record.user_id}
                    </td>

                    <td>
                      {formatTime(record.check_in)}
                    </td>

                    <td>
                      {formatTime(record.check_out)}
                    </td>

                    <td>
                      {getTotalHours(
                        record.check_in,
                        record.check_out
                      )}
                    </td>

                    <td>
                      <span
                        className={`status-badge ${getStatusClass(
                          record.status
                        )}`}
                      >
                        {record.status}
                      </span>
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>
        )}

      {!loading &&
        !error &&
        attendanceRecords.length === 0 && (

          <div className="no-records">
            No attendance records found.
          </div>

        )}

    </div>
  );
}