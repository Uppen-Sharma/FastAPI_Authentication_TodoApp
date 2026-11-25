import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { login } from "../api";

// Login page
export default function Login({ onLogin }) {
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Submit login
  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      onLogin(await login(username, password));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="card form" onSubmit={onSubmit}>
      <h1>Login</h1>
      {location.state?.registered && (
        <p className="success">Account created. Please log in.</p>
      )}
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
      {error && <p className="error">{error}</p>}
      <p className="muted">
        No account? <Link to="/register">Sign up</Link>
      </p>
    </form>
  );
}
