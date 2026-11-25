import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../api";

// Sign up page
export default function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");

  // Match passwords, then register
  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (password !== confirm) {
      setError("Passwords do not match");
      return;
    }
    try {
      await register(username, password);
      navigate("/login", { state: { registered: true } });
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="card form" onSubmit={onSubmit}>
      <h1>Sign up</h1>
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
      <input
        type="password"
        placeholder="Retype password"
        value={confirm}
        onChange={(e) => setConfirm(e.target.value)}
        required
      />
      <button type="submit">Create account</button>
      {error && <p className="error">{error}</p>}
      <p className="muted">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </form>
  );
}
