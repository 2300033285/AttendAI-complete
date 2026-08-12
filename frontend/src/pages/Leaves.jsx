import React, { useState } from "react";
import {
  Plus,
  Search,
  Check,
  X,
  Calendar as CalendarIcon,
  Clock,
  CheckCircle2,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Leaves() {
  const { user } = useAuth();

  // =====================================================
  // USER ROLE
  // =====================================================

  const userRole = user?.role?.toLowerCase() || "employee";

  const isHR =
    userRole === "hr" ||
    userRole === "admin";

  const isEmployee = !isHR;

  // =====================================================
  // STATE
  // =====================================================

  const [activeTab, setActiveTab] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const [isModalOpen, setIsModalOpen] = useState(false);

  // =====================================================
  // FORM DATA
  // =====================================================

  const [formData, setFormData] = useState({
    employee: user?.name || "",
    type: "Annual Leave",
    fromDate: "",
    toDate: "",
    reason: "",
  });

  // =====================================================
  // LEAVE REQUESTS
  // =====================================================

  const [leaveRequests, setLeaveRequests] = useState([
    {
      id: 1,
      employee: "Rahul Sharma",
      type: "Annual Leave",
      fromDate: "Jul 24, 2026",
      toDate: "Jul 25, 2026",
      days: 2,
      reason: "Medical checkup and personal work",
      status: "Pending",
      appliedOn: "Jul 22, 2026",
    },
    {
      id: 2,
      employee: "Priya Patel",
      type: "Sick Leave",
      fromDate: "Jul 21, 2026",
      toDate: "Jul 21, 2026",
      days: 1,
      reason: "High fever and rest",
      status: "Approved",
      appliedOn: "Jul 20, 2026",
    },
    {
      id: 3,
      employee: "Arjun Kumar",
      type: "Casual Leave",
      fromDate: "Jul 15, 2026",
      toDate: "Jul 16, 2026",
      days: 2,
      reason: "Family function",
      status: "Rejected",
      appliedOn: "Jul 12, 2026",
    },
    {
      id: 4,
      employee: "Sneha Rao",
      type: "Maternity Leave",
      fromDate: "Aug 01, 2026",
      toDate: "Oct 31, 2026",
      days: 90,
      reason: "Maternity rest",
      status: "Approved",
      appliedOn: "Jul 10, 2026",
    },
  ]);

  // =====================================================
  // APPROVE / REJECT
  // HR AND ADMIN ONLY
  // =====================================================

  const handleStatusChange = (id, newStatus) => {
    // Employee cannot approve or reject
    if (!isHR) {
      return;
    }

    setLeaveRequests((prev) =>
      prev.map((request) =>
        request.id === id
          ? {
            ...request,
            status: newStatus,
          }
          : request
      )
    );
  };

  // =====================================================
  // APPLY FOR LEAVE
  // EMPLOYEE ONLY
  // =====================================================

  const handleApplyLeave = (e) => {
    e.preventDefault();

    if (!formData.fromDate || !formData.toDate) {
      alert("Please select From Date and To Date.");
      return;
    }

    const start = new Date(formData.fromDate);
    const end = new Date(formData.toDate);

    if (end < start) {
      alert("To Date cannot be earlier than From Date.");
      return;
    }

    // Calculate number of days
    const diffTime = end.getTime() - start.getTime();

    const diffDays =
      Math.ceil(
        diffTime / (1000 * 60 * 60 * 24)
      ) + 1;

    // Format date
    const formatDate = (date) => {
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
        year: "numeric",
      });
    };

    const newRequest = {
      id: Date.now(),

      employee:
        user?.name ||
        formData.employee ||
        "Employee",

      type: formData.type,

      fromDate: formatDate(start),

      toDate: formatDate(end),

      days: diffDays,

      reason:
        formData.reason.trim() ||
        "No reason provided",

      status: "Pending",

      appliedOn: formatDate(new Date()),
    };

    setLeaveRequests((prev) => [
      newRequest,
      ...prev,
    ]);

    // Close modal
    setIsModalOpen(false);

    // Reset form
    setFormData({
      employee: user?.name || "",
      type: "Annual Leave",
      fromDate: "",
      toDate: "",
      reason: "",
    });
  };

  // =====================================================
  // FILTER REQUESTS
  // =====================================================

  const filteredRequests = leaveRequests.filter(
    (request) => {

      // -------------------------------------------------
      // EMPLOYEE:
      // Only show their own leave requests
      // -------------------------------------------------

      if (isEmployee) {
        const currentUserName =
          user?.name?.toLowerCase();

        const requestEmployee =
          request.employee?.toLowerCase();

        if (
          currentUserName &&
          requestEmployee !== currentUserName
        ) {
          return false;
        }
      }

      // -------------------------------------------------
      // SEARCH
      // -------------------------------------------------

      const matchesSearch =
        request.employee
          .toLowerCase()
          .includes(
            searchTerm.toLowerCase()
          ) ||
        request.type
          .toLowerCase()
          .includes(
            searchTerm.toLowerCase()
          );

      // -------------------------------------------------
      // STATUS FILTER
      // -------------------------------------------------

      if (activeTab === "pending") {
        return (
          matchesSearch &&
          request.status === "Pending"
        );
      }

      if (activeTab === "approved") {
        return (
          matchesSearch &&
          request.status === "Approved"
        );
      }

      if (activeTab === "rejected") {
        return (
          matchesSearch &&
          request.status === "Rejected"
        );
      }

      return matchesSearch;
    }
  );

  // =====================================================
  // COUNTS
  // =====================================================

  const pendingCount = leaveRequests.filter(
    (request) =>
      request.status === "Pending"
  ).length;

  const approvedCount = leaveRequests.filter(
    (request) =>
      request.status === "Approved"
  ).length;

  // =====================================================
  // PAGE TITLE / DESCRIPTION
  // =====================================================

  const pageTitle = isHR
    ? "Leave Management"
    : "My Leave Requests";

  const pageDescription = isHR
    ? "Review, approve, and track employee leave applications."
    : "Apply for leave and track your leave applications.";

  // =====================================================
  // UI
  // =====================================================

  return (
    <>
      {/* =================================================
          PAGE HEADER
      ================================================= */}

      <div className="page-header">

        <div>
          <h1>
            {pageTitle}
          </h1>

          <p
            style={{
              color:
                "var(--text-secondary)",
              marginTop: "0.25rem",
            }}
          >
            {pageDescription}
          </p>
        </div>

        {/* =================================================
            APPLY FOR LEAVE

            EMPLOYEE ONLY
        ================================================= */}

        {isEmployee && (
          <button
            className="btn-primary"
            onClick={() =>
              setIsModalOpen(true)
            }
          >
            <Plus size={16} />

            Apply for Leave
          </button>
        )}

      </div>

      {/* =================================================
          METRICS
      ================================================= */}

      <div className="metrics-grid">

        {/* PENDING */}

        <div className="metric-card">

          <div className="metric-icon">
            <Clock size={20} />
          </div>

          <div className="metric-data">

            <h3>
              {pendingCount}
            </h3>

            <p>
              Pending Approval
            </p>

          </div>

        </div>

        {/* APPROVED */}

        <div className="metric-card">

          <div
            className="metric-icon"
            style={{
              background: "#dcfce7",
              color: "#166534",
            }}
          >
            <CheckCircle2 size={20} />
          </div>

          <div className="metric-data">

            <h3>
              {approvedCount}
            </h3>

            <p>
              Approved This Month
            </p>

          </div>

        </div>

        {/* CURRENTLY ON LEAVE */}

        <div className="metric-card">

          <div
            className="metric-icon"
            style={{
              background: "#e0f2fe",
              color: "#075985",
            }}
          >
            <CalendarIcon size={20} />
          </div>

          <div className="metric-data">

            <h3>
              12
            </h3>

            <p>
              Currently On Leave
            </p>

          </div>

        </div>

      </div>

      {/* =================================================
          TABLE
      ================================================= */}

      <div className="table-container">

        {/* TABLE TOOLS */}

        <div className="table-header-tools">

          {/* SEARCH */}

          <div
            className="input-wrapper"
            style={{
              width: "280px",
            }}
          >

            <Search
              size={16}
              className="input-icon"
            />

            <input
              type="text"
              placeholder={
                isHR
                  ? "Search employee or leave type..."
                  : "Search leave type..."
              }
              value={searchTerm}
              onChange={(e) =>
                setSearchTerm(
                  e.target.value
                )
              }
              style={{
                paddingLeft: "2.2rem",
              }}
            />

          </div>

          {/* FILTER TABS */}

          <div
            style={{
              display: "flex",
              gap: "0.5rem",
            }}
          >

            {[
              "all",
              "pending",
              "approved",
              "rejected",
            ].map((tab) => (

              <button
                key={tab}
                onClick={() =>
                  setActiveTab(tab)
                }
                className={`nav-item ${activeTab === tab
                    ? "active"
                    : ""
                  }`}
                style={{
                  padding:
                    "0.4rem 0.85rem",
                  fontSize:
                    "0.85rem",
                  textTransform:
                    "capitalize",
                  borderRadius:
                    "var(--radius-sm)",
                }}
              >
                {tab}
              </button>

            ))}

          </div>

        </div>

        {/* =================================================
            TABLE
        ================================================= */}

        <table className="data-table">

          <thead>

            <tr>

              {/* HR sees employee name */}

              {isHR && (
                <th>
                  Employee
                </th>
              )}

              <th>
                Leave Type
              </th>

              <th>
                Duration / Dates
              </th>

              <th>
                Reason
              </th>

              <th>
                Applied On
              </th>

              <th>
                Status
              </th>

              {/* HR ONLY */}

              {isHR && (
                <th
                  style={{
                    textAlign: "right",
                  }}
                >
                  Actions
                </th>
              )}

            </tr>

          </thead>

          <tbody>

            {filteredRequests.length > 0 ? (

              filteredRequests.map(
                (request) => (

                  <tr
                    key={request.id}
                  >

                    {/* =================================================
                        EMPLOYEE NAME
                        HR ONLY
                    ================================================= */}

                    {isHR && (
                      <td>
                        <strong>
                          {request.employee}
                        </strong>
                      </td>
                    )}

                    {/* LEAVE TYPE */}

                    <td>
                      {request.type}
                    </td>

                    {/* DURATION */}

                    <td>

                      <div>
                        {request.fromDate}{" "}
                        -{" "}
                        {request.toDate}
                      </div>

                      <small
                        style={{
                          color:
                            "var(--text-secondary)",
                        }}
                      >
                        (
                        {request.days}{" "}
                        {request.days === 1
                          ? "day"
                          : "days"}
                        )
                      </small>

                    </td>

                    {/* REASON */}

                    <td
                      style={{
                        maxWidth:
                          "220px",
                        color:
                          "var(--text-secondary)",
                      }}
                    >
                      {request.reason}
                    </td>

                    {/* APPLIED ON */}

                    <td
                      style={{
                        color:
                          "var(--text-secondary)",
                      }}
                    >
                      {request.appliedOn}
                    </td>

                    {/* STATUS */}

                    <td>

                      <span
                        className={`badge ${request.status ===
                            "Approved"
                            ? "badge-success"
                            : request.status ===
                              "Pending"
                              ? "badge-warning"
                              : "badge-danger"
                          }`}
                      >
                        {request.status}
                      </span>

                    </td>

                    {/* =================================================
                        HR ACTIONS ONLY

                        APPROVE + REJECT

                        EMPLOYEE WILL NOT SEE THIS COLUMN
                    ================================================= */}

                    {isHR && (

                      <td
                        style={{
                          textAlign:
                            "right",
                        }}
                      >

                        {request.status ===
                          "Pending" ? (

                          <div
                            style={{
                              display:
                                "flex",
                              gap:
                                "0.4rem",
                              justifyContent:
                                "flex-end",
                            }}
                          >

                            {/* APPROVE */}

                            <button
                              onClick={() =>
                                handleStatusChange(
                                  request.id,
                                  "Approved"
                                )
                              }
                              className="btn-primary"
                              style={{
                                padding:
                                  "0.35rem 0.65rem",
                                fontSize:
                                  "0.8rem",
                                background:
                                  "#16a34a",
                              }}
                            >

                              <Check
                                size={14}
                              />

                              Approve

                            </button>

                            {/* REJECT */}

                            <button
                              onClick={() =>
                                handleStatusChange(
                                  request.id,
                                  "Rejected"
                                )
                              }
                              className="btn-primary"
                              style={{
                                padding:
                                  "0.35rem 0.65rem",
                                fontSize:
                                  "0.8rem",
                                background:
                                  "#dc2626",
                              }}
                            >

                              <X
                                size={14}
                              />

                              Reject

                            </button>

                          </div>

                        ) : (

                          <span
                            style={{
                              fontSize:
                                "0.85rem",
                              color:
                                "var(--text-muted)",
                            }}
                          >
                            Completed
                          </span>

                        )}

                      </td>

                    )}

                  </tr>

                )

              )

            ) : (

              <tr>

                <td
                  colSpan={
                    isHR ? 7 : 6
                  }
                  style={{
                    textAlign:
                      "center",
                    padding:
                      "2rem",
                    color:
                      "var(--text-secondary)",
                  }}
                >
                  No leave requests
                  found.
                </td>

              </tr>

            )}

          </tbody>

        </table>

      </div>

      {/* =================================================
          APPLY FOR LEAVE MODAL
          
          EMPLOYEE ONLY
      ================================================= */}

      {isModalOpen && isEmployee && (

        <div className="modal-overlay">

          <div className="modal-container">

            {/* MODAL HEADER */}

            <div className="modal-header">

              <h2>
                Apply for Leave
              </h2>

              <button
                className="close-btn"
                onClick={() =>
                  setIsModalOpen(false)
                }
              >
                <X size={18} />
              </button>

            </div>

            {/* FORM */}

            <form
              onSubmit={
                handleApplyLeave
              }
              className="modal-form"
            >

              {/* EMPLOYEE NAME */}

              <div className="form-group">

                <label>
                  Employee Name
                </label>

                <input
                  type="text"
                  value={
                    user?.name ||
                    formData.employee
                  }
                  disabled
                />

              </div>

              {/* LEAVE TYPE */}

              <div className="form-group">

                <label>
                  Leave Type *
                </label>

                <select
                  value={
                    formData.type
                  }
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      type:
                        e.target.value,
                    })
                  }
                >

                  <option value="Annual Leave">
                    Annual Leave
                  </option>

                  <option value="Casual Leave">
                    Casual Leave
                  </option>

                  <option value="Sick Leave">
                    Sick Leave
                  </option>

                  <option value="Maternity Leave">
                    Maternity Leave
                  </option>

                </select>

              </div>

              {/* DATES */}

              <div className="form-row">

                <div className="form-group">

                  <label>
                    From Date *
                  </label>

                  <input
                    type="date"
                    required
                    value={
                      formData.fromDate
                    }
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        fromDate:
                          e.target.value,
                      })
                    }
                  />

                </div>

                <div className="form-group">

                  <label>
                    To Date *
                  </label>

                  <input
                    type="date"
                    required
                    value={
                      formData.toDate
                    }
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        toDate:
                          e.target.value,
                      })
                    }
                  />

                </div>

              </div>

              {/* REASON */}

              <div className="form-group">

                <label>
                  Reason
                </label>

                <input
                  type="text"
                  placeholder="Reason for leave..."
                  value={
                    formData.reason
                  }
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      reason:
                        e.target.value,
                    })
                  }
                />

              </div>

              {/* MODAL BUTTONS */}

              <div className="modal-actions">

                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() =>
                    setIsModalOpen(false)
                  }
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="btn-primary"
                >
                  Submit Application
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </>
  );
}