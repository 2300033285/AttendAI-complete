import React from "react";
import {
  Clock3,
  User,
  BriefcaseBusiness,
  CheckCircle2,
} from "lucide-react";

export default function HRShifts() {
  const employees = [
    {
      id: 1,
      name: "Neeharika",
      designation: "Frontend Developer",
      shift: "9:00 AM - 6:00 PM",
      status: "Active",
    },
    {
      id: 2,
      name: "Nikhil",
      designation: "Backend Developer",
      shift: "10:00 AM - 7:00 PM",
      status: "Active",
    },
    {
      id: 3,
      name: "Jyonith",
      designation: "Backend Developer",
      shift: "9:00 AM - 6:00 PM",
      status: "Upcoming",
    },
  ];

  const getStatusStyle = (status) => {
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

  return (
    <div
      style={{
        padding: "24px",
        minHeight: "100%",
        background: "#f8fafc",
      }}
    >
      {/* PAGE HEADER */}
      <div style={{ marginBottom: "24px" }}>
        <h1
          style={{
            margin: 0,
            fontSize: "26px",
            fontWeight: "700",
            color: "#0f172a",
          }}
        >
          Shift Management
        </h1>

        <p
          style={{
            margin: "6px 0 0",
            fontSize: "14px",
            color: "#64748b",
          }}
        >
          View and manage employee shifts.
        </p>
      </div>

      {/* SHIFT TABLE CARD */}
      <div
        style={{
          background: "#ffffff",
          border: "1px solid #e2e8f0",
          borderRadius: "16px",
          overflow: "hidden",
          boxShadow:
            "0 4px 16px rgba(15, 23, 42, 0.06)",
        }}
      >
        {/* TABLE HEADER */}
        <div
          style={{
            padding: "20px 24px",
            borderBottom: "1px solid #e2e8f0",
          }}
        >
          <h2
            style={{
              margin: 0,
              fontSize: "18px",
              fontWeight: "700",
              color: "#0f172a",
            }}
          >
            Employee Shifts
          </h2>

          <p
            style={{
              margin: "5px 0 0",
              fontSize: "13px",
              color: "#64748b",
            }}
          >
            Manage the assigned shifts of employees.
          </p>
        </div>

        {/* RESPONSIVE TABLE */}
        <div
          style={{
            width: "100%",
            overflowX: "auto",
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              minWidth: "750px",
            }}
          >
            <thead>
              <tr
                style={{
                  background: "#f8fafc",
                }}
              >
                <th
                  style={{
                    padding: "14px 20px",
                    textAlign: "left",
                    fontSize: "12px",
                    color: "#64748b",
                    fontWeight: "700",
                  }}
                >
                  EMPLOYEE
                </th>

                <th
                  style={{
                    padding: "14px 20px",
                    textAlign: "left",
                    fontSize: "12px",
                    color: "#64748b",
                    fontWeight: "700",
                  }}
                >
                  DESIGNATION
                </th>

                <th
                  style={{
                    padding: "14px 20px",
                    textAlign: "left",
                    fontSize: "12px",
                    color: "#64748b",
                    fontWeight: "700",
                  }}
                >
                  SHIFT TIME
                </th>

                <th
                  style={{
                    padding: "14px 20px",
                    textAlign: "left",
                    fontSize: "12px",
                    color: "#64748b",
                    fontWeight: "700",
                  }}
                >
                  STATUS
                </th>

                <th
                  style={{
                    padding: "14px 20px",
                    textAlign: "left",
                    fontSize: "12px",
                    color: "#64748b",
                    fontWeight: "700",
                  }}
                >
                  ACTION
                </th>
              </tr>
            </thead>

            <tbody>
              {employees.map((employee) => {
                const statusStyle = getStatusStyle(
                  employee.status
                );

                return (
                  <tr
                    key={employee.id}
                    style={{
                      borderTop:
                        "1px solid #e2e8f0",
                    }}
                  >
                    {/* EMPLOYEE */}
                    <td
                      style={{
                        padding: "18px 20px",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "12px",
                        }}
                      >
                        <div
                          style={{
                            width: "38px",
                            height: "38px",
                            borderRadius: "50%",
                            background:
                              "var(--primary)",
                            color: "#ffffff",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            fontWeight: "700",
                          }}
                        >
                          {employee.name
                            .charAt(0)
                            .toUpperCase()}
                        </div>

                        <div>
                          <p
                            style={{
                              margin: 0,
                              fontSize: "14px",
                              fontWeight: "600",
                              color: "#1e293b",
                            }}
                          >
                            {employee.name}
                          </p>

                          <p
                            style={{
                              margin: "3px 0 0",
                              fontSize: "11px",
                              color: "#94a3b8",
                            }}
                          >
                            Employee
                          </p>
                        </div>
                      </div>
                    </td>

                    {/* DESIGNATION */}
                    <td
                      style={{
                        padding: "18px 20px",
                        fontSize: "14px",
                        color: "#334155",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "8px",
                        }}
                      >
                        <BriefcaseBusiness
                          size={16}
                          color="#64748b"
                        />

                        {employee.designation}
                      </div>
                    </td>

                    {/* SHIFT */}
                    <td
                      style={{
                        padding: "18px 20px",
                        fontSize: "14px",
                        fontWeight: "600",
                        color: "#334155",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "8px",
                        }}
                      >
                        <Clock3
                          size={16}
                          color="#ea580c"
                        />

                        {employee.shift}
                      </div>
                    </td>

                    {/* STATUS */}
                    <td
                      style={{
                        padding: "18px 20px",
                      }}
                    >
                      <span
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "6px",
                          padding: "7px 12px",
                          borderRadius: "999px",
                          fontSize: "12px",
                          fontWeight: "600",
                          background:
                            statusStyle.background,
                          color:
                            statusStyle.color,
                        }}
                      >
                        <CheckCircle2 size={14} />

                        {employee.status}
                      </span>
                    </td>

                    {/* ACTION */}
                    <td
                      style={{
                        padding: "18px 20px",
                      }}
                    >
                      <button
                        type="button"
                        onClick={() =>
                          alert(
                            `Assign/change shift for ${employee.name}`
                          )
                        }
                        style={{
                          padding: "8px 13px",
                          border: "1px solid #dbe2ea",
                          borderRadius: "8px",
                          background: "#ffffff",
                          color: "#334155",
                          fontSize: "12px",
                          fontWeight: "600",
                          cursor: "pointer",
                        }}
                      >
                        Assign / Change
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}