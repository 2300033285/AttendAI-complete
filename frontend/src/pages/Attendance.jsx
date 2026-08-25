import React, { useEffect, useState } from "react";
import {
  QrCode,
  CheckCircle2,
  Clock,
  User,
  Users,
  LogOut,
} from "lucide-react";
import { QRCodeSVG } from "qrcode.react";

export default function Attendance() {
  // =====================================================
  // STATE
  // =====================================================

  const [qrToken, setQrToken] = useState("");

  const [attendanceMarked, setAttendanceMarked] =
    useState(false);

  const [employeeAttendance, setEmployeeAttendance] =
    useState(null);

  const [allAttendance, setAllAttendance] =
    useState([]);

  const [isVerifying, setIsVerifying] =
    useState(true);

  const [isCheckingOut, setIsCheckingOut] =
    useState(false);


  // =====================================================
  // GET CURRENTLY LOGGED-IN USER
  // =====================================================

  const storedUser =
    localStorage.getItem("active_user");

  let currentUser = null;

  try {
    currentUser = storedUser
      ? JSON.parse(storedUser)
      : null;
  } catch (error) {
    currentUser = null;
  }


  const employeeName =
    currentUser?.name || "Employee";

  const employeeEmail =
    currentUser?.email || "";


  // =====================================================
  // GET CURRENT DATE
  // =====================================================

  const getCurrentDate = () => {
    return new Date().toLocaleDateString(
      "en-US",
      {
        month: "short",
        day: "2-digit",
        year: "numeric",
      }
    );
  };


  // =====================================================
  // GET CURRENT TIME
  // =====================================================

  const getCurrentTime = () => {
    return new Date().toLocaleTimeString(
      [],
      {
        hour: "2-digit",
        minute: "2-digit",
      }
    );
  };


  // =====================================================
  // CONVERT TIME TO MINUTES
  // Used for calculating total working hours
  // =====================================================

  const timeToMinutes = (timeString) => {
    if (!timeString) {
      return null;
    }

    const parts =
      timeString.match(
        /(\d+):(\d+)\s*(AM|PM)/i
      );

    if (!parts) {
      return null;
    }

    let hours =
      parseInt(parts[1], 10);

    const minutes =
      parseInt(parts[2], 10);

    const period =
      parts[3].toUpperCase();

    if (period === "PM" && hours !== 12) {
      hours += 12;
    }

    if (period === "AM" && hours === 12) {
      hours = 0;
    }

    return (
      hours * 60 + minutes
    );
  };


  // =====================================================
  // CALCULATE TOTAL WORKING HOURS
  // =====================================================

  const calculateTotalHours = (
    checkIn,
    checkOut
  ) => {

    const checkInMinutes =
      timeToMinutes(checkIn);

    const checkOutMinutes =
      timeToMinutes(checkOut);

    if (
      checkInMinutes === null ||
      checkOutMinutes === null
    ) {
      return "--";
    }

    let difference =
      checkOutMinutes -
      checkInMinutes;


    // Handles overnight shifts
    if (difference < 0) {
      difference += 24 * 60;
    }


    const hours =
      Math.floor(
        difference / 60
      );

    const minutes =
      difference % 60;


    return `${hours}h ${String(
      minutes
    ).padStart(2, "0")}m`;
  };


  // =====================================================
  // GENERATE ATTENDANCE QR TOKEN
  // =====================================================

  const generateAttendanceQR = () => {

    const randomCode =
      Math.random()
        .toString(36)
        .substring(2, 8)
        .toUpperCase();

    const token =
      `ATTENDAI-${Date.now()}-${randomCode}`;

    return token;
  };


  // =====================================================
  // LOAD ALL ATTENDANCE RECORDS
  // =====================================================

  const loadAllAttendance = () => {

    const savedRecords =
      localStorage.getItem(
        "attendance_records"
      );


    if (!savedRecords) {

      setAllAttendance([]);

      return [];
    }


    try {

      const parsedRecords =
        JSON.parse(savedRecords);


      if (Array.isArray(parsedRecords)) {

        setAllAttendance(
          parsedRecords
        );

        return parsedRecords;
      }


      return [];

    } catch (error) {

      console.error(
        "Unable to load attendance records:",
        error
      );

      return [];
    }
  };


  // =====================================================
  // SAVE ALL ATTENDANCE RECORDS
  // =====================================================

  const saveAllAttendance = (
    records
  ) => {

    localStorage.setItem(
      "attendance_records",
      JSON.stringify(records)
    );

    setAllAttendance(records);
  };


  // =====================================================
  // AUTOMATIC CHECK-IN
  // =====================================================

  const verifyAttendance = () => {

    if (
      !currentUser ||
      !employeeEmail
    ) {

      setIsVerifying(false);

      return;
    }


    const today =
      getCurrentDate();


    // =================================================
    // GET EXISTING RECORDS
    // =================================================

    const savedRecords =
      localStorage.getItem(
        "attendance_records"
      );

    let records = [];


    try {

      records = savedRecords
        ? JSON.parse(savedRecords)
        : [];


      if (!Array.isArray(records)) {
        records = [];
      }

    } catch (error) {

      records = [];
    }


    // =================================================
    // CHECK WHETHER EMPLOYEE ALREADY
    // HAS TODAY'S ATTENDANCE
    // =================================================

    const existingRecord =
      records.find(
        (record) =>
          record.email?.toLowerCase() ===
            employeeEmail.toLowerCase() &&
          record.date === today
      );


    // =================================================
    // EXISTING RECORD FOUND
    // =================================================

    if (existingRecord) {

      setQrToken(
        existingRecord.qrToken || ""
      );


      setEmployeeAttendance(
        existingRecord
      );


      setAttendanceMarked(true);


      setIsVerifying(false);


      setAllAttendance(
        records
      );


      return;
    }


    // =================================================
    // GENERATE NEW QR
    // =================================================

    const token =
      generateAttendanceQR();


    setQrToken(token);


    // =================================================
    // CREATE NEW ATTENDANCE RECORD
    // =================================================

    const newAttendance = {

      id: Date.now(),

      date: today,

      employee: employeeName,

      email: employeeEmail,

      checkIn:
        getCurrentTime(),

      checkOut: "--",

      totalHours: "--",

      status: "Present",

      qrToken: token,

      checkedOut: false,
    };


    // =================================================
    // ADD TO EXISTING RECORDS
    // =================================================

    const updatedRecords = [
      ...records,
      newAttendance,
    ];


    // =================================================
    // SAVE RECORDS
    // =================================================

    saveAllAttendance(
      updatedRecords
    );


    // =================================================
    // UPDATE CURRENT EMPLOYEE
    // =================================================

    setEmployeeAttendance(
      newAttendance
    );

    setAttendanceMarked(true);

    setIsVerifying(false);
  };


  // =====================================================
  // CHECK OUT CURRENT EMPLOYEE
  // =====================================================

  const handleCheckOut = () => {

    if (
      !employeeAttendance ||
      !employeeEmail
    ) {
      return;
    }


    // Prevent duplicate checkout

    if (
      employeeAttendance.checkedOut === true ||
      employeeAttendance.checkOut !== "--"
    ) {
      return;
    }


    setIsCheckingOut(true);


    // =================================================
    // GET CURRENT CHECKOUT TIME
    // =================================================

    const checkOutTime =
      getCurrentTime();


    // =================================================
    // CALCULATE TOTAL HOURS
    // =================================================

    const totalHours =
      calculateTotalHours(
        employeeAttendance.checkIn,
        checkOutTime
      );


    // =================================================
    // UPDATED CURRENT EMPLOYEE RECORD
    // =================================================

    const updatedAttendance = {

      ...employeeAttendance,

      checkOut:
        checkOutTime,

      totalHours:
        totalHours,

      checkedOut:
        true,

      status:
        "Present",
    };


    // =================================================
    // GET ALL EXISTING RECORDS
    // =================================================

    const savedRecords =
      localStorage.getItem(
        "attendance_records"
      );

    let records = [];


    try {

      records = savedRecords
        ? JSON.parse(savedRecords)
        : [];


      if (!Array.isArray(records)) {
        records = [];
      }

    } catch (error) {

      records = [];
    }


    // =================================================
    // UPDATE ONLY CURRENT EMPLOYEE
    // =================================================

    const updatedRecords =
      records.map(
        (record) => {

          if (
            record.email?.toLowerCase() ===
              employeeEmail.toLowerCase() &&
            record.date ===
              employeeAttendance.date
          ) {

            return updatedAttendance;
          }

          return record;
        }
      );


    // =================================================
    // SAVE UPDATED RECORDS
    // =================================================

    saveAllAttendance(
      updatedRecords
    );


    // =================================================
    // UPDATE CURRENT EMPLOYEE STATE
    // =================================================

    setEmployeeAttendance(
      updatedAttendance
    );


    setAllAttendance(
      updatedRecords
    );


    setIsCheckingOut(false);
  };


  // =====================================================
  // AUTOMATIC ATTENDANCE FLOW
  // =====================================================

  useEffect(() => {

    if (!currentUser) {

      setIsVerifying(false);

      return;
    }


    // Load all previous records

    loadAllAttendance();


    // Give UI a moment to render

    const verificationTimer =
      setTimeout(() => {

        verifyAttendance();

      }, 1000);


    return () => {

      clearTimeout(
        verificationTimer
      );

    };

  }, []);


  // =====================================================
  // RENDER
  // =====================================================

  return (
    <>
      {/* =================================================
          PAGE HEADER
      ================================================== */}

      <div className="page-header">

        <div>

          <h1>
            Attendance Tracking
          </h1>

          <p
            style={{
              color:
                "var(--text-secondary)",
            }}
          >
            Track real-time check-ins and
            attendance logs.
          </p>

        </div>

      </div>


      {/* =================================================
          AUTOMATIC ATTENDANCE CARD
      ================================================== */}

      <div
        style={{
          background: "#ffffff",
          borderRadius: "16px",
          padding: "30px",
          marginBottom: "25px",
          border:
            "1px solid #e5e7eb",
          boxShadow:
            "0 4px 15px rgba(0,0,0,0.05)",
        }}
      >

        <div
          style={{
            textAlign: "center",
          }}
        >

          {/* =================================================
              QR ICON
          ================================================== */}

          <div
            style={{
              display: "flex",
              justifyContent:
                "center",
              marginBottom: "15px",
            }}
          >

            <div
              style={{
                width: "48px",
                height: "48px",
                borderRadius: "12px",
                background:
                  "#eff6ff",
                display: "flex",
                alignItems:
                  "center",
                justifyContent:
                  "center",
              }}
            >

              <QrCode
                size={26}
                color="#2563eb"
              />

            </div>

          </div>


          {/* =================================================
              TITLE
          ================================================== */}

          <h2
            style={{
              marginBottom: "6px",
            }}
          >
            Automatic Attendance
          </h2>


          <p
            style={{
              color:
                "var(--text-secondary)",
              marginBottom: "25px",
            }}
          >
            Your attendance is being
            automatically processed.
          </p>


          {/* =================================================
              QR CODE
          ================================================== */}

          {qrToken && (

            <div
              style={{
                display: "flex",
                justifyContent:
                  "center",
                marginBottom: "25px",
              }}
            >

              <div
                style={{
                  padding: "18px",
                  border:
                    "1px solid #e5e7eb",
                  borderRadius: "14px",
                  background:
                    "#ffffff",
                }}
              >

                <QRCodeSVG
                  value={qrToken}
                  size={200}
                  level="H"
                />

              </div>

            </div>

          )}


          {/* =================================================
              VERIFYING STATE
          ================================================== */}

          {isVerifying && (

            <div
              style={{
                display: "flex",
                alignItems:
                  "center",
                justifyContent:
                  "center",
                gap: "8px",
                color:
                  "var(--text-secondary)",
                fontSize: "14px",
                marginBottom: "10px",
              }}
            >

              <Clock size={18} />

              Verifying attendance...

            </div>

          )}


          {/* =================================================
              SUCCESS STATE
          ================================================== */}

          {attendanceMarked && (

            <div
              style={{
                background:
                  "#f0fdf4",
                border:
                  "1px solid #bbf7d0",
                borderRadius: "12px",
                padding: "18px",
                marginTop: "10px",
              }}
            >

              <div
                style={{
                  display: "flex",
                  alignItems:
                    "center",
                  justifyContent:
                    "center",
                  gap: "8px",
                  color:
                    "#16a34a",
                  fontWeight: "600",
                  fontSize: "16px",
                }}
              >

                <CheckCircle2
                  size={22}
                />

                Attendance marked
                successfully

              </div>


              <p
                style={{
                  marginTop: "8px",
                  marginBottom: "0",
                  color:
                    "#166534",
                  fontSize: "14px",
                }}
              >
                Your check-in has been
                recorded.
              </p>

            </div>

          )}

        </div>

      </div>


      {/* =================================================
          CURRENT EMPLOYEE ATTENDANCE DETAILS
      ================================================== */}

      {employeeAttendance && (

        <div
          style={{
            background: "#ffffff",
            borderRadius: "16px",
            padding: "25px",
            marginBottom: "25px",
            border:
              "1px solid #e5e7eb",
          }}
        >

          <h2
            style={{
              marginBottom: "20px",
              fontSize: "18px",
            }}
          >
            Today's Attendance
          </h2>


          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "15px",
            }}
          >

            {/* =================================================
                EMPLOYEE
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  display: "flex",
                  alignItems:
                    "center",
                  gap: "8px",
                  marginBottom: "8px",
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                }}
              >

                <User size={16} />

                Employee

              </div>

              <strong>
                {employeeAttendance.employee}
              </strong>

            </div>


            {/* =================================================
                DATE
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                  marginBottom: "8px",
                }}
              >
                Date
              </div>

              <strong>
                {employeeAttendance.date}
              </strong>

            </div>


            {/* =================================================
                CHECK IN
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                  marginBottom: "8px",
                }}
              >
                Check In
              </div>

              <strong>
                {employeeAttendance.checkIn}
              </strong>

            </div>


            {/* =================================================
                CHECK OUT
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                  marginBottom: "8px",
                }}
              >
                Check Out
              </div>

              <strong>
                {employeeAttendance.checkOut}
              </strong>

            </div>


            {/* =================================================
                TOTAL HOURS
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                  marginBottom: "8px",
                }}
              >
                Total Hours
              </div>

              <strong>
                {employeeAttendance.totalHours}
              </strong>

            </div>


            {/* =================================================
                STATUS
            ================================================== */}

            <div
              style={{
                background:
                  "#f8fafc",
                padding: "16px",
                borderRadius: "10px",
              }}
            >

              <div
                style={{
                  color:
                    "var(--text-secondary)",
                  fontSize: "13px",
                  marginBottom: "8px",
                }}
              >
                Status
              </div>

              <span className="badge badge-success">
                {employeeAttendance.status}
              </span>

            </div>

          </div>


          {/* =================================================
              CHECK OUT BUTTON
          ================================================== */}

          {!employeeAttendance.checkedOut &&
            employeeAttendance.checkOut === "--" && (

            <div
              style={{
                marginTop: "25px",
                display: "flex",
                justifyContent:
                  "center",
              }}
            >

              <button
                className="btn-primary"
                onClick={handleCheckOut}
                disabled={isCheckingOut}
                style={{
                  display: "flex",
                  alignItems:
                    "center",
                  justifyContent:
                    "center",
                  gap: "8px",
                  minWidth: "180px",
                }}
              >

                <LogOut size={17} />

                {isCheckingOut
                  ? "Checking out..."
                  : "Check Out"}

              </button>

            </div>

          )}


          {/* =================================================
              CHECKED OUT MESSAGE
          ================================================== */}

          {employeeAttendance.checkedOut && (

            <div
              style={{
                marginTop: "25px",
                background:
                  "#eff6ff",
                border:
                  "1px solid #bfdbfe",
                borderRadius: "10px",
                padding: "14px",
                textAlign: "center",
                color: "#1d4ed8",
                fontSize: "14px",
                fontWeight: "500",
              }}
            >

              You have checked out
              successfully for today.

            </div>

          )}

        </div>

      )}


      {/* =================================================
          ALL EMPLOYEE ATTENDANCE
      ================================================== */}

      <div className="table-container">

        {/* TABLE HEADER */}

        <div
          style={{
            padding:
              "20px 20px 5px",
            display: "flex",
            alignItems:
              "center",
            gap: "10px",
          }}
        >

          <Users size={20} />

          <h2
            style={{
              fontSize: "18px",
              margin: 0,
            }}
          >
            All Attendance Records
          </h2>

        </div>


        {/* TABLE */}

        <table className="data-table">

          <thead>

            <tr>

              <th>
                Date
              </th>

              <th>
                Employee
              </th>

              <th>
                Email
              </th>

              <th>
                Check In
              </th>

              <th>
                Check Out
              </th>

              <th>
                Total Hours
              </th>

              <th>
                Status
              </th>

            </tr>

          </thead>


          <tbody>

            {allAttendance.length > 0 ? (

              allAttendance
                .slice()
                .reverse()
                .map((record) => (

                  <tr
                    key={record.id}
                  >

                    <td>
                      {record.date}
                    </td>

                    <td>
                      {record.employee}
                    </td>

                    <td>
                      {record.email}
                    </td>

                    <td>
                      {record.checkIn}
                    </td>

                    <td>
                      {record.checkOut}
                    </td>

                    <td>
                      {record.totalHours}
                    </td>

                    <td>

                      <span className="badge badge-success">
                        {record.status}
                      </span>

                    </td>

                  </tr>

                ))

            ) : (

              <tr>

                <td
                  colSpan="7"
                  style={{
                    textAlign:
                      "center",
                    padding:
                      "30px",
                    color:
                      "var(--text-secondary)",
                  }}
                >
                  No attendance records
                  available yet.
                </td>

              </tr>

            )}

          </tbody>

        </table>

      </div>

    </>
  );
}