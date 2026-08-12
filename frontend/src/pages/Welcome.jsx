import React from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  BarChart3,
  Brain,
  CalendarCheck,
  ChevronRight,
  Clock3,
  QrCode,
  ShieldCheck,
  Sparkles,
  Users,
  UserCheck,
  CheckCircle2,
  Sliders,
  TrendingUp,
  LogIn
} from "lucide-react";

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <main className="welcome-page">
      {/* ================= NAVBAR ================= */}
      <nav className="landing-navbar">
        <div className="brand">
          <div className="brand-logo">A</div>
          <span className="brand-name">
            Attend<span>AI</span>
          </span>
        </div>

        <div style={{ display: "flex", gap: "0.85rem", alignItems: "center" }}>
          <button
            className="hero-secondary-btn"
            style={{ padding: "0.55rem 1.1rem", fontSize: "0.9rem" }}
            onClick={() => navigate("/login")}
          >
            <LogIn size={16} />
            Log In
          </button>
          
          <button
            className="nav-login-btn"
            onClick={() => navigate("/register")}
          >
            Get Started
            <ArrowRight size={15} />
          </button>
        </div>
      </nav>

      {/* ================= HERO SECTION ================= */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <div className="eyebrow">
              <Sparkles size={14} />
              AI-POWERED WORKFORCE MANAGEMENT
            </div>

            <h1>
              Smarter Attendance.<br />
              <span>Better Workforce Management.</span>
            </h1>

            <p>
              AttendAI is an all-in-one workforce intelligence platform designed to eliminate manual registers, streamline employee management, automate leave workflows, and deliver real-time analytics.
            </p>

            <div className="hero-actions">
              <button
                className="hero-login-btn"
                onClick={() => navigate("/login")}
              >
                Log In to AttendAI
                <ArrowRight size={16} />
              </button>

              <button
                className="hero-secondary-btn"
                onClick={() =>
                  document
                    .getElementById("how-it-works")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                How It Works
                <ChevronRight size={16} />
              </button>
            </div>

            <div className="hero-trust">
              <div>
                <ShieldCheck size={16} />
                Secure Access
              </div>
              <div>
                <Brain size={16} />
                AI Insights
              </div>
              <div>
                <BarChart3 size={16} />
                Real-Time Reports
              </div>
            </div>
          </div>

          {/* DASHBOARD PREVIEW GRAPHIC */}
          <div className="hero-visual">
            <div className="dashboard-preview">
              <div className="preview-header">
                <div className="brand">
                  <div className="brand-logo" style={{ width: "28px", height: "28px", fontSize: "0.85rem" }}>A</div>
                  <strong style={{ fontSize: "0.95rem" }}>Attend<span>AI</span></strong>
                </div>

                <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                  Live System Overview
                </div>
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", margin: "0.5rem 0 1rem" }}>
                <div>
                  <strong style={{ fontSize: "1rem", display: "block" }}>Workforce Summary</strong>
                  <small style={{ color: "var(--text-secondary)", fontSize: "0.75rem" }}>Today's Live Tracking</small>
                </div>
                <span className="badge badge-success">● Active</span>
              </div>

              <div className="preview-stats">
                <div className="preview-stat-card">
                  <span>Total Staff</span>
                  <strong>248</strong>
                </div>
                <div className="preview-stat-card">
                  <span>Present</span>
                  <strong>221</strong>
                </div>
                <div className="preview-stat-card">
                  <span>On Leave</span>
                  <strong>12</strong>
                </div>
              </div>

              <div className="chart-heading" style={{ marginTop: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong style={{ fontSize: "0.85rem" }}>Weekly Attendance Rate</strong>
                <span style={{ fontSize: "0.85rem", fontWeight: "700", color: "var(--primary)" }}>92.4%</span>
              </div>

              <div className="chart-bars">
                {[45, 65, 52, 80, 70, 92, 85].map((height, index) => (
                  <div className="preview-bar-wrapper" key={index}>
                    <div className="preview-bar" style={{ height: `${height}%` }} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ================= WHAT IS ATTENDAI ================= */}
      <section className="hero-section" style={{ paddingTop: "1rem" }}>
        <div style={{ textAlign: "center", maxWidth: "750px", margin: "0 auto 3rem" }}>
          <span className="eyebrow">About AttendAI</span>
          <h2 style={{ fontSize: "2.25rem", fontWeight: "800", marginBottom: "0.85rem" }}>
            What is AttendAI?
          </h2>
          <p style={{ color: "var(--text-secondary)", fontSize: "1.1rem" }}>
            AttendAI is a modern HR tech platform engineered to solve employee tracking and workforce scheduling challenges. It connects employees, management, and HR operational metrics into one unified, intelligent cloud solution.
          </p>
        </div>

        <div className="metrics-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "1.5rem" }}>
          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.75rem" }}>
            <div className="metric-icon"><Users size={22} /></div>
            <h3 style={{ fontSize: "1.2rem", margin: "0.75rem 0 0.3rem" }}>Employee Directory</h3>
            <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
              Centralize employee profile data, manage department assignments, and configure role-based access control seamlessly.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.75rem" }}>
            <div className="metric-icon"><Clock3 size={22} /></div>
            <h3 style={{ fontSize: "1.2rem", margin: "0.75rem 0 0.3rem" }}>Attendance Tracking</h3>
            <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
              Instant QR check-ins, automated digital logs, accurate late-arrival detection, and active duration tracking.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.75rem" }}>
            <div className="metric-icon"><CalendarCheck size={22} /></div>
            <h3 style={{ fontSize: "1.2rem", margin: "0.75rem 0 0.3rem" }}>Leave Approvals</h3>
            <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
              Streamline employee leave applications (Sick, Casual, Annual) with single-click admin approval workflows.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.75rem" }}>
            <div className="metric-icon"><BarChart3 size={22} /></div>
            <h3 style={{ fontSize: "1.2rem", margin: "0.75rem 0 0.3rem" }}>Smart Analytics</h3>
            <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
              Export workforce reports, observe monthly attendance trends, and monitor team productivity metrics.
            </p>
          </div>
        </div>
      </section>

      {/* ================= HOW IT WORKS ================= */}
      <section className="hero-section" id="how-it-works" style={{ paddingTop: "2rem" }}>
        <div style={{ textAlign: "center", maxWidth: "650px", margin: "0 auto 3.5rem" }}>
          <span className="eyebrow">4-Step Process</span>
          <h2 style={{ fontSize: "2.25rem", fontWeight: "800", marginBottom: "0.75rem" }}>
            How AttendAI Works
          </h2>
          <p style={{ color: "var(--text-secondary)" }}>
            A streamlined workflow engineered to make workforce operations effortless for both managers and employees.
          </p>
        </div>

        <div className="metrics-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.5rem" }}>
          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.5rem", position: "relative" }}>
            <span style={{ fontSize: "0.8rem", fontWeight: "800", color: "var(--primary)", background: "var(--primary-light)", padding: "0.2rem 0.6rem", borderRadius: "var(--radius-full)" }}>Step 01</span>
            <div className="metric-icon" style={{ marginTop: "1rem" }}><QrCode size={22} /></div>
            <h3 style={{ fontSize: "1.1rem", margin: "0.75rem 0 0.25rem" }}>1. Scan & Check-in</h3>
            <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)" }}>
              Employees scan their workspace QR code using their phone or kiosk to record instant attendance.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.5rem" }}>
            <span style={{ fontSize: "0.8rem", fontWeight: "800", color: "var(--primary)", background: "var(--primary-light)", padding: "0.2rem 0.6rem", borderRadius: "var(--radius-full)" }}>Step 02</span>
            <div className="metric-icon" style={{ marginTop: "1rem" }}><UserCheck size={22} /></div>
            <h3 style={{ fontSize: "1.1rem", margin: "0.75rem 0 0.25rem" }}>2. Real-time Log</h3>
            <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)" }}>
              Check-in times are logged immediately in the live dashboard, marking users as On Time or Late automatically.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.5rem" }}>
            <span style={{ fontSize: "0.8rem", fontWeight: "800", color: "var(--primary)", background: "var(--primary-light)", padding: "0.2rem 0.6rem", borderRadius: "var(--radius-full)" }}>Step 03</span>
            <div className="metric-icon" style={{ marginTop: "1rem" }}><Sliders size={22} /></div>
            <h3 style={{ fontSize: "1.1rem", margin: "0.75rem 0 0.25rem" }}>3. Manage Requests</h3>
            <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)" }}>
              Employees submit leave requests online, while managers review, approve, or reject requests with one click.
            </p>
          </div>

          <div className="metric-card" style={{ flexDirection: "column", alignItems: "flex-start", padding: "1.5rem" }}>
            <span style={{ fontSize: "0.8rem", fontWeight: "800", color: "var(--primary)", background: "var(--primary-light)", padding: "0.2rem 0.6rem", borderRadius: "var(--radius-full)" }}>Step 04</span>
            <div className="metric-icon" style={{ marginTop: "1rem" }}><TrendingUp size={22} /></div>
            <h3 style={{ fontSize: "1.1rem", margin: "0.75rem 0 0.25rem" }}>4. Analyze Trends</h3>
            <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)" }}>
              Automated charts and reports highlight attendance trends, absence patterns, and department productivity summaries.
            </p>
          </div>
        </div>
      </section>

      {/* ================= CALL TO ACTION ================= */}
      <section style={{ background: "white", padding: "4rem 5%", margin: "4rem 0 0", borderTop: "1px solid var(--border-color)", textAlign: "center" }}>
        <div style={{ maxWidth: "600px", margin: "0 auto" }}>
          <h2 style={{ fontSize: "2rem", fontWeight: "800", marginBottom: "1rem" }}>
            Ready to experience AttendAI?
          </h2>
          <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>
            Sign in to your account or register your workspace to transform your organization's attendance management.
          </p>
          <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
            <button
              className="hero-login-btn"
              onClick={() => navigate("/login")}
            >
              Log In to Platform
              <ArrowRight size={16} />
            </button>
            <button
              className="hero-secondary-btn"
              onClick={() => navigate("/register")}
            >
              Create Account
            </button>
          </div>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer className="landing-footer">
        <div className="brand">
          <div className="brand-logo">A</div>
          <span className="brand-name">
            Attend<span>AI</span>
          </span>
        </div>
        <p style={{ fontSize: "0.875rem" }}>
          © {new Date().getFullYear()} AttendAI. All rights reserved.
        </p>
      </footer>
    </main>
  );
}