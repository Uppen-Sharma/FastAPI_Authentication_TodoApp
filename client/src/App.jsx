import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import { onAuthChange, restoreSession } from "./api";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Restricted from "./pages/Restricted";
import Todos from "./pages/Todos";

// Root component: keeps the logged in user and decides which page to show
function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On page load, the refresh cookie (if there is one) restores the session
  useEffect(() => {
    restoreSession()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  // When another tab logs in or out, reload this tab so it shows the right user
  useEffect(() => onAuthChange(() => window.location.reload()), []);

  // Wait for the session check so a logged in user does not see the login page
  if (loading) return <p>Loading...</p>;

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/todos" replace />} />
      <Route
        path="/login"
        element={
          user ? <Navigate to="/todos" replace /> : <Login onLogin={setUser} />
        }
      />
      <Route
        path="/register"
        element={user ? <Navigate to="/todos" replace /> : <Register />}
      />
      <Route
        path="/todos"
        element={
          user ? (
            <Todos user={user} onLogout={() => setUser(null)} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route path="*" element={<Restricted />} />
    </Routes>
  );
}

export default App;
