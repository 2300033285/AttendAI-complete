import React, { useMemo, useState } from "react";
import {
  BriefcaseBusiness,
  Plus,
  Search,
  MapPin,
  Users,
  CalendarDays,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  X,
  Building2,
  Clock3,
  ChevronDown,
} from "lucide-react";

export default function Recruitment() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  const [jobs, setJobs] = useState([
    {
      id: 1,
      title: "Frontend Developer",
      department: "Engineering",
      location: "Hyderabad",
      type: "Full-time",
      applicants: 32,
      postedDate: "July 20, 2026",
      status: "Open",
      description:
        "We are looking for a skilled Frontend Developer to build modern and responsive web applications.",
    },
    {
      id: 2,
      title: "Backend Developer",
      department: "Engineering",
      location: "Bangalore",
      type: "Full-time",
      applicants: 24,
      postedDate: "July 18, 2026",
      status: "Open",
      description:
        "Looking for a Backend Developer experienced in APIs, databases, and scalable backend systems.",
    },
    {
      id: 3,
      title: "HR Executive",
      department: "Human Resources",
      location: "Vijayawada",
      type: "Full-time",
      applicants: 18,
      postedDate: "July 15, 2026",
      status: "Open",
      description:
        "HR Executive responsible for employee coordination, recruitment, and HR operations.",
    },
    {
      id: 4,
      title: "Data Analyst",
      department: "Analytics",
      location: "Hyderabad",
      type: "Full-time",
      applicants: 27,
      postedDate: "July 12, 2026",
      status: "Closed",
      description:
        "Analyze business data and generate meaningful reports and insights for decision making.",
    },
    {
      id: 5,
      title: "UI/UX Designer",
      department: "Design",
      location: "Remote",
      type: "Full-time",
      applicants: 15,
      postedDate: "July 10, 2026",
      status: "Open",
      description:
        "Create intuitive, accessible, and visually appealing user experiences for AttendAI.",
    },
  ]);

  const [modalType, setModalType] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);

  const [formData, setFormData] = useState({
    title: "",
    department: "",
    location: "",
    type: "Full-time",
    status: "Open",
    description: "",
  });

  /* =====================================================
     FILTER JOBS
     ===================================================== */

  const filteredJobs = useMemo(() => {
    return jobs.filter((job) => {
      const search = searchTerm.toLowerCase().trim();

      const matchesSearch =
        job.title.toLowerCase().includes(search) ||
        job.department.toLowerCase().includes(search) ||
        job.location.toLowerCase().includes(search);

      const matchesStatus =
        statusFilter === "All" || job.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [jobs, searchTerm, statusFilter]);

  /* =====================================================
     STATISTICS
     ===================================================== */

  const totalPositions = jobs.length;

  const openPositions = jobs.filter(
    (job) => job.status === "Open"
  ).length;

  const totalApplicants = jobs.reduce(
    (total, job) => total + Number(job.applicants || 0),
    0
  );

  const newThisWeek = 3;

  /* =====================================================
     OPEN ADD MODAL
     ===================================================== */

  const openAddModal = () => {
    setFormData({
      title: "",
      department: "",
      location: "",
      type: "Full-time",
      status: "Open",
      description: "",
    });

    setSelectedJob(null);
    setModalType("add");
  };

  /* =====================================================
     OPEN EDIT MODAL
     ===================================================== */

  const openEditModal = (job) => {
    setSelectedJob(job);

    setFormData({
      title: job.title,
      department: job.department,
      location: job.location,
      type: job.type,
      status: job.status,
      description: job.description || "",
    });

    setModalType("edit");
  };

  /* =====================================================
     OPEN VIEW MODAL
     ===================================================== */

  const openViewModal = (job) => {
    setSelectedJob(job);
    setModalType("view");
  };

  /* =====================================================
     CLOSE MODAL
     ===================================================== */

  const closeModal = () => {
    setModalType(null);
    setSelectedJob(null);
  };

  /* =====================================================
     HANDLE FORM CHANGE
     ===================================================== */

  const handleFormChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  /* =====================================================
     ADD / EDIT JOB
     ===================================================== */

  const handleSubmit = (event) => {
    event.preventDefault();

    if (
      !formData.title.trim() ||
      !formData.department.trim() ||
      !formData.location.trim()
    ) {
      window.alert(
        "Please fill in Job Title, Department, and Location."
      );
      return;
    }

    if (modalType === "add") {
      const newJob = {
        id: Date.now(),
        title: formData.title.trim(),
        department: formData.department.trim(),
        location: formData.location.trim(),
        type: formData.type,
        status: formData.status,
        applicants: 0,
        postedDate: "July 29, 2026",
        description: formData.description.trim(),
      };

      setJobs((previous) => [newJob, ...previous]);
    }

    if (modalType === "edit" && selectedJob) {
      setJobs((previous) =>
        previous.map((job) =>
          job.id === selectedJob.id
            ? {
                ...job,
                title: formData.title.trim(),
                department: formData.department.trim(),
                location: formData.location.trim(),
                type: formData.type,
                status: formData.status,
                description: formData.description.trim(),
              }
            : job
        )
      );
    }

    closeModal();
  };

  /* =====================================================
     DELETE JOB
     ===================================================== */

  const handleDelete = (id) => {
    const job = jobs.find((item) => item.id === id);

    const confirmed = window.confirm(
      `Are you sure you want to delete "${job?.title}"?`
    );

    if (!confirmed) return;

    setJobs((previous) =>
      previous.filter((item) => item.id !== id)
    );
  };

  /* =====================================================
     RENDER
     ===================================================== */

  return (
    <div className="page-content recruitment-page">

      {/* =================================================
          PAGE HEADER
      ================================================= */}

      <div className="page-header recruitment-page-header">

        <div>
          <div className="dashboard-eyebrow recruitment-eyebrow">
            <BriefcaseBusiness size={14} />
            RECRUITMENT
          </div>

          <h1>Recruitment</h1>

          <p className="subtext">
            Manage open positions, job postings, and applicants.
          </p>
        </div>

        <button
          className="btn-primary recruitment-add-btn"
          onClick={openAddModal}
        >
          <Plus size={17} />
          Add Job Opening
        </button>

      </div>

      {/* =================================================
          STATISTICS
      ================================================= */}

      <div className="recruitment-stats-grid">

        <div className="recruitment-stat-card">
          <div className="recruitment-stat-icon blue">
            <BriefcaseBusiness size={20} />
          </div>

          <div className="recruitment-stat-content">
            <span>Total Positions</span>
            <h3>{totalPositions}</h3>
          </div>
        </div>

        <div className="recruitment-stat-card">
          <div className="recruitment-stat-icon green">
            <BriefcaseBusiness size={20} />
          </div>

          <div className="recruitment-stat-content">
            <span>Open Positions</span>
            <h3>{openPositions}</h3>
          </div>
        </div>

        <div className="recruitment-stat-card">
          <div className="recruitment-stat-icon purple">
            <Users size={20} />
          </div>

          <div className="recruitment-stat-content">
            <span>Total Applicants</span>
            <h3>{totalApplicants}</h3>
          </div>
        </div>

        <div className="recruitment-stat-card">
          <div className="recruitment-stat-icon orange">
            <CalendarDays size={20} />
          </div>

          <div className="recruitment-stat-content">
            <span>New This Week</span>
            <h3>{newThisWeek}</h3>
          </div>
        </div>

      </div>

      {/* =================================================
          JOB OPENINGS TABLE
      ================================================= */}

      <div className="table-container recruitment-table-container">

        <div className="table-header-tools recruitment-table-header">

          <div className="recruitment-table-title">
            <strong className="dashboard-section-title">
              Job Openings
            </strong>

            <p className="subtext">
              View and manage current job positions
            </p>
          </div>

          <div className="recruitment-filters">

            {/* SEARCH */}

            <div className="search-box recruitment-search">

              <Search
                size={16}
                className="search-icon"
              />

              <input
                type="text"
                placeholder="Search jobs..."
                value={searchTerm}
                onChange={(event) =>
                  setSearchTerm(event.target.value)
                }
              />

              {searchTerm && (
                <button
                  className="search-clear-btn"
                  onClick={() => setSearchTerm("")}
                  type="button"
                >
                  <X size={14} />
                </button>
              )}

            </div>

            {/* STATUS FILTER */}

            <div className="recruitment-select-wrapper">

              <select
                value={statusFilter}
                onChange={(event) =>
                  setStatusFilter(event.target.value)
                }
                className="recruitment-status-filter"
              >
                <option value="All">All Status</option>
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
              </select>

              <ChevronDown
                size={14}
                className="recruitment-select-icon"
              />

            </div>

          </div>

        </div>

        {/* =================================================
            TABLE
        ================================================= */}

        <div className="table-responsive">

          <table className="data-table recruitment-table">

            <thead>
              <tr>
                <th>Job Position</th>
                <th>Department</th>
                <th>Location</th>
                <th>Type</th>
                <th>Applicants</th>
                <th>Posted</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {filteredJobs.length > 0 ? (

                filteredJobs.map((job) => (

                  <tr key={job.id}>

                    {/* JOB POSITION */}

                    <td>
                      <div className="job-title-cell">

                        <div className="job-icon">
                          <BriefcaseBusiness size={15} />
                        </div>

                        <strong>{job.title}</strong>

                      </div>
                    </td>

                    {/* DEPARTMENT */}

                    <td>
                      <span className="job-department">
                        {job.department}
                      </span>
                    </td>

                    {/* LOCATION */}

                    <td>
                      <div className="job-location">

                        <MapPin size={14} />

                        <span>{job.location}</span>

                      </div>
                    </td>

                    {/* TYPE */}

                    <td>
                      <span className="job-type">
                        {job.type}
                      </span>
                    </td>

                    {/* APPLICANTS */}

                    <td>
                      <div className="applicant-count">

                        <Users size={14} />

                        <span>{job.applicants}</span>

                      </div>
                    </td>

                    {/* POSTED */}

                    <td>
                      <span className="job-posted-date">
                        {job.postedDate}
                      </span>
                    </td>

                    {/* STATUS */}

                    <td>

                      <span
                        className={
                          job.status === "Open"
                            ? "badge badge-success"
                            : "badge badge-danger"
                        }
                      >
                        {job.status}
                      </span>

                    </td>

                    {/* ACTIONS */}

                    <td>

                      <div className="job-actions">

                        <button
                          type="button"
                          className="table-action-btn"
                          title="View Job"
                          onClick={() =>
                            openViewModal(job)
                          }
                        >
                          <Eye size={15} />
                        </button>

                        <button
                          type="button"
                          className="table-action-btn"
                          title="Edit Job"
                          onClick={() =>
                            openEditModal(job)
                          }
                        >
                          <Edit size={15} />
                        </button>

                        <button
                          type="button"
                          className="table-action-btn danger"
                          title="Delete Job"
                          onClick={() =>
                            handleDelete(job.id)
                          }
                        >
                          <Trash2 size={15} />
                        </button>

                        <button
                          type="button"
                          className="table-action-btn"
                          title="More Options"
                        >
                          <MoreVertical size={15} />
                        </button>

                      </div>

                    </td>

                  </tr>

                ))

              ) : (

                <tr>
                  <td
                    colSpan="8"
                    className="empty-table-message"
                  >
                    <div className="empty-recruitment-state">

                      <BriefcaseBusiness size={32} />

                      <strong>
                        No job openings found
                      </strong>

                      <span>
                        Try changing your search or filter.
                      </span>

                    </div>
                  </td>
                </tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

      {/* =================================================
          ADD / EDIT MODAL
      ================================================= */}

      {(modalType === "add" || modalType === "edit") && (

        <div
          className="modal-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeModal();
            }
          }}
        >

          <div className="modal-container recruitment-modal">

            <div className="modal-header">

              <div>
                <span className="modal-eyebrow">
                  <BriefcaseBusiness size={13} />
                  RECRUITMENT
                </span>

                <h2>
                  {modalType === "add"
                    ? "Add Job Opening"
                    : "Edit Job Opening"}
                </h2>

                <p className="modal-description">
                  {modalType === "add"
                    ? "Create a new job position."
                    : "Update the job position details."}
                </p>
              </div>

              <button
                className="close-btn"
                type="button"
                onClick={closeModal}
              >
                <X size={20} />
              </button>

            </div>

            <form
              className="modal-form"
              onSubmit={handleSubmit}
            >

              <div className="form-group">

                <label htmlFor="title">
                  Job Title
                </label>

                <div className="modal-input-wrapper">
                  <BriefcaseBusiness size={16} />

                  <input
                    id="title"
                    name="title"
                    type="text"
                    placeholder="e.g. Frontend Developer"
                    value={formData.title}
                    onChange={handleFormChange}
                    required
                  />
                </div>

              </div>

              <div className="form-row">

                <div className="form-group">

                  <label htmlFor="department">
                    Department
                  </label>

                  <div className="modal-input-wrapper">
                    <Building2 size={16} />

                    <input
                      id="department"
                      name="department"
                      type="text"
                      placeholder="e.g. Engineering"
                      value={formData.department}
                      onChange={handleFormChange}
                      required
                    />
                  </div>

                </div>

                <div className="form-group">

                  <label htmlFor="location">
                    Location
                  </label>

                  <div className="modal-input-wrapper">
                    <MapPin size={16} />

                    <input
                      id="location"
                      name="location"
                      type="text"
                      placeholder="e.g. Hyderabad"
                      value={formData.location}
                      onChange={handleFormChange}
                      required
                    />
                  </div>

                </div>

              </div>

              <div className="form-row">

                <div className="form-group">

                  <label htmlFor="type">
                    Employment Type
                  </label>

                  <div className="modal-input-wrapper">

                    <Clock3 size={16} />

                    <select
                      id="type"
                      name="type"
                      value={formData.type}
                      onChange={handleFormChange}
                    >
                      <option value="Full-time">
                        Full-time
                      </option>

                      <option value="Part-time">
                        Part-time
                      </option>

                      <option value="Contract">
                        Contract
                      </option>

                      <option value="Internship">
                        Internship
                      </option>
                    </select>

                  </div>

                </div>

                <div className="form-group">

                  <label htmlFor="status">
                    Status
                  </label>

                  <div className="modal-input-wrapper">

                    <BriefcaseBusiness size={16} />

                    <select
                      id="status"
                      name="status"
                      value={formData.status}
                      onChange={handleFormChange}
                    >
                      <option value="Open">
                        Open
                      </option>

                      <option value="Closed">
                        Closed
                      </option>
                    </select>

                  </div>

                </div>

              </div>

              <div className="form-group">

                <label htmlFor="description">
                  Job Description
                </label>

                <textarea
                  id="description"
                  name="description"
                  rows="4"
                  placeholder="Enter job description..."
                  value={formData.description}
                  onChange={handleFormChange}
                />

              </div>

              <div className="modal-actions">

                <button
                  type="button"
                  className="btn-secondary"
                  onClick={closeModal}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="btn-primary"
                >
                  <Plus size={16} />

                  {modalType === "add"
                    ? "Create Job"
                    : "Save Changes"}
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

      {/* =================================================
          VIEW JOB MODAL
      ================================================= */}

      {modalType === "view" && selectedJob && (

        <div
          className="modal-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeModal();
            }
          }}
        >

          <div className="modal-container recruitment-view-modal">

            <div className="modal-header">

              <div>

                <span className="modal-eyebrow">
                  <BriefcaseBusiness size={13} />
                  JOB DETAILS
                </span>

                <h2>{selectedJob.title}</h2>

              </div>

              <button
                className="close-btn"
                type="button"
                onClick={closeModal}
              >
                <X size={20} />
              </button>

            </div>

            <div className="job-detail-status-row">

              <span
                className={
                  selectedJob.status === "Open"
                    ? "badge badge-success"
                    : "badge badge-danger"
                }
              >
                {selectedJob.status}
              </span>

              <span className="job-detail-applicants">
                <Users size={15} />
                {selectedJob.applicants} applicants
              </span>

            </div>

            <div className="job-detail-grid">

              <div className="job-detail-item">
                <span>Department</span>
                <strong>
                  <Building2 size={15} />
                  {selectedJob.department}
                </strong>
              </div>

              <div className="job-detail-item">
                <span>Location</span>
                <strong>
                  <MapPin size={15} />
                  {selectedJob.location}
                </strong>
              </div>

              <div className="job-detail-item">
                <span>Employment Type</span>
                <strong>
                  <Clock3 size={15} />
                  {selectedJob.type}
                </strong>
              </div>

              <div className="job-detail-item">
                <span>Posted Date</span>
                <strong>
                  <CalendarDays size={15} />
                  {selectedJob.postedDate}
                </strong>
              </div>

            </div>

            <div className="job-description-box">

              <h3>Job Description</h3>

              <p>
                {selectedJob.description ||
                  "No job description available."}
              </p>

            </div>

            <div className="modal-actions">

              <button
                type="button"
                className="btn-secondary"
                onClick={closeModal}
              >
                Close
              </button>

              <button
                type="button"
                className="btn-primary"
                onClick={() =>
                  openEditModal(selectedJob)
                }
              >
                <Edit size={15} />
                Edit Job
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}