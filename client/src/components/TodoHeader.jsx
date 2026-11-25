// Title, user and logout
export default function TodoHeader({ user, onLogout }) {
  return (
    <div className="top">
      <div>
        <h1>My Todos</h1>
        <p className="muted">
          Logged in as <strong>{user.username}</strong> ({user.role})
        </p>
      </div>
      <button className="secondary" onClick={onLogout}>
        Logout
      </button>
    </div>
  );
}
