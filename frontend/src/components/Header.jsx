import React, { useState, useRef, useEffect } from "react";
import { 
  FiBell, 
  FiSettings, 
  FiUser, 
  FiLogOut, 
  FiChevronDown,
  FiHelpCircle
} from "react-icons/fi";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    navigate("/login");
  };

  return (
    <header className="top-header">
      <div className="header-right">
        {/* Notifications Icon */}
        <button className="icon-btn" title="Notifications">
          <FiBell size={18} />
          <span className="notification-badge"></span>
        </button>

        {/* Quick Settings Icon */}
        <button className="icon-btn" title="Settings" onClick={() => navigate("/settings")}>
          <FiSettings size={18} />
        </button>

        {/* User Profile Dropdown */}
        <div className="profile-dropdown-wrapper" ref={dropdownRef}>
          <button 
            className="profile-btn" 
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="avatar">A</div>
            <div className="profile-info">
              <span className="profile-name">Admin User</span>
              <span className="profile-role">Administrator</span>
            </div>
            <FiChevronDown className={`chevron-icon ${dropdownOpen ? "open" : ""}`} />
          </button>

          {/* Dropdown Menu */}
          {dropdownOpen && (
            <div className="dropdown-menu">
              <div className="dropdown-header">
                <strong>Admin User</strong>
                <span>admin@attendai.com</span>
              </div>
              <hr className="dropdown-divider" />
              <button className="dropdown-item" onClick={() => { setDropdownOpen(false); navigate("/profile"); }}>
                <FiUser size={16} /> Profile
              </button>
              <button className="dropdown-item" onClick={() => { setDropdownOpen(false); navigate("/settings"); }}>
                <FiSettings size={16} /> Settings
              </button>
              <button className="dropdown-item" onClick={() => { setDropdownOpen(false); }}>
                <FiHelpCircle size={16} /> Help & Support
              </button>
              <hr className="dropdown-divider" />
              <button className="dropdown-item danger" onClick={handleLogout}>
                <FiLogOut size={16} /> Log Out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}