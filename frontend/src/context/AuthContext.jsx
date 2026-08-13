import React, {
  createContext,
  useContext,
  useState,
} from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {

  // Load user when app starts
  const [user, setUser] = useState(() => {
    const savedUser =
      localStorage.getItem("attendai_user");

    if (!savedUser) {
      return null;
    }

    try {
      return JSON.parse(savedUser);
    } catch (error) {
      console.error("Error reading saved user:", error);

      localStorage.removeItem("attendai_user");
      localStorage.removeItem("access_token");

      return null;
    }
  });


  // REGISTER USER
  // Keep this for now if your registration page uses it
  const registerUser = (userData) => {
    localStorage.setItem(
      "user_credentials",
      JSON.stringify(userData)
    );
  };


  // LOGIN USER
  const login = (userData, token) => {

    const authData = {
      ...userData,
      access_token: token,
    };

    // Save user
    localStorage.setItem(
      "attendai_user",
      JSON.stringify(authData)
    );

    // Save JWT token
    localStorage.setItem(
      "access_token",
      token
    );

    // Optional: used by your existing dashboard
    localStorage.setItem(
      "active_user",
      JSON.stringify(userData)
    );

    setUser(authData);
  };


  // LOGOUT USER
  const logout = () => {

    localStorage.removeItem("attendai_user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("active_user");

    setUser(null);
  };


  const isAuthenticated = Boolean(user);


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


export function useAuth() {

  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside an AuthProvider"
    );
  }

  return context;
}