import { useEffect, useState } from "react";
import { api, logout } from "../api";

// Todo page: a client manages their own todos, an admin also sees every other user's todos
export default function Todos({ user, onLogout }) {
  const isAdmin = user.role === "admin";
  // Clients and admins each have their own routes on the backend
  const base = isAdmin ? "/admin/todos" : "/client/todos";
  const [all, setAll] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  // Split the loaded todos into the user's own and the ones owned by other users
  const todos = all.filter((t) => t.user_id === user.id);
  const others = all.filter((t) => t.user_id !== user.id);

  // Load the todos when the page opens
  useEffect(() => {
    api(base)
      .then(setAll)
      .catch((err) => setError(err.message));
  }, [base]);

  // Run an action, then reload the todos so the page shows the latest data
  const run = async (action) => {
    setError("");
    try {
      await action();
      setAll(await api(base));
    } catch (err) {
      setError(err.message);
    }
  };

  // Add a new todo for the logged in user
  const add = async (e) => {
    e.preventDefault();
    await run(() =>
      api(base, { method: "POST", body: JSON.stringify({ title }) }),
    );
    setTitle("");
  };

  // Tick or untick a todo
  const toggle = (t) =>
    run(() =>
      api(`${base}/${t.id}`, {
        method: "PUT",
        body: JSON.stringify({ done: !t.done }),
      }),
    );

  // Delete a todo, an admin can delete any user's todo
  const remove = (id) => run(() => api(`${base}/${id}`, { method: "DELETE" }));

  // End the session on the server, then clear the user in the app
  const onLogoutClick = async () => {
    await logout();
    onLogout();
  };

  return (
    <div className="card">
      <div className="top">
        <div>
          <h1>My Todos</h1>
          <p className="muted">
            Logged in as <strong>{user.username}</strong> ({user.role})
          </p>
        </div>
        <button className="secondary" onClick={onLogoutClick}>
          Logout
        </button>
      </div>

      <form className="row" onSubmit={add}>
        <input
          placeholder="New todo"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="todos">
        {todos.map((t) => (
          <li key={t.id} className={t.done ? "done" : ""}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={() => toggle(t)}
            />
            <span>{t.title}</span>
            <button className="danger" onClick={() => remove(t.id)}>
              Delete
            </button>
          </li>
        ))}
        {todos.length === 0 && <li className="muted empty">No todos yet.</li>}
      </ul>

      {isAdmin && (
        <>
          <h2 className="section">Other users&apos; todos</h2>
          <ul className="todos">
            {others.map((t) => (
              <li key={t.id} className={t.done ? "done" : ""}>
                <input type="checkbox" checked={t.done} disabled />
                <span>
                  {t.title} <span className="muted">({t.owner})</span>
                </span>
                <button className="danger" onClick={() => remove(t.id)}>
                  Delete
                </button>
              </li>
            ))}
            {others.length === 0 && (
              <li className="muted empty">No todos from other users.</li>
            )}
          </ul>
        </>
      )}
    </div>
  );
}
