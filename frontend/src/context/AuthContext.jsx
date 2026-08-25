import React, {
  createContext,
  useContext,
  useState,
} from "react";


// =====================================================
// CREATE AUTHENTICATION CONTEXT
// =====================================================

const AuthContext = createContext(null);


// =====================================================
// AUTH PROVIDER
// =====================================================

export function AuthProvider({ children }) {

  // ===================================================
  // GET LOGGED-IN USER WHEN APPLICATION STARTS
  // ===================================================

  const [user, setUser] = useState(() => {

    const savedUser =
      localStorage.getItem("attendai_user");

    if (!savedUser) {
      return null;
    }

    try {

      return JSON.parse(savedUser);

    } catch (error) {

      console.error(
        "Error reading saved user:",
        error
      );

      localStorage.removeItem(
        "attendai_user"
      );

      return null;
    }
  });


  // ===================================================
  // REGISTER USER
  // ===================================================

  const registerUser = (userData) => {

    localStorage.setItem(
      "user_credentials",
      JSON.stringify(userData)
    );

  };


  // ===================================================
  // LOGIN USER
  // ===================================================

  const login = (userData) => {

    localStorage.setItem(
      "attendai_user",
      JSON.stringify(userData)
    );

    setUser(userData);

  };


  // ===================================================
  // LOGOUT USER
  // ===================================================

  const logout = () => {

    localStorage.removeItem(
      "attendai_user"
    );

    setUser(null);

  };


  // ===================================================
  // AUTHENTICATION STATUS
  // ===================================================

  const isAuthenticated =
    Boolean(user);


  // ===================================================
  // PROVIDE AUTHENTICATION DATA
  // ===================================================

  return (

    <AuthContext.Provider
      value={{

        user,

        registerUser,

        login,

        logout,

        isAuthenticated,

      }}
    >

      {children}

    </AuthContext.Provider>

  );

}


// =====================================================
// CUSTOM AUTHENTICATION HOOK
// =====================================================

export function useAuth() {

  const context =
    useContext(AuthContext);


  if (!context) {

    throw new Error(
      "useAuth must be used inside an AuthProvider"
    );

  }


  return context;

}