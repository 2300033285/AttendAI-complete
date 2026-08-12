import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Mail,
  X,
  ArrowRight,
  CheckCircle2,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
} from "lucide-react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // =====================================================
  // HANDLE PASSWORD RESET
  // =====================================================

  const handleSubmit = (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    // -----------------------------------------------
    // PASSWORD LENGTH
    // -----------------------------------------------

    if (newPassword.length < 6) {
      setError("Password must contain at least 6 characters.");
      return;
    }

    // -----------------------------------------------
    // PASSWORD MATCH
    // -----------------------------------------------

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    // -----------------------------------------------
    // FRONTEND TESTING
    // -----------------------------------------------

    setTimeout(() => {
      setLoading(false);

      // Get existing registered user
      const savedUserData =
        localStorage.getItem("user_credentials");

      if (savedUserData) {
        try {
          const savedUser = JSON.parse(savedUserData);

          // Check email
          if (
            savedUser.email?.toLowerCase() ===
            email.trim().toLowerCase()
          ) {
            // Update password
            const updatedUser = {
              ...savedUser,
              password: newPassword,
            };

            localStorage.setItem(
              "user_credentials",
              JSON.stringify(updatedUser)
            );
          }
        } catch (error) {
          console.error(
            "Error updating password:",
            error
          );
        }
      }

      setMessage(
        "Your password has been reset successfully. You can now sign in with your new password."
      );

      // Clear password fields
      setNewPassword("");
      setConfirmPassword("");
    }, 1000);
  };

  return (
    <div className="forgot-password-overlay">

      {/* =================================================
          MODAL
      ================================================= */}

      <div className="forgot-password-modal">

        {/* CLOSE BUTTON */}

        <Link
          to="/login"
          className="forgot-close-btn"
          aria-label="Close forgot password"
        >
          <X size={20} />
        </Link>


        {/* =================================================
            ICON
        ================================================= */}

        <div className="forgot-password-icon">
          <Mail size={25} />
        </div>


        {/* =================================================
            HEADER
        ================================================= */}

        <div className="forgot-header">

          <h2>
            Reset your password
          </h2>

          <p>
            Enter your registered Gmail address and
            create a new password for your AttendAI account.
          </p>

        </div>


        {/* =================================================
            SUCCESS MESSAGE
        ================================================= */}

        {message && (

          <div className="forgot-success">

            <CheckCircle2 size={19} />

            <span>
              {message}
            </span>

          </div>

        )}


        {/* =================================================
            ERROR MESSAGE
        ================================================= */}

        {error && (

          <div className="forgot-error">

            <AlertCircle size={19} />

            <span>
              {error}
            </span>

          </div>

        )}


        {/* =================================================
            FORM
        ================================================= */}

        {!message && (

          <form
            onSubmit={handleSubmit}
            className="forgot-password-form"
          >

            {/* =================================================
                EMAIL
            ================================================= */}

            <div className="form-group">

              <label htmlFor="forgot-email">
                Gmail address
              </label>

              <div className="input-wrapper">

                <Mail
                  size={18}
                  className="input-icon"
                />

                <input
                  id="forgot-email"
                  type="email"
                  placeholder="name@gmail.com"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    setError("");
                  }}
                  autoComplete="email"
                  required
                />

              </div>

            </div>


            {/* =================================================
                NEW PASSWORD
            ================================================= */}

            <div className="form-group">

              <label htmlFor="new-password">
                New password
              </label>

              <div className="input-wrapper">

                <Lock
                  size={18}
                  className="input-icon"
                />

                <input
                  id="new-password"
                  type={
                    showNewPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => {
                    setNewPassword(e.target.value);
                    setError("");
                  }}
                  autoComplete="new-password"
                  required
                />

                <button
                  type="button"
                  className="toggle-password"
                  onClick={() =>
                    setShowNewPassword(
                      !showNewPassword
                    )
                  }
                  aria-label={
                    showNewPassword
                      ? "Hide new password"
                      : "Show new password"
                  }
                >
                  {showNewPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>

              </div>

            </div>


            {/* =================================================
                CONFIRM PASSWORD
            ================================================= */}

            <div className="form-group">

              <label htmlFor="confirm-password">
                Confirm password
              </label>

              <div className="input-wrapper">

                <Lock
                  size={18}
                  className="input-icon"
                />

                <input
                  id="confirm-password"
                  type={
                    showConfirmPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(
                      e.target.value
                    );
                    setError("");
                  }}
                  autoComplete="new-password"
                  required
                />

                <button
                  type="button"
                  className="toggle-password"
                  onClick={() =>
                    setShowConfirmPassword(
                      !showConfirmPassword
                    )
                  }
                  aria-label={
                    showConfirmPassword
                      ? "Hide confirm password"
                      : "Show confirm password"
                  }
                >
                  {showConfirmPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>

              </div>

            </div>


            {/* =================================================
                SUBMIT BUTTON
            ================================================= */}

            <button
              type="submit"
              className="auth-submit-btn forgot-submit-btn"
              disabled={loading}
            >

              {loading ? (
                "Resetting Password..."
              ) : (
                <>
                  Reset Password
                  <ArrowRight size={17} />
                </>
              )}

            </button>

          </form>

        )}


        {/* =================================================
            BACK TO LOGIN
        ================================================= */}

        <div className="forgot-back">

          <Link to="/login">
            Back to Sign In
          </Link>

        </div>

      </div>

    </div>
  );
}