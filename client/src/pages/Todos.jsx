import { useEffect, useState } from "react";
import { api, logout } from "../api";
import OtherTodos from "../components/OtherTodos";
import TodoForm from "../components/TodoForm";
import TodoHeader from "../components/TodoHeader";
import TodoList from "../components/TodoList";

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
      <TodoHeader user={user} onLogout={onLogoutClick} />
      <TodoForm title={title} onTitleChange={setTitle} onSubmit={add} />

      {error && <p className="error">{error}</p>}

      <TodoList todos={todos} onToggle={toggle} onRemove={remove} />

      {isAdmin && <OtherTodos todos={others} onRemove={remove} />}
    </div>
  );
}
