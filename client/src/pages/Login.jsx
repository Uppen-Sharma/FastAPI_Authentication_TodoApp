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
  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      onLogin(await login(username, password));
    } catch (requestError) {
      setError(requestError.message);
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
        onChange={(event) => setUsername(event.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
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
