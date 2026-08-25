import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  User,
  Mail,
  LockKeyhole,
  Eye,
  EyeOff,
  Sparkles,
  AlertCircle,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Register() {
  const navigate = useNavigate();

  const { registerUser } = useAuth();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    role: "Employee",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  // ============================================
  // HANDLE INPUT CHANGES
  // ============================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));

    setError("");
  };

  // ============================================
  // HANDLE REGISTRATION
  // ============================================

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");

    // Password validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    // Password length validation
    if (formData.password.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    setLoading(true);

    // User data to save
    const userData = {
      name: formData.name.trim(),
      email: formData.email.trim().toLowerCase(),
      role: formData.role,
      password: formData.password,
    };

    // Save user using AuthContext
    registerUser(userData);

    // Redirect to login page
    setTimeout(() => {
      navigate("/login", {
        replace: true,
        state: {
          registrationSuccess: true,
          message: "Account created successfully! Please sign in.",
        },
      });
    }, 500);
  };

  return (
    <main className="auth-page">

      {/* ============================================
          LEFT BRAND PANEL
      ============================================ */}

      <section className="auth-brand-panel">

        <Link to="/" className="auth-back-btn">
          <ArrowLeft size={16} />
          Back to Home
        </Link>

        <div className="auth-logo">
          <Sparkles size={24} />
        </div>

        <h1>
          Join <span>AttendAI</span>
        </h1>

        <p className="auth-tagline">
          Start managing your team's attendance and operations
          with intelligent insights.
        </p>

        <div className="auth-highlight">
          <Sparkles size={20} />

          <div>
            <strong>Quick Setup</strong>

            <p>
              Get your workspace configured in less than 2 minutes.
            </p>
          </div>
        </div>

      </section>


      {/* ============================================
          RIGHT FORM PANEL
      ============================================ */}

      <section className="auth-form-panel">

        <div className="auth-form-container">

          {/* FORM HEADER */}

          <div className="auth-form-header">

            <h2>
              Create an Account
            </h2>

            <p>
              Enter your details to register your workspace.
            </p>

          </div>


          {/* ERROR MESSAGE */}

          {error && (

            <div className="auth-error-message">

              <AlertCircle size={18} />

              <span>
                {error}
              </span>

            </div>

          )}


          {/* REGISTRATION FORM */}

          <form
            className="auth-form"
            onSubmit={handleSubmit}
          >

            {/* FULL NAME */}

            <div className="form-group">

              <label htmlFor="name">
                Full Name
              </label>

              <div className="input-wrapper">

                <User
                  size={18}
                  className="input-icon"
                />

                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>


            {/* EMAIL */}

            <div className="form-group">

              <label htmlFor="email">
                Email Address
              </label>

              <div className="input-wrapper">

                <Mail
                  size={18}
                  className="input-icon"
                />

                <input
                  type="email"
                  id="email"
                  name="email"
                  placeholder="name@company.com"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>


            {/* ROLE */}

            <div className="form-group">

              <label htmlFor="role">
                Role
              </label>

              <div className="input-wrapper role-wrapper">


                <select
                  id="role"
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  required
                >

                  <option value="Employee">
                    Employee
                  </option>

                  <option value="HR">
                    HR / HR Manager
                  </option>

                  <option value="Admin">
                    Admin / System Administrator
                  </option>

                </select>

              </div>

            </div>


            {/* PASSWORD */}

            <div className="form-group">

              <label htmlFor="password">
                Password
              </label>

              <div className="input-wrapper">

                <LockKeyhole
                  size={18}
                  className="input-icon"
                />

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />

                <button
                  type="button"
                  className="toggle-password"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >

                  {showPassword ? (
                    <EyeOff size={17} />
                  ) : (
                    <Eye size={17} />
                  )}

                </button>

              </div>

            </div>


            {/* CONFIRM PASSWORD */}

            <div className="form-group">

              <label htmlFor="confirmPassword">
                Confirm Password
              </label>

              <div className="input-wrapper">

                <LockKeyhole
                  size={18}
                  className="input-icon"
                />

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  id="confirmPassword"
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>


            {/* SUBMIT BUTTON */}

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={loading}
            >

              {loading ? (
                "Creating Account..."
              ) : (
                <>
                  Create Account
                  <ArrowRight size={16} />
                </>
              )}

            </button>

          </form>


          {/* LOGIN LINK */}

          <p className="auth-switch-link">

            Already have an account?{" "}

            <Link to="/login">
              Sign In
            </Link>

          </p>

        </div>

      </section>

    </main>
  );
}