import React, { useState } from "react";
import {
  FiSearch,
  FiDownload,
  FiUsers,
  FiUserCheck,
  FiUserMinus,
  FiClock,
  FiUser,
  FiPhone,
  FiMail,
  FiSettings,
  FiEdit3,
  FiChevronDown,
  FiX,
  FiCamera,
} from "react-icons/fi";

import { useAuth } from "../context/AuthContext";

// =====================================================
// MOCK EMPLOYEE DATA
// =====================================================

const INITIAL_EMPLOYEES = [
  {
    id: "EMP-001",
    name: "Sarah Jenkins",
    role: "Product Designer",
    dept: "Design",
    email: "sarah.j@attendai.com",
    status: "Active",
    joinDate: "Jan 15, 2023",
  },
  {
    id: "EMP-002",
    name: "Alex Rivera",
    role: "Frontend Developer",
    dept: "Engineering",
    email: "alex.r@attendai.com",
    status: "Active",
    joinDate: "Mar 01, 2023",
  },
  {
    id: "EMP-003",
    name: "Michael Chen",
    role: "Backend Engineer",
    dept: "Engineering",
    email: "m.chen@attendai.com",
    status: "On Leave",
    joinDate: "Nov 10, 2022",
  },
  {
    id: "EMP-004",
    name: "Emily Watson",
    role: "HR Specialist",
    dept: "Human Resources",
    email: "emily.w@attendai.com",
    status: "Active",
    joinDate: "Feb 20, 2024",
  },
  {
    id: "EMP-005",
    name: "David Kim",
    role: "Marketing Lead",
    dept: "Marketing",
    email: "david.k@attendai.com",
    status: "Inactive",
    joinDate: "Aug 05, 2021",
  },
];

// =====================================================
// EMPLOYEES COMPONENT
// =====================================================

export default function Employees() {
  const { user } = useAuth();

  // =====================================================
  // USER PROFILE DATA
  // =====================================================

  const [profile, setProfile] = useState(() => {
    const savedProfile =
      localStorage.getItem("attendai_profile");

    if (savedProfile) {
      try {
        return JSON.parse(savedProfile);
      } catch {
        return null;
      }
    }

    return {
      name: user?.name || "User",
      email: user?.email || "user@attendai.com",
      phone: "+91 98765 43210",
      picture: "",
    };
  });

  // =====================================================
  // STATES
  // =====================================================

  const [employees] =
    useState(INITIAL_EMPLOYEES);

  const [search, setSearch] =
    useState("");

  const [selectedDept, setSelectedDept] =
    useState("All");

  const [isProfileOpen, setIsProfileOpen] =
    useState(false);

  const [isEditProfileOpen, setIsEditProfileOpen] =
    useState(false);

  const [editProfile, setEditProfile] =
    useState(profile);

  // =====================================================
  // FILTER EMPLOYEES
  // =====================================================

  const filteredEmployees =
    employees.filter((emp) => {
      const searchValue =
        search.toLowerCase();

      const matchesSearch =
        emp.name
          .toLowerCase()
          .includes(searchValue) ||
        emp.email
          .toLowerCase()
          .includes(searchValue) ||
        emp.id
          .toLowerCase()
          .includes(searchValue);

      const matchesDept =
        selectedDept === "All" ||
        emp.dept === selectedDept;

      return (
        matchesSearch &&
        matchesDept
      );
    });

  // =====================================================
  // EXPORT CSV
  // =====================================================

  const handleExportCSV = () => {
    if (filteredEmployees.length === 0) {
      alert(
        "No employee records available to export."
      );
      return;
    }

    const headers = [
      "ID",
      "Name",
      "Email",
      "Role",
      "Department",
      "Status",
      "Joined Date",
    ];

    const rows =
      filteredEmployees.map((emp) => [
        emp.id,
        `"${emp.name}"`,
        `"${emp.email}"`,
        `"${emp.role}"`,
        `"${emp.dept}"`,
        `"${emp.status}"`,
        `"${emp.joinDate}"`,
      ]);

    const csvContent =
      "data:text/csv;charset=utf-8," +
      [
        headers.join(","),
        ...rows.map((row) =>
          row.join(",")
        ),
      ].join("\n");

    const encodedUri =
      encodeURI(csvContent);

    const link =
      document.createElement("a");

    link.setAttribute(
      "href",
      encodedUri
    );

    link.setAttribute(
      "download",
      `Employee_Directory_${new Date()
        .toISOString()
        .slice(0, 10)}.csv`
    );

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
  };

  // =====================================================
  // SAVE PROFILE
  // =====================================================

  const handleSaveProfile = (e) => {
    e.preventDefault();

    setProfile(editProfile);

    localStorage.setItem(
      "attendai_profile",
      JSON.stringify(editProfile)
    );

    setIsEditProfileOpen(false);
  };

  // =====================================================
  // PROFILE PICTURE
  // =====================================================

  const handleProfilePicture = (e) => {
    const file =
      e.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select an image file.");
      return;
    }

    const reader =
      new FileReader();

    reader.onload = () => {
      setEditProfile((previous) => ({
        ...previous,
        picture: reader.result,
      }));
    };

    reader.readAsDataURL(file);
  };

  // =====================================================
  // STATISTICS
  // =====================================================

  const totalEmployees =
    employees.length;

  const activeEmployees =
    employees.filter(
      (employee) =>
        employee.status === "Active"
    ).length;

  const employeesOnLeave =
    employees.filter(
      (employee) =>
        employee.status === "On Leave"
    ).length;

  const inactiveEmployees =
    employees.filter(
      (employee) =>
        employee.status === "Inactive"
    ).length;

  // =====================================================
  // USER INITIAL
  // =====================================================

  const userInitial =
    profile.name
      ?.charAt(0)
      ?.toUpperCase() || "U";

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="employees-container">

      {/* =================================================
          PAGE HEADER
      ================================================= */}

      <div
        className="page-header"
        style={{
          position: "relative",
        }}
      >

        <div>

          <h1>
            Employee Directory
          </h1>

          <p className="subtext">
            Manage staff profiles, roles,
            and departmental information.
          </p>

        </div>


        {/* =================================================
            TOP RIGHT ACTIONS
        ================================================= */}

        <div
          className="header-actions"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >

          {/* EXPORT */}

          <button
            className="btn-secondary"
            onClick={handleExportCSV}
          >
            <FiDownload />

            Export CSV
          </button>


          {/* =================================================
              USER PROFILE BUTTON
          ================================================= */}

          <div
            style={{
              position: "relative",
            }}
          >

            <button
              type="button"
              onClick={() =>
                setIsProfileOpen(
                  !isProfileOpen
                )
              }
              style={{
                display: "flex",
                alignItems: "center",
                gap: "9px",
                padding: "6px 10px",
                background: "#ffffff",
                border: "1px solid #e5e7eb",
                borderRadius: "10px",
                cursor: "pointer",
                boxShadow:
                  "0 2px 8px rgba(0,0,0,0.05)",
              }}
            >

              {/* PROFILE IMAGE */}

              {profile.picture ? (

                <img
                  src={profile.picture}
                  alt="Profile"
                  style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "50%",
                    objectFit: "cover",
                  }}
                />

              ) : (

                <div
                  style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "50%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background:
                      "#eef2ff",
                    color: "#4f46e5",
                    fontWeight: "700",
                    fontSize: "16px",
                  }}
                >
                  {userInitial}
                </div>

              )}


              {/* NAME */}

              <div
                style={{
                  textAlign: "left",
                  lineHeight: "1.2",
                }}
              >

                <strong
                  style={{
                    display: "block",
                    fontSize: "13px",
                    color: "#111827",
                  }}
                >
                  {profile.name}
                </strong>

                <span
                  style={{
                    fontSize: "11px",
                    color: "#6b7280",
                  }}
                >
                  {user?.role ||
                    "Employee"}
                </span>

              </div>


              <FiChevronDown
                size={16}
                color="#6b7280"
              />

            </button>


            {/* =================================================
                PROFILE DROPDOWN
            ================================================= */}

            {isProfileOpen && (

              <div
                style={{
                  position: "absolute",
                  top: "52px",
                  right: "0",
                  width: "310px",
                  background: "#ffffff",
                  border:
                    "1px solid #e5e7eb",
                  borderRadius: "14px",
                  boxShadow:
                    "0 15px 40px rgba(0,0,0,0.12)",
                  zIndex: 1000,
                  overflow: "hidden",
                }}
              >

                {/* PROFILE HEADER */}

                <div
                  style={{
                    padding: "20px",
                    background:
                      "#f8fafc",
                    borderBottom:
                      "1px solid #e5e7eb",
                    display: "flex",
                    alignItems: "center",
                    gap: "14px",
                  }}
                >

                  {profile.picture ? (

                    <img
                      src={
                        profile.picture
                      }
                      alt="Profile"
                      style={{
                        width: "62px",
                        height: "62px",
                        borderRadius:
                          "50%",
                        objectFit:
                          "cover",
                      }}
                    />

                  ) : (

                    <div
                      style={{
                        width: "62px",
                        height: "62px",
                        borderRadius:
                          "50%",
                        background:
                          "#eef2ff",
                        color: "#4f46e5",
                        display: "flex",
                        alignItems:
                          "center",
                        justifyContent:
                          "center",
                        fontSize: "24px",
                        fontWeight: "700",
                      }}
                    >
                      {userInitial}
                    </div>

                  )}


                  <div>

                    <h3
                      style={{
                        margin: "0 0 4px",
                        fontSize: "17px",
                        color:
                          "#111827",
                      }}
                    >
                      {profile.name}
                    </h3>

                    <span
                      style={{
                        fontSize: "12px",
                        color:
                          "#6b7280",
                      }}
                    >
                      {user?.role ||
                        "Employee"}
                    </span>

                  </div>

                </div>


                {/* PROFILE INFORMATION */}

                <div
                  style={{
                    padding: "16px 20px",
                  }}
                >

                  {/* PHONE */}

                  <div
                    style={{
                      display: "flex",
                      gap: "12px",
                      alignItems:
                        "center",
                      marginBottom:
                        "15px",
                    }}
                  >

                    <FiPhone
                      size={17}
                      color="#6366f1"
                    />

                    <div>

                      <span
                        style={{
                          display:
                            "block",
                          fontSize:
                            "11px",
                          color:
                            "#9ca3af",
                          marginBottom:
                            "2px",
                        }}
                      >
                        Phone Number
                      </span>

                      <strong
                        style={{
                          fontSize:
                            "13px",
                          color:
                            "#374151",
                        }}
                      >
                        {profile.phone ||
                          "Not provided"}
                      </strong>

                    </div>

                  </div>


                  {/* EMAIL */}

                  <div
                    style={{
                      display: "flex",
                      gap: "12px",
                      alignItems:
                        "center",
                      marginBottom:
                        "18px",
                    }}
                  >

                    <FiMail
                      size={17}
                      color="#6366f1"
                    />

                    <div>

                      <span
                        style={{
                          display:
                            "block",
                          fontSize:
                            "11px",
                          color:
                            "#9ca3af",
                          marginBottom:
                            "2px",
                        }}
                      >
                        Email Address
                      </span>

                      <strong
                        style={{
                          fontSize:
                            "13px",
                          color:
                            "#374151",
                          wordBreak:
                            "break-word",
                        }}
                      >
                        {profile.email}
                      </strong>

                    </div>

                  </div>


                  {/* EDIT PROFILE */}

                  <button
                    type="button"
                    onClick={() => {
                      setEditProfile(
                        profile
                      );
                      setIsProfileOpen(
                        false
                      );
                      setIsEditProfileOpen(
                        true
                      );
                    }}
                    style={{
                      width: "100%",
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "10px",
                      padding:
                        "10px 12px",
                      background:
                        "#f8fafc",
                      border:
                        "1px solid #e5e7eb",
                      borderRadius:
                        "8px",
                      cursor:
                        "pointer",
                      fontSize:
                        "13px",
                      color:
                        "#374151",
                      marginBottom:
                        "8px",
                    }}
                  >

                    <FiEdit3
                      size={16}
                    />

                    Edit Profile

                  </button>


                  {/* SETTINGS */}

                  <button
                    type="button"
                    onClick={() =>
                      alert(
                        "Settings page will be connected here."
                      )
                    }
                    style={{
                      width: "100%",
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "10px",
                      padding:
                        "10px 12px",
                      background:
                        "transparent",
                      border: "none",
                      borderRadius:
                        "8px",
                      cursor:
                        "pointer",
                      fontSize:
                        "13px",
                      color:
                        "#374151",
                    }}
                  >

                    <FiSettings
                      size={16}
                    />

                    Settings

                  </button>

                </div>

              </div>

            )}

          </div>

        </div>

      </div>


      {/* =================================================
          STATISTICS
      ================================================= */}

      <div className="metrics-grid">

        <div className="metric-card">

          <div className="metric-icon">
            <FiUsers />
          </div>

          <div className="metric-data">

            <h3>
              {totalEmployees}
            </h3>

            <p>
              Total Staff
            </p>

          </div>

        </div>


        <div className="metric-card">

          <div className="metric-icon success">

            <FiUserCheck />

          </div>

          <div className="metric-data">

            <h3>
              {activeEmployees}
            </h3>

            <p>
              Active Today
            </p>

          </div>

        </div>


        <div className="metric-card">

          <div className="metric-icon warning">

            <FiClock />

          </div>

          <div className="metric-data">

            <h3>
              {employeesOnLeave}
            </h3>

            <p>
              On Leave
            </p>

          </div>

        </div>


        <div className="metric-card">

          <div className="metric-icon danger">

            <FiUserMinus />

          </div>

          <div className="metric-data">

            <h3>
              {inactiveEmployees}
            </h3>

            <p>
              Inactive
            </p>

          </div>

        </div>

      </div>


      {/* =================================================
          EMPLOYEE TABLE
      ================================================= */}

      <div className="table-container">

        {/* SEARCH & FILTER */}

        <div className="table-header-tools">

          <div className="search-box">

            <FiSearch
              className="search-icon"
            />

            <input
              type="text"
              placeholder="Search by name, email, or ID..."
              value={search}
              onChange={(e) =>
                setSearch(
                  e.target.value
                )
              }
            />

          </div>


          <div className="filter-group">

            <label>
              Department:
            </label>

            <select
              value={selectedDept}
              onChange={(e) =>
                setSelectedDept(
                  e.target.value
                )
              }
            >

              <option value="All">
                All Departments
              </option>

              <option value="Engineering">
                Engineering
              </option>

              <option value="Design">
                Design
              </option>

              <option value="Human Resources">
                Human Resources
              </option>

              <option value="Marketing">
                Marketing
              </option>

            </select>

          </div>

        </div>


        {/* TABLE */}

        <table className="data-table">

          <thead>

            <tr>

              <th>
                Employee Name
              </th>

              <th>
                Role
              </th>

              <th>
                ID
              </th>

              <th>
                Department
              </th>

              <th>
                Status
              </th>

              <th>
                Joined Date
              </th>

            </tr>

          </thead>


          <tbody>

            {filteredEmployees.length >
            0 ? (

              filteredEmployees.map(
                (emp) => (

                  <tr key={emp.id}>

                    <td>

                      <div className="user-details">

                        <strong className="user-name">
                          {emp.name}
                        </strong>

                        <span className="user-email">
                          {emp.email}
                        </span>

                      </div>

                    </td>


                    <td>
                      {emp.role}
                    </td>


                    <td>
                      <code>
                        {emp.id}
                      </code>
                    </td>


                    <td>

                      <span className="dept-pill">
                        {emp.dept}
                      </span>

                    </td>


                    <td>

                      <span
                        className={`badge ${
                          emp.status ===
                          "Active"
                            ? "badge-success"
                            : emp.status ===
                              "On Leave"
                            ? "badge-warning"
                            : "badge-danger"
                        }`}
                      >
                        {emp.status}
                      </span>

                    </td>


                    <td>
                      {emp.joinDate}
                    </td>

                  </tr>

                )
              )

            ) : (

              <tr>

                <td
                  colSpan="6"
                  className="empty-state"
                >
                  No employees found
                  matching your filter
                  criteria.
                </td>

              </tr>

            )}

          </tbody>

        </table>

      </div>


      {/* =================================================
          EDIT PROFILE MODAL
      ================================================= */}

      {isEditProfileOpen && (

        <div
          className="modal-overlay"
          onClick={() =>
            setIsEditProfileOpen(false)
          }
        >

          <div
            className="modal-container"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            {/* HEADER */}

            <div className="modal-header">

              <h2>
                Edit Profile
              </h2>

              <button
                className="close-btn"
                onClick={() =>
                  setIsEditProfileOpen(
                    false
                  )
                }
              >
                <FiX />
              </button>

            </div>


            {/* FORM */}

            <form
              onSubmit={
                handleSaveProfile
              }
              className="modal-form"
            >

              {/* PROFILE PICTURE */}

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "center",
                  marginBottom:
                    "20px",
                }}
              >

                <div
                  style={{
                    position:
                      "relative",
                  }}
                >

                  {editProfile.picture ? (

                    <img
                      src={
                        editProfile.picture
                      }
                      alt="Profile"
                      style={{
                        width: "90px",
                        height: "90px",
                        borderRadius:
                          "50%",
                        objectFit:
                          "cover",
                      }}
                    />

                  ) : (

                    <div
                      style={{
                        width: "90px",
                        height: "90px",
                        borderRadius:
                          "50%",
                        background:
                          "#eef2ff",
                        color:
                          "#4f46e5",
                        display: "flex",
                        alignItems:
                          "center",
                        justifyContent:
                          "center",
                        fontSize:
                          "32px",
                        fontWeight:
                          "700",
                      }}
                    >
                      {editProfile.name
                        ?.charAt(0)
                        ?.toUpperCase() ||
                        "U"}
                    </div>

                  )}

                  <label
                    style={{
                      position:
                        "absolute",
                      bottom: "0",
                      right: "0",
                      width: "30px",
                      height: "30px",
                      borderRadius:
                        "50%",
                      background:
                        "#4f46e5",
                      color:
                        "#ffffff",
                      display: "flex",
                      alignItems:
                        "center",
                      justifyContent:
                        "center",
                      cursor:
                        "pointer",
                    }}
                  >

                    <FiCamera
                      size={15}
                    />

                    <input
                      type="file"
                      accept="image/*"
                      onChange={
                        handleProfilePicture
                      }
                      style={{
                        display:
                          "none",
                      }}
                    />

                  </label>

                </div>

              </div>


              {/* NAME */}

              <div className="form-group">

                <label>
                  Full Name
                </label>

                <div
                  className="input-wrapper"
                >

                  <FiUser
                    className="input-icon"
                  />

                  <input
                    type="text"
                    value={
                      editProfile.name
                    }
                    onChange={(e) =>
                      setEditProfile({
                        ...editProfile,
                        name:
                          e.target.value,
                      })
                    }
                    required
                  />

                </div>

              </div>


              {/* PHONE */}

              <div className="form-group">

                <label>
                  Phone Number
                </label>

                <div
                  className="input-wrapper"
                >

                  <FiPhone
                    className="input-icon"
                  />

                  <input
                    type="tel"
                    placeholder="+91 98765 43210"
                    value={
                      editProfile.phone
                    }
                    onChange={(e) =>
                      setEditProfile({
                        ...editProfile,
                        phone:
                          e.target.value,
                      })
                    }
                  />

                </div>

              </div>


              {/* EMAIL */}

              <div className="form-group">

                <label>
                  Email Address
                </label>

                <div
                  className="input-wrapper"
                >

                  <FiMail
                    className="input-icon"
                  />

                  <input
                    type="email"
                    value={
                      editProfile.email
                    }
                    onChange={(e) =>
                      setEditProfile({
                        ...editProfile,
                        email:
                          e.target.value,
                      })
                    }
                    required
                  />

                </div>

              </div>


              {/* ACTIONS */}

              <div className="modal-actions">

                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() =>
                    setIsEditProfileOpen(
                      false
                    )
                  }
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="btn-primary"
                >
                  Save Changes
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </div>
  );
}