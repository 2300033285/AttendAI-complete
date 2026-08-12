import React from "react";
import { Clock3, User, BriefcaseBusiness, CheckCircle2 } from "lucide-react";

export default function EmployeeShifts() {
  // Temporary mock data.
  // Later we will replace this with API data from the backend.
  const employeeShift = {
    name: "Neeharika",
    designation: "Frontend Developer",
    shift: "9:00 AM - 6:00 PM",
    status: "Active",
  };

  const getStatusClass = (status) => {
    if (status === "Active") {
      return {
        background: "#dcfce7",
        color: "#166534",
      };
    }

    if (status === "Upcoming") {
      return {
        background: "#dbeafe",
        color: "#1d4ed8",
      };
    }

    if (status === "Completed") {
      return {
        background: "#f1f5f9",
        color: "#475569",
      };
    }

    return {
      background: "#fef3c7",
      color: "#92400e",
    };
  };

  const statusStyle = getStatusClass(employeeShift.status);

  return (
    <div
      style={{
        padding: "24px",
        minHeight: "100%",
        background: "#f8fafc",
      }}
    >
      {/* PAGE HEADER */}
      <div
        style={{
          marginBottom: "24px",
        }}
      >
        <h1
          style={{
            margin: 0,
            fontSize: "26px",
            fontWeight: "700",
            color: "#0f172a",
          }}
        >
          My Shift
        </h1>

        <p
          style={{
            margin: "6px 0 0",
            fontSize: "14px",
            color: "#64748b",
          }}
        >
          View your assigned shift and current shift status.
        </p>
      </div>

      {/* SHIFT CARD */}
      <div
        style={{
          maxWidth: "900px",
          background: "#ffffff",
          border: "1px solid #e2e8f0",
          borderRadius: "16px",
          padding: "24px",
          boxShadow: "0 4px 16px rgba(15, 23, 42, 0.06)",
        }}
      >
        {/* CARD HEADER */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "16px",
            marginBottom: "24px",
            flexWrap: "wrap",
          }}
        >
          <div>
            <h2
              style={{
                margin: 0,
                fontSize: "19px",
                fontWeight: "700",
                color: "#0f172a",
              }}
            >
              Assigned Shift
            </h2>

            <p
              style={{
                margin: "5px 0 0",
                fontSize: "13px",
                color: "#64748b",
              }}
            >
              Your current work shift details
            </p>
          </div>

          {/* STATUS */}
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              padding: "7px 12px",
              borderRadius: "999px",
              fontSize: "12px",
              fontWeight: "600",
              background: statusStyle.background,
              color: statusStyle.color,
            }}
          >
            <CheckCircle2 size={14} />
            {employeeShift.status}
          </span>
        </div>

        {/* INFORMATION GRID */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "16px",
          }}
        >
          {/* EMPLOYEE NAME */}
          <div
            style={{
              padding: "18px",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              background: "#f8fafc",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "10px",
                background: "#eef2ff",
                color: "var(--primary)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "12px",
              }}
            >
              <User size={18} />
            </div>

            <p
              style={{
                margin: "0 0 5px",
                fontSize: "11px",
                color: "#94a3b8",
                fontWeight: "600",
                textTransform: "uppercase",
              }}
            >
              Employee Name
            </p>

            <p
              style={{
                margin: 0,
                fontSize: "15px",
                fontWeight: "600",
                color: "#1e293b",
              }}
            >
              {employeeShift.name}
            </p>
          </div>

          {/* DESIGNATION */}
          <div
            style={{
              padding: "18px",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              background: "#f8fafc",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "10px",
                background: "#f0fdf4",
                color: "#16a34a",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "12px",
              }}
            >
              <BriefcaseBusiness size={18} />
            </div>

            <p
              style={{
                margin: "0 0 5px",
                fontSize: "11px",
                color: "#94a3b8",
                fontWeight: "600",
                textTransform: "uppercase",
              }}
            >
              Designation
            </p>

            <p
              style={{
                margin: 0,
                fontSize: "15px",
                fontWeight: "600",
                color: "#1e293b",
              }}
            >
              {employeeShift.designation}
            </p>
          </div>

          {/* SHIFT TIME */}
          <div
            style={{
              padding: "18px",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              background: "#f8fafc",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "10px",
                background: "#fff7ed",
                color: "#ea580c",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "12px",
              }}
            >
              <Clock3 size={18} />
            </div>

            <p
              style={{
                margin: "0 0 5px",
                fontSize: "11px",
                color: "#94a3b8",
                fontWeight: "600",
                textTransform: "uppercase",
              }}
            >
              Shift Time
            </p>

            <p
              style={{
                margin: 0,
                fontSize: "15px",
                fontWeight: "600",
                color: "#1e293b",
              }}
            >
              {employeeShift.shift}
            </p>
          </div>

          {/* STATUS */}
          <div
            style={{
              padding: "18px",
              border: "1px solid #e2e8f0",
              borderRadius: "12px",
              background: "#f8fafc",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "10px",
                background: "#ecfdf5",
                color: "#059669",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "12px",
              }}
            >
              <CheckCircle2 size={18} />
            </div>

            <p
              style={{
                margin: "0 0 5px",
                fontSize: "11px",
                color: "#94a3b8",
                fontWeight: "600",
                textTransform: "uppercase",
              }}
            >
              Shift Status
            </p>

            <p
              style={{
                margin: 0,
                fontSize: "15px",
                fontWeight: "600",
                color: statusStyle.color,
              }}
            >
              {employeeShift.status}
            </p>
          </div>
        </div>

        {/* EMPLOYEE NOTICE */}
        <div
          style={{
            marginTop: "20px",
            padding: "14px 16px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            borderRadius: "10px",
            fontSize: "13px",
            color: "#64748b",
          }}
        >
          Your shift is assigned by HR. If you need to request a
          change, please contact your HR administrator.
        </div>
      </div>
    </div>
  );
}