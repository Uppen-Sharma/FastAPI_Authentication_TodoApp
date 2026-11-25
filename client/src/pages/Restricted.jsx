import { Link } from "react-router-dom";

// Blocked page
export default function Restricted() {
  return (
    <div className="card">
      <h1>Restricted route</h1>
      <p className="muted">
        This page does not exist or you are not allowed to view it.
      </p>
      <Link to="/">Go back</Link>
    </div>
  );
}
