import React, { useEffect, useState } from "react";
import {
  Link,
  useNavigate,
  useLocation,
} from "react-router-dom";

import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  ArrowLeft,
  AlertCircle,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Login() {
  // =====================================================
  // STATE
  // =====================================================

  const [showPassword, setShowPassword] =
    useState(false);

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [successMessage, setSuccessMessage] =
    useState("");


  // =====================================================
  // ROUTER HOOKS
  // =====================================================

  const navigate =
    useNavigate();

  const location =
    useLocation();


  // =====================================================
  // AUTH CONTEXT
  // =====================================================

  const { login } =
    useAuth();


  // =====================================================
  // READ REGISTRATION SUCCESS MESSAGE
  // =====================================================

  useEffect(() => {
    const message =
      location.state?.message;

    if (message) {
      setSuccessMessage(message);

      // Clear the message from browser history
      // while keeping the current page
      window.history.replaceState(
        {},
        document.title,
        window.location.pathname
      );
    }
  }, [location]);


  // =====================================================
  // HANDLE LOGIN
  // =====================================================

  const handleSubmit = (e) => {
    e.preventDefault();

    setError("");
    setLoading(false);


    // -----------------------------------------------
    // GET REGISTERED USER
    // -----------------------------------------------

    const savedUserData =
      localStorage.getItem(
        "user_credentials"
      );


    // -----------------------------------------------
    // CHECK WHETHER USER EXISTS
    // -----------------------------------------------

    if (!savedUserData) {
      setError(
        "No account found. Please create an account first."
      );

      return;
    }


    // -----------------------------------------------
    // SAFELY READ USER DATA
    // -----------------------------------------------

    let savedUser;

    try {
      savedUser =
        JSON.parse(savedUserData);
    } catch (error) {
      setError(
        "Something went wrong. Please register again."
      );

      localStorage.removeItem(
        "user_credentials"
      );

      return;
    }


    // -----------------------------------------------
    // VALIDATE LOGIN CREDENTIALS
    // -----------------------------------------------

    const isEmailValid =
      savedUser.email?.toLowerCase() ===
      email.trim().toLowerCase();

    const isPasswordValid =
      savedUser.password === password;


    if (
      isEmailValid &&
      isPasswordValid
    ) {

      setLoading(true);


      // ---------------------------------------------
      // USER DATA FOR AUTHENTICATION CONTEXT
      // ---------------------------------------------

      const userData = {
        name: savedUser.name,
        email: savedUser.email,
        role: savedUser.role || "Employee",
      };


      // ---------------------------------------------
      // SAVE USER IN AUTH CONTEXT
      // ---------------------------------------------

      login(userData);


      // ---------------------------------------------
      // SAVE ACTIVE USER
      // ---------------------------------------------

      localStorage.setItem(
        "active_user",
        JSON.stringify(userData)
      );


      // ---------------------------------------------
      // REDIRECT TO DASHBOARD
      // ---------------------------------------------

      navigate(
        "/dashboard",
        {
          replace: true,
        }
      );

    } else {

      setError(
        "Invalid email or password. Please try again."
      );

    }
  };


  // =====================================================
  // COMPONENT UI
  // =====================================================

  return (
    <div className="auth-page">

      {/* =================================================
          LEFT BRANDING PANEL
      ================================================= */}

      <div className="auth-brand-panel">

        {/* BACK TO HOME */}

        <Link
          to="/"
          className="auth-back-btn"
        >
          <ArrowLeft size={16} />
          Back to home
        </Link>


        {/* LOGO */}

        <div className="auth-logo">
          <Sparkles size={24} />
        </div>


        {/* HEADING */}

        <h1>
          Your workforce.
          <br />

          <span>
            Smarter than ever.
          </span>
        </h1>


        {/* DESCRIPTION */}

        <p className="auth-tagline">
          Track attendance, manage employees,
          and analyze performance with
          AI-powered insights.
        </p>


        {/* FEATURES */}

        <div className="auth-feature-list">

          <div className="auth-feature-item">

            <div className="auth-feature-icon">
              <CheckCircle2 size={18} />
            </div>

            <span>
              98% automated attendance accuracy
            </span>

          </div>


          <div className="auth-feature-item">

            <div className="auth-feature-icon">
              <CheckCircle2 size={18} />
            </div>

            <span>
              Real-time shift & leave tracking
            </span>

          </div>


          <div className="auth-feature-item">

            <div className="auth-feature-icon">
              <CheckCircle2 size={18} />
            </div>

            <span>
              Instant workforce analytics reports
            </span>

          </div>

        </div>

      </div>


      {/* =================================================
          RIGHT FORM PANEL
      ================================================= */}

      <div className="auth-form-panel">

        <div className="auth-form-container">


          {/* SUCCESS MESSAGE */}

          {successMessage && (

            <div className="auth-success-message">

              <CheckCircle2 size={18} />

              <span>
                {successMessage}
              </span>

            </div>

          )}


          {/* ERROR MESSAGE */}

          {error && (

            <div className="auth-error-message">

              <AlertCircle size={18} />

              <span>
                {error}
              </span>

            </div>

          )}


          {/* FORM HEADER */}

          <div className="auth-form-header">

            <h2>
              Welcome back
            </h2>

            <p>
              Sign in to your account to continue
            </p>

          </div>


          {/* LOGIN FORM */}

          <form
            onSubmit={handleSubmit}
            className="auth-form"
          >


            {/* EMAIL */}

            <div className="form-group">

              <label htmlFor="email">
                Email address
              </label>

              <div className="input-wrapper">

                <Mail
                  size={18}
                  className="input-icon"
                />

                <input
                  type="email"
                  id="email"
                  placeholder="name@company.com"
                  value={email}
                  autoComplete="email"
                  onChange={(e) => {

                    setEmail(
                      e.target.value
                    );

                    setError("");

                  }}
                  required
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="form-group">

              <div className="password-label-row">

                <label htmlFor="password">
                  Password
                </label>

                <Link
                  to="/forgot-password"
                  className="forgot-password-link"
                >
                  Forgot password?
                </Link>

              </div>


              <div className="input-wrapper">

                <Lock
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
                  placeholder="Enter your password"
                  value={password}
                  autoComplete="current-password"
                  onChange={(e) => {

                    setPassword(
                      e.target.value
                    );

                    setError("");

                  }}
                  required
                />


                <button
                  type="button"
                  className="toggle-password"
                  onClick={() =>
                    setShowPassword(
                      !showPassword
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >

                  {showPassword ? (

                    <EyeOff size={18} />

                  ) : (

                    <Eye size={18} />

                  )}

                </button>

              </div>

            </div>


            {/* REMEMBER ME */}

            <div className="remember-me-container">

              <input
                type="checkbox"
                id="remember"
              />

              <label htmlFor="remember">
                Remember me on this device
              </label>

            </div>


            {/* SUBMIT BUTTON */}

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={loading}
            >

              {loading ? (

                "Signing in..."

              ) : (

                <>
                  Sign in
                  <ArrowRight size={18} />
                </>

              )}

            </button>

          </form>


          {/* REGISTER LINK */}

          <div className="auth-switch-link">

            Don't have an account?{" "}

            <Link to="/register">
              Create an account
            </Link>

          </div>

        </div>

      </div>

    </div>
  );
}