import { useEffect, useState } from "react";
import { api, logout } from "../api";

// Todo page
export default function Todos({ user, onLogout }) {
  const isAdmin = user.role === "admin";
  // Routes by role
  const base = isAdmin ? "/admin/todos" : "/client/todos";
  const [all, setAll] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  // Own and other todos
  const todos = all.filter((t) => t.user_id === user.id);
  const others = all.filter((t) => t.user_id !== user.id);
  const owners = [...new Set(others.map((t) => t.owner))];

  // Load todos
  useEffect(() => {
    api(base)
      .then(setAll)
      .catch((err) => setError(err.message));
  }, [base]);

  // Run action and reload
  const run = async (action) => {
    setError("");
    try {
      await action();
      setAll(await api(base));
    } catch (err) {
      setError(err.message);
    }
  };

  // Add todo
  const add = async (e) => {
    e.preventDefault();
    await run(() =>
      api(base, { method: "POST", body: JSON.stringify({ title }) }),
    );
    setTitle("");
  };

  // Tick todo
  const toggle = (t) =>
    run(() =>
      api(`${base}/${t.id}`, {
        method: "PUT",
        body: JSON.stringify({ done: !t.done }),
      }),
    );

  // Delete todo
  const remove = (id) => run(() => api(`${base}/${id}`, { method: "DELETE" }));

  // Logout
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
          {owners.map((owner) => (
            <div key={owner} className="owner">
              <h3>{owner}</h3>
              <ul className="todos">
                {others
                  .filter((t) => t.owner === owner)
                  .map((t) => (
                    <li key={t.id} className={t.done ? "done" : ""}>
                      <input type="checkbox" checked={t.done} disabled />
                      <span>{t.title}</span>
                      <button className="danger" onClick={() => remove(t.id)}>
                        Delete
                      </button>
                    </li>
                  ))}
              </ul>
            </div>
          ))}
          {owners.length === 0 && (
            <p className="muted">No todos from other users.</p>
          )}
        </>
      )}
    </div>
  );
}
