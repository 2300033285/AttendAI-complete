import React, { useRef, useState } from "react";
import {
  Bell,
  Search,
  ChevronDown,
  User,
  Phone,
  Mail,
  Settings,
  Edit3,
  Camera,
  X,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";

export default function Navbar({
  title = "AttendAI Workspace",
}) {
  // =====================================================
  // AUTHENTICATED USER
  // =====================================================

  const { user } = useAuth();

  // =====================================================
  // PROFILE MENU STATE
  // =====================================================

  const [isProfileOpen, setIsProfileOpen] =
    useState(false);

  // =====================================================
  // EDIT PROFILE MODAL STATE
  // =====================================================

  const [isEditProfileOpen, setIsEditProfileOpen] =
    useState(false);

  // =====================================================
  // FILE INPUT REFERENCE
  // =====================================================

  const fileInputRef = useRef(null);

  // =====================================================
  // LOAD SAVED PROFILE
  // =====================================================

  const getSavedProfile = () => {
    const savedProfile =
      localStorage.getItem("attendai_profile");

    if (savedProfile) {
      try {
        return JSON.parse(savedProfile);
      } catch (error) {
        console.error(
          "Error loading profile:",
          error
        );
      }
    }

    return {
      name: user?.name || "User",
      email:
        user?.email || "user@attendai.com",
      phone: "",
      picture: "",
    };
  };

  const [profile, setProfile] =
    useState(getSavedProfile);

  // =====================================================
  // EDIT PROFILE DATA
  // =====================================================

  const [editProfile, setEditProfile] =
    useState(profile);

  // =====================================================
  // PROFILE INITIAL
  // =====================================================

  const profileInitial =
    profile.name
      ?.charAt(0)
      ?.toUpperCase() || "A";

  // =====================================================
  // OPEN EDIT PROFILE
  // =====================================================

  const openEditProfile = () => {
    setEditProfile(profile);
    setIsProfileOpen(false);
    setIsEditProfileOpen(true);
  };

  // =====================================================
  // CLOSE EDIT PROFILE
  // =====================================================

  const closeEditProfile = () => {
    setIsEditProfileOpen(false);
  };

  // =====================================================
  // HANDLE PROFILE INPUT
  // =====================================================

  const handleProfileChange = (e) => {
    const { name, value } = e.target;

    setEditProfile((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // =====================================================
  // HANDLE PROFILE IMAGE
  // =====================================================

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];

    if (!file) {
      return;
    }

    // Only allow image files
    if (!file.type.startsWith("image/")) {
      alert("Please select a valid image.");
      return;
    }

    // Limit image size to 5MB
    if (file.size > 5 * 1024 * 1024) {
      alert(
        "Please select an image smaller than 5MB."
      );
      return;
    }

    const reader = new FileReader();

    reader.onload = () => {
      setEditProfile((previous) => ({
        ...previous,
        picture: reader.result,
      }));
    };

    reader.readAsDataURL(file);
  };

  // =====================================================
  // SAVE PROFILE
  // =====================================================

  const handleSaveProfile = (e) => {
    e.preventDefault();

    const updatedProfile = {
      ...editProfile,
      name: editProfile.name.trim(),
      email: editProfile.email.trim(),
      phone: editProfile.phone.trim(),
    };

    setProfile(updatedProfile);

    localStorage.setItem(
      "attendai_profile",
      JSON.stringify(updatedProfile)
    );

    setIsEditProfileOpen(false);
  };

  // =====================================================
  // REMOVE PROFILE PICTURE
  // =====================================================

  const removeProfilePicture = () => {
    setEditProfile((previous) => ({
      ...previous,
      picture: "",
    }));
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <>
      {/* =================================================
          NAVBAR
      ================================================= */}

      <header
        className="app-navbar"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "1rem 2.5rem",
          backgroundColor: "white",
          borderBottom:
            "1px solid var(--border-color)",
          position: "relative",
          zIndex: 1000,
        }}
      >

        {/* =================================================
            PAGE TITLE
        ================================================= */}

        <h2
          style={{
            fontSize: "1.25rem",
            fontWeight: "700",
            margin: 0,
          }}
        >
          {title}
        </h2>


        {/* =================================================
            RIGHT SIDE
        ================================================= */}

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "1.5rem",
          }}
        >

          {/* =================================================
              SEARCH
          ================================================= */}

          <div
            className="navbar-search"
            style={{
              position: "relative",
            }}
          >

            <Search
              size={17}
              style={{
                position: "absolute",
                left: "0.75rem",
                top: "50%",
                transform:
                  "translateY(-50%)",
                color: "#94a3b8",
              }}
            />

            <input
              type="text"
              placeholder="Search anything..."
              style={{
                padding:
                  "0.5rem 0.75rem 0.5rem 2.25rem",
                borderRadius: "8px",
                border:
                  "1px solid #e2e8f0",
                outline: "none",
                fontSize: "0.875rem",
              }}
            />

          </div>


          {/* =================================================
              NOTIFICATION
          ================================================= */}

          <button
            className="navbar-icon-btn"
            type="button"
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              position: "relative",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >

            <Bell size={18} />

          </button>


          {/* =================================================
              PROFILE BUTTON
          ================================================= */}

          <div
            className="navbar-profile"
            style={{
              position: "relative",
            }}
          >

            <button
              type="button"
              onClick={() =>
                setIsProfileOpen(
                  (previous) => !previous
                )
              }
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                cursor: "pointer",
                background: "transparent",
                border: "none",
                padding: "2px",
              }}
              aria-label="Open profile"
            >

              {/* =================================================
                  SMALL PROFILE AVATAR
              ================================================= */}

              {profile.picture ? (

                <img
                  src={profile.picture}
                  alt="Profile"
                  style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "50%",
                    objectFit: "cover",
                    objectPosition:
                      "center top",
                    border:
                      "2px solid #e2e8f0",
                  }}
                />

              ) : (

                <div
                  className="navbar-avatar"
                  style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "50%",
                    backgroundColor:
                      "var(--primary)",
                    color: "white",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: "700",
                    fontSize: "15px",
                  }}
                >
                  {profileInitial}
                </div>

              )}

              <ChevronDown
                size={15}
                style={{
                  transition:
                    "transform 0.2s ease",
                  transform:
                    isProfileOpen
                      ? "rotate(180deg)"
                      : "rotate(0deg)",
                }}
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
                  width: "360px",
                  background: "#ffffff",
                  border:
                    "1px solid #e2e8f0",
                  borderRadius: "16px",
                  boxShadow:
                    "0 20px 45px rgba(15, 23, 42, 0.16)",
                  overflow: "hidden",
                  zIndex: 2000,
                }}
              >

                {/* =================================================
                    LARGE PROFILE PHOTO AREA
                ================================================= */}

                <div
                  style={{
                    padding:
                      "28px 24px 24px",
                    background:
                      "linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)",
                    textAlign: "center",
                    borderBottom:
                      "1px solid #e5e7eb",
                  }}
                >

                  {/* LARGE PHOTO */}

                  <div
                    style={{
                      width: "150px",
                      height: "150px",
                      margin: "0 auto 14px",
                      borderRadius: "50%",
                      overflow: "hidden",
                      background:
                        "#eef2ff",
                      border:
                        "5px solid #ffffff",
                      boxShadow:
                        "0 4px 18px rgba(0,0,0,0.12)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >

                    {profile.picture ? (

                      <img
                        src={profile.picture}
                        alt="User profile"
                        style={{
                          width: "100%",
                          height: "100%",
                          objectFit: "cover",
                          objectPosition:
                            "center top",
                        }}
                      />

                    ) : (

                      <span
                        style={{
                          fontSize: "52px",
                          fontWeight: "700",
                          color:
                            "var(--primary)",
                        }}
                      >
                        {profileInitial}
                      </span>

                    )}

                  </div>


                  {/* NAME */}

                  <h3
                    style={{
                      margin: "0 0 4px",
                      fontSize: "19px",
                      fontWeight: "700",
                      color: "#0f172a",
                    }}
                  >
                    {profile.name}
                  </h3>


                  {/* ROLE */}

                  <p
                    style={{
                      margin: 0,
                      fontSize: "13px",
                      color: "#64748b",
                    }}
                  >
                    {user?.role ||
                      "Employee"}
                  </p>

                </div>


                {/* =================================================
                    PROFILE INFORMATION
                ================================================= */}

                <div
                  style={{
                    padding: "20px 24px",
                  }}
                >

                  {/* FULL NAME */}

                  <div
                    style={{
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "13px",
                      marginBottom:
                        "18px",
                    }}
                  >

                    <div
                      style={{
                        width: "36px",
                        height: "36px",
                        borderRadius:
                          "9px",
                        background:
                          "#f1f5f9",
                        display: "flex",
                        alignItems:
                          "center",
                        justifyContent:
                          "center",
                        color: "#475569",
                      }}
                    >
                      <User size={17} />
                    </div>

                    <div>

                      <p
                        style={{
                          margin: 0,
                          fontSize: "11px",
                          color:
                            "#94a3b8",
                          marginBottom:
                            "3px",
                        }}
                      >
                        Full Name
                      </p>

                      <p
                        style={{
                          margin: 0,
                          fontSize: "14px",
                          fontWeight: "600",
                          color:
                            "#1e293b",
                        }}
                      >
                        {profile.name}
                      </p>

                    </div>

                  </div>


                  {/* PHONE */}

                  <div
                    style={{
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "13px",
                      marginBottom:
                        "18px",
                    }}
                  >

                    <div
                      style={{
                        width: "36px",
                        height: "36px",
                        borderRadius:
                          "9px",
                        background:
                          "#f1f5f9",
                        display: "flex",
                        alignItems:
                          "center",
                        justifyContent:
                          "center",
                        color: "#475569",
                      }}
                    >
                      <Phone size={17} />
                    </div>

                    <div>

                      <p
                        style={{
                          margin: 0,
                          fontSize: "11px",
                          color:
                            "#94a3b8",
                          marginBottom:
                            "3px",
                        }}
                      >
                        Phone Number
                      </p>

                      <p
                        style={{
                          margin: 0,
                          fontSize: "14px",
                          fontWeight: "600",
                          color:
                            "#1e293b",
                        }}
                      >
                        {profile.phone ||
                          "Not provided"}
                      </p>

                    </div>

                  </div>


                  {/* EMAIL */}

                  <div
                    style={{
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "13px",
                      marginBottom:
                        "22px",
                    }}
                  >

                    <div
                      style={{
                        width: "36px",
                        height: "36px",
                        borderRadius:
                          "9px",
                        background:
                          "#f1f5f9",
                        display: "flex",
                        alignItems:
                          "center",
                        justifyContent:
                          "center",
                        color: "#475569",
                      }}
                    >
                      <Mail size={17} />
                    </div>

                    <div
                      style={{
                        minWidth: 0,
                      }}
                    >

                      <p
                        style={{
                          margin: 0,
                          fontSize: "11px",
                          color:
                            "#94a3b8",
                          marginBottom:
                            "3px",
                        }}
                      >
                        Email Address
                      </p>

                      <p
                        style={{
                          margin: 0,
                          fontSize: "14px",
                          fontWeight: "600",
                          color:
                            "#1e293b",
                          overflowWrap:
                            "anywhere",
                        }}
                      >
                        {profile.email}
                      </p>

                    </div>

                  </div>


                  {/* =================================================
                      EDIT PROFILE
                  ================================================= */}

                  <button
                    type="button"
                    onClick={
                      openEditProfile
                    }
                    style={{
                      width: "100%",
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "10px",
                      padding:
                        "11px 13px",
                      marginBottom:
                        "8px",
                      background:
                        "#f8fafc",
                      border:
                        "1px solid #e2e8f0",
                      borderRadius:
                        "9px",
                      cursor: "pointer",
                      color: "#334155",
                      fontSize: "13px",
                      fontWeight: "600",
                    }}
                  >

                    <Edit3 size={16} />

                    Edit Profile

                  </button>


                  {/* =================================================
                      SETTINGS
                  ================================================= */}

                  <button
                    type="button"
                    onClick={() =>
                      alert(
                        "Settings page will be added here."
                      )
                    }
                    style={{
                      width: "100%",
                      display: "flex",
                      alignItems:
                        "center",
                      gap: "10px",
                      padding:
                        "11px 13px",
                      background:
                        "transparent",
                      border: "none",
                      borderRadius:
                        "9px",
                      cursor: "pointer",
                      color: "#334155",
                      fontSize: "13px",
                      fontWeight: "600",
                      textAlign: "left",
                    }}
                  >

                    <Settings size={16} />

                    Settings

                  </button>

                </div>

              </div>

            )}

          </div>

        </div>

      </header>


      {/* =====================================================
          EDIT PROFILE MODAL
      ===================================================== */}

      {isEditProfileOpen && (

        <div
          style={{
            position: "fixed",
            inset: 0,
            background:
              "rgba(15, 23, 42, 0.55)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 5000,
            padding: "20px",
          }}
          onClick={
            closeEditProfile
          }
        >

          <div
            style={{
              width: "100%",
              maxWidth: "500px",
              maxHeight: "90vh",
              overflowY: "auto",
              background: "#ffffff",
              borderRadius: "16px",
              boxShadow:
                "0 25px 60px rgba(0,0,0,0.2)",
            }}
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            {/* =================================================
                MODAL HEADER
            ================================================= */}

            <div
              style={{
                display: "flex",
                alignItems:
                  "center",
                justifyContent:
                  "space-between",
                padding:
                  "20px 24px",
                borderBottom:
                  "1px solid #e5e7eb",
              }}
            >

              <div>

                <h2
                  style={{
                    margin: 0,
                    fontSize: "20px",
                    color:
                      "#0f172a",
                  }}
                >
                  Edit Profile
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
                  Update your personal
                  information.
                </p>

              </div>


              <button
                type="button"
                onClick={
                  closeEditProfile
                }
                style={{
                  width: "34px",
                  height: "34px",
                  border: "none",
                  background:
                    "#f1f5f9",
                  borderRadius:
                    "8px",
                  cursor: "pointer",
                  display: "flex",
                  alignItems:
                    "center",
                  justifyContent:
                    "center",
                  color: "#475569",
                }}
              >

                <X size={18} />

              </button>

            </div>


            {/* =================================================
                EDIT FORM
            ================================================= */}

            <form
              onSubmit={
                handleSaveProfile
              }
              style={{
                padding: "24px",
              }}
            >

              {/* =================================================
                  LARGE PHOTO UPLOAD
              ================================================= */}

              <div
                style={{
                  textAlign:
                    "center",
                  marginBottom:
                    "25px",
                }}
              >

                <div
                  style={{
                    position:
                      "relative",
                    width: "170px",
                    height: "170px",
                    margin:
                      "0 auto 14px",
                  }}
                >

                  {/* PHOTO */}

                  <div
                    style={{
                      width: "170px",
                      height: "170px",
                      borderRadius:
                        "50%",
                      overflow: "hidden",
                      background:
                        "#eef2ff",
                      border:
                        "5px solid #ffffff",
                      boxShadow:
                        "0 4px 18px rgba(0,0,0,0.15)",
                      display: "flex",
                      alignItems:
                        "center",
                      justifyContent:
                        "center",
                    }}
                  >

                    {editProfile.picture ? (

                      <img
                        src={
                          editProfile.picture
                        }
                        alt="Profile preview"
                        style={{
                          width: "100%",
                          height: "100%",
                          objectFit:
                            "cover",
                          objectPosition:
                            "center top",
                        }}
                      />

                    ) : (

                      <span
                        style={{
                          fontSize:
                            "60px",
                          fontWeight:
                            "700",
                          color:
                            "var(--primary)",
                        }}
                      >
                        {editProfile.name
                          ?.charAt(0)
                          ?.toUpperCase() ||
                          "A"}
                      </span>

                    )}

                  </div>


                  {/* CAMERA BUTTON */}

                  <button
                    type="button"
                    onClick={() =>
                      fileInputRef.current?.click()
                    }
                    style={{
                      position:
                        "absolute",
                      right: "5px",
                      bottom: "8px",
                      width: "42px",
                      height: "42px",
                      borderRadius:
                        "50%",
                      border:
                        "3px solid white",
                      background:
                        "var(--primary)",
                      color: "white",
                      display: "flex",
                      alignItems:
                        "center",
                      justifyContent:
                        "center",
                      cursor:
                        "pointer",
                    }}
                    title="Upload profile picture"
                  >

                    <Camera size={18} />

                  </button>


                  <input
                    ref={
                      fileInputRef
                    }
                    type="file"
                    accept="image/*"
                    onChange={
                      handleImageUpload
                    }
                    style={{
                      display: "none",
                    }}
                  />

                </div>


                <p
                  style={{
                    margin:
                      "0 0 5px",
                    fontSize:
                      "13px",
                    fontWeight:
                      "600",
                    color:
                      "#334155",
                  }}
                >
                  Profile Picture
                </p>

                <p
                  style={{
                    margin: 0,
                    fontSize:
                      "11px",
                    color:
                      "#94a3b8",
                  }}
                >
                  Upload a clear chest-up
                  profile photo.
                </p>


                {/* REMOVE PHOTO */}

                {editProfile.picture && (

                  <button
                    type="button"
                    onClick={
                      removeProfilePicture
                    }
                    style={{
                      marginTop:
                        "8px",
                      border: "none",
                      background:
                        "transparent",
                      color:
                        "#dc2626",
                      fontSize:
                        "12px",
                      cursor:
                        "pointer",
                    }}
                  >
                    Remove photo
                  </button>

                )}

              </div>


              {/* =================================================
                  FULL NAME
              ================================================= */}

              <div
                style={{
                  marginBottom:
                    "18px",
                }}
              >

                <label
                  style={{
                    display:
                      "block",
                    marginBottom:
                      "7px",
                    fontSize:
                      "13px",
                    fontWeight:
                      "600",
                    color:
                      "#334155",
                  }}
                >
                  Full Name
                </label>

                <div
                  style={{
                    position:
                      "relative",
                  }}
                >

                  <User
                    size={17}
                    style={{
                      position:
                        "absolute",
                      left:
                        "12px",
                      top:
                        "50%",
                      transform:
                        "translateY(-50%)",
                      color:
                        "#94a3b8",
                    }}
                  />

                  <input
                    type="text"
                    name="name"
                    value={
                      editProfile.name
                    }
                    onChange={
                      handleProfileChange
                    }
                    required
                    style={{
                      width:
                        "100%",
                      boxSizing:
                        "border-box",
                      padding:
                        "11px 12px 11px 40px",
                      border:
                        "1px solid #dbe2ea",
                      borderRadius:
                        "8px",
                      outline:
                        "none",
                      fontSize:
                        "14px",
                    }}
                  />

                </div>

              </div>


              {/* =================================================
                  PHONE
              ================================================= */}

              <div
                style={{
                  marginBottom:
                    "18px",
                }}
              >

                <label
                  style={{
                    display:
                      "block",
                    marginBottom:
                      "7px",
                    fontSize:
                      "13px",
                    fontWeight:
                      "600",
                    color:
                      "#334155",
                  }}
                >
                  Phone Number
                </label>

                <div
                  style={{
                    position:
                      "relative",
                  }}
                >

                  <Phone
                    size={17}
                    style={{
                      position:
                        "absolute",
                      left:
                        "12px",
                      top:
                        "50%",
                      transform:
                        "translateY(-50%)",
                      color:
                        "#94a3b8",
                    }}
                  />

                  <input
                    type="tel"
                    name="phone"
                    placeholder="+91 98765 43210"
                    value={
                      editProfile.phone
                    }
                    onChange={
                      handleProfileChange
                    }
                    style={{
                      width:
                        "100%",
                      boxSizing:
                        "border-box",
                      padding:
                        "11px 12px 11px 40px",
                      border:
                        "1px solid #dbe2ea",
                      borderRadius:
                        "8px",
                      outline:
                        "none",
                      fontSize:
                        "14px",
                    }}
                  />

                </div>

              </div>


              {/* =================================================
                  EMAIL
              ================================================= */}

              <div
                style={{
                  marginBottom:
                    "25px",
                }}
              >

                <label
                  style={{
                    display:
                      "block",
                    marginBottom:
                      "7px",
                    fontSize:
                      "13px",
                    fontWeight:
                      "600",
                    color:
                      "#334155",
                  }}
                >
                  Email Address
                </label>

                <div
                  style={{
                    position:
                      "relative",
                  }}
                >

                  <Mail
                    size={17}
                    style={{
                      position:
                        "absolute",
                      left:
                        "12px",
                      top:
                        "50%",
                      transform:
                        "translateY(-50%)",
                      color:
                        "#94a3b8",
                    }}
                  />

                  <input
                    type="email"
                    name="email"
                    value={
                      editProfile.email
                    }
                    onChange={
                      handleProfileChange
                    }
                    required
                    style={{
                      width:
                        "100%",
                      boxSizing:
                        "border-box",
                      padding:
                        "11px 12px 11px 40px",
                      border:
                        "1px solid #dbe2ea",
                      borderRadius:
                        "8px",
                      outline:
                        "none",
                      fontSize:
                        "14px",
                    }}
                  />

                </div>

              </div>


              {/* =================================================
                  FORM BUTTONS
              ================================================= */}

              <div
                style={{
                  display: "flex",
                  justifyContent:
                    "flex-end",
                  gap: "10px",
                }}
              >

                <button
                  type="button"
                  onClick={
                    closeEditProfile
                  }
                  style={{
                    padding:
                      "10px 18px",
                    border:
                      "1px solid #dbe2ea",
                    background:
                      "#ffffff",
                    borderRadius:
                      "8px",
                    cursor:
                      "pointer",
                    fontSize:
                      "13px",
                    fontWeight:
                      "600",
                    color:
                      "#475569",
                  }}
                >
                  Cancel
                </button>


                <button
                  type="submit"
                  className="btn-primary"
                  style={{
                    padding:
                      "10px 18px",
                  }}
                >
                  Save Changes
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </>
  );
}