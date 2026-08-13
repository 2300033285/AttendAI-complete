import React, {
  useEffect,
  useState,
} from "react";

import {
  Clock3,
  BriefcaseBusiness,
  CheckCircle2,
  RefreshCw,
} from "lucide-react";

import {
  API_BASE_URL,
} from "../api/api";

export default function HRShifts() {

  // =====================================================
  // STATE
  // =====================================================

  const [shifts, setShifts] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  // =====================================================
  // FETCH SHIFTS
  // =====================================================

  const fetchShifts = async () => {

    try {

      setLoading(true);

      setError("");

      const token =
        localStorage.getItem(
          "access_token"
        );

      const response =
        await fetch(
          `${API_BASE_URL}/shifts/`,
          {
            method: "GET",

            headers: {

              Accept:
                "application/json",

              ...(token
                ? {
                    Authorization:
                      `Bearer ${token}`,
                  }
                : {}),
            },
          }
        );

      if (!response.ok) {

        const errorData =
          await response
            .json()
            .catch(() => ({}));

        throw new Error(
          errorData.detail ||
          "Failed to fetch shifts."
        );
      }

      const data =
        await response.json();

      setShifts(data);

    } catch (error) {

      console.error(
        "Shift fetch error:",
        error
      );

      setError(
        error.message ||
        "Unable to load shifts from the backend."
      );

    } finally {

      setLoading(false);

    }

  };

  // =====================================================
  // LOAD DATA
  // =====================================================

  useEffect(() => {

    fetchShifts();

  }, []);

  // =====================================================
  // FORMAT TIME
  // =====================================================

  const formatTime = (time) => {

    if (!time) {
      return "Not available";
    }

    try {

      const parts =
        time.split(":");

      let hours =
        parseInt(parts[0]);

      const minutes =
        parts[1];

      const ampm =
        hours >= 12
          ? "PM"
          : "AM";

      hours =
        hours % 12 || 12;

      return `${hours}:${minutes} ${ampm}`;

    } catch {

      return time;

    }

  };

  // =====================================================
  // STATUS STYLE
  // =====================================================

  const getStatusStyle = (status) => {

    if (status === true) {

      return {
        background:
          "#dcfce7",

        color:
          "#166534",

        label:
          "Active",
      };

    }

    return {

      background:
        "#fee2e2",

      color:
        "#b91c1c",

      label:
        "Inactive",

    };

  };

  // =====================================================
  // HANDLE CHANGE BUTTON
  // =====================================================

  const handleChangeShift =
    (shift) => {

      alert(
        `Shift: ${shift.shift_name}\n` +
        `Time: ${formatTime(
          shift.start_time
        )} - ${formatTime(
          shift.end_time
        )}`
      );

    };

  // =====================================================
  // UI
  // =====================================================

  return (

    <div
      style={{
        padding: "24px",
        minHeight: "100%",
        background: "#f8fafc",
      }}
    >

      {/* ================================================ */}
      {/* PAGE HEADER */}
      {/* ================================================ */}

      <div
        style={{
          marginBottom: "24px",
          display: "flex",
          justifyContent:
            "space-between",
          alignItems:
            "center",
        }}
      >

        <div>

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
            View and manage shifts.
          </p>

        </div>


        {/* REFRESH BUTTON */}

        <button
          type="button"
          onClick={fetchShifts}
          disabled={loading}

          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",

            padding:
              "10px 16px",

            border:
              "1px solid #dbe2ea",

            borderRadius:
              "8px",

            background:
              "#ffffff",

            color:
              "#334155",

            fontSize:
              "13px",

            fontWeight:
              "600",

            cursor:
              loading
                ? "not-allowed"
                : "pointer",

            opacity:
              loading
                ? 0.7
                : 1,
          }}
        >

          <RefreshCw
            size={16}
          />

          Refresh

        </button>

      </div>


      {/* ================================================ */}
      {/* ERROR MESSAGE */}
      {/* ================================================ */}

      {error && (

        <div
          style={{
            marginBottom:
              "20px",

            padding:
              "14px 18px",

            borderRadius:
              "10px",

            background:
              "#fee2e2",

            border:
              "1px solid #fecaca",

            color:
              "#b91c1c",

            fontSize:
              "14px",
          }}
        >

          {error}

        </div>

      )}


      {/* ================================================ */}
      {/* SHIFT TABLE CARD */}
      {/* ================================================ */}

      <div
        style={{
          background:
            "#ffffff",

          border:
            "1px solid #e2e8f0",

          borderRadius:
            "16px",

          overflow:
            "hidden",

          boxShadow:
            "0 4px 16px rgba(15, 23, 42, 0.06)",
        }}
      >


        {/* TABLE HEADER */}

        <div
          style={{
            padding:
              "20px 24px",

            borderBottom:
              "1px solid #e2e8f0",
          }}
        >

          <h2
            style={{
              margin: 0,

              fontSize:
                "18px",

              fontWeight:
                "700",

              color:
                "#0f172a",
            }}
          >
            Available Shifts
          </h2>

          <p
            style={{
              margin:
                "5px 0 0",

              fontSize:
                "13px",

              color:
                "#64748b",
            }}
          >
            Shifts loaded from the AttendAI backend.
          </p>

        </div>


        {/* ================================================ */}
        {/* LOADING */}
        {/* ================================================ */}

        {loading && (

          <div
            style={{
              padding:
                "50px",

              textAlign:
                "center",

              color:
                "#64748b",

              fontSize:
                "14px",
            }}
          >

            Loading shifts...

          </div>

        )}


        {/* ================================================ */}
        {/* EMPTY STATE */}
        {/* ================================================ */}

        {!loading &&
          !error &&
          shifts.length === 0 && (

          <div
            style={{
              padding:
                "50px",

              textAlign:
                "center",

              color:
                "#64748b",

              fontSize:
                "14px",
            }}
          >

            No shifts found.

            <br />

            Create a shift from your backend API.

          </div>

        )}


        {/* ================================================ */}
        {/* TABLE */}
        {/* ================================================ */}

        {!loading &&
          shifts.length > 0 && (

          <div
            style={{
              width:
                "100%",

              overflowX:
                "auto",
            }}
          >

            <table
              style={{
                width:
                  "100%",

                borderCollapse:
                  "collapse",

                minWidth:
                  "750px",
              }}
            >

              {/* TABLE HEAD */}

              <thead>

                <tr
                  style={{
                    background:
                      "#f8fafc",
                  }}
                >

                  <th
                    style={{
                      padding:
                        "14px 20px",

                      textAlign:
                        "left",

                      fontSize:
                        "12px",

                      color:
                        "#64748b",

                      fontWeight:
                        "700",
                    }}
                  >
                    SHIFT
                  </th>


                  <th
                    style={{
                      padding:
                        "14px 20px",

                      textAlign:
                        "left",

                      fontSize:
                        "12px",

                      color:
                        "#64748b",

                      fontWeight:
                        "700",
                    }}
                  >
                    START TIME
                  </th>


                  <th
                    style={{
                      padding:
                        "14px 20px",

                      textAlign:
                        "left",

                      fontSize:
                        "12px",

                      color:
                        "#64748b",

                      fontWeight:
                        "700",
                    }}
                  >
                    END TIME
                  </th>


                  <th
                    style={{
                      padding:
                        "14px 20px",

                      textAlign:
                        "left",

                      fontSize:
                        "12px",

                      color:
                        "#64748b",

                      fontWeight:
                        "700",
                    }}
                  >
                    STATUS
                  </th>


                  <th
                    style={{
                      padding:
                        "14px 20px",

                      textAlign:
                        "left",

                      fontSize:
                        "12px",

                      color:
                        "#64748b",

                      fontWeight:
                        "700",
                    }}
                  >
                    ACTION
                  </th>

                </tr>

              </thead>


              {/* TABLE BODY */}

              <tbody>

                {shifts.map(
                  (shift) => {

                    const statusStyle =
                      getStatusStyle(
                        shift.status
                      );

                    return (

                      <tr
                        key={shift.id}

                        style={{
                          borderTop:
                            "1px solid #e2e8f0",
                        }}
                      >


                        {/* SHIFT NAME */}

                        <td
                          style={{
                            padding:
                              "18px 20px",
                          }}
                        >

                          <div
                            style={{
                              display:
                                "flex",

                              alignItems:
                                "center",

                              gap:
                                "12px",
                            }}
                          >

                            <div
                              style={{
                                width:
                                  "38px",

                                height:
                                  "38px",

                                borderRadius:
                                  "50%",

                                background:
                                  "var(--primary)",

                                color:
                                  "#ffffff",

                                display:
                                  "flex",

                                alignItems:
                                  "center",

                                justifyContent:
                                  "center",

                                fontWeight:
                                  "700",
                              }}
                            >

                              {shift.shift_name
                                ?.charAt(0)
                                .toUpperCase() ||
                                "S"}

                            </div>


                            <div>

                              <p
                                style={{
                                  margin:
                                    0,

                                  fontSize:
                                    "14px",

                                  fontWeight:
                                    "600",

                                  color:
                                    "#1e293b",
                                }}
                              >

                                {shift.shift_name}

                              </p>


                              <p
                                style={{
                                  margin:
                                    "3px 0 0",

                                  fontSize:
                                    "11px",

                                  color:
                                    "#94a3b8",
                                }}
                              >

                                Shift ID:
                                {" "}
                                {shift.id}

                              </p>

                            </div>

                          </div>

                        </td>


                        {/* START TIME */}

                        <td
                          style={{
                            padding:
                              "18px 20px",

                            fontSize:
                              "14px",

                            color:
                              "#334155",
                          }}
                        >

                          <div
                            style={{
                              display:
                                "flex",

                              alignItems:
                                "center",

                              gap:
                                "8px",
                            }}
                          >

                            <Clock3
                              size={16}
                              color="#ea580c"
                            />

                            {formatTime(
                              shift.start_time
                            )}

                          </div>

                        </td>


                        {/* END TIME */}

                        <td
                          style={{
                            padding:
                              "18px 20px",

                            fontSize:
                              "14px",

                            color:
                              "#334155",
                          }}
                        >

                          <div
                            style={{
                              display:
                                "flex",

                              alignItems:
                                "center",

                              gap:
                                "8px",
                            }}
                          >

                            <Clock3
                              size={16}
                              color="#ea580c"
                            />

                            {formatTime(
                              shift.end_time
                            )}

                          </div>

                        </td>


                        {/* STATUS */}

                        <td
                          style={{
                            padding:
                              "18px 20px",
                          }}
                        >

                          <span
                            style={{
                              display:
                                "inline-flex",

                              alignItems:
                                "center",

                              gap:
                                "6px",

                              padding:
                                "7px 12px",

                              borderRadius:
                                "999px",

                              fontSize:
                                "12px",

                              fontWeight:
                                "600",

                              background:
                                statusStyle.background,

                              color:
                                statusStyle.color,
                            }}
                          >

                            <CheckCircle2
                              size={14}
                            />

                            {statusStyle.label}

                          </span>

                        </td>


                        {/* ACTION */}

                        <td
                          style={{
                            padding:
                              "18px 20px",
                          }}
                        >

                          <button
                            type="button"

                            onClick={() =>
                              handleChangeShift(
                                shift
                              )
                            }

                            style={{
                              padding:
                                "8px 13px",

                              border:
                                "1px solid #dbe2ea",

                              borderRadius:
                                "8px",

                              background:
                                "#ffffff",

                              color:
                                "#334155",

                              fontSize:
                                "12px",

                              fontWeight:
                                "600",

                              cursor:
                                "pointer",
                            }}
                          >

                            View Shift

                          </button>

                        </td>

                      </tr>

                    );

                  }
                )}

              </tbody>

            </table>

          </div>

        )}

      </div>

    </div>

  );

}