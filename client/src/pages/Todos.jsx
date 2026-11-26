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
  const todosPath = isAdmin ? "/admin/todos" : "/client/todos";
  const [allTodos, setAllTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  // Own and other todos
  const todos = allTodos.filter((todo) => todo.user_id === user.id);
  const otherTodos = allTodos.filter((todo) => todo.user_id !== user.id);

  // Load todos
  useEffect(() => {
    api(todosPath)
      .then(setAllTodos)
      .catch((requestError) => setError(requestError.message));
  }, [todosPath]);

  // Run action and reload
  const runAndReload = async (action) => {
    setError("");
    try {
      await action();
      setAllTodos(await api(todosPath));
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  // Add todo
  const addTodo = async (event) => {
    event.preventDefault();
    await runAndReload(() =>
      api(todosPath, { method: "POST", body: JSON.stringify({ title }) }),
    );
    setTitle("");
  };

  // Tick todo
  const toggleTodo = (todo) =>
    runAndReload(() =>
      api(`${todosPath}/${todo.id}`, {
        method: "PUT",
        body: JSON.stringify({ done: !todo.done }),
      }),
    );

  // Delete todo
  const deleteTodo = (todoId) =>
    runAndReload(() => api(`${todosPath}/${todoId}`, { method: "DELETE" }));

  // Logout
  const onLogoutClick = async () => {
    await logout();
    onLogout();
  };

  return (
    <div className="card">
      <TodoHeader user={user} onLogout={onLogoutClick} />
      <TodoForm title={title} onTitleChange={setTitle} onSubmit={addTodo} />

      {error && <p className="error">{error}</p>}

      <TodoList todos={todos} onToggle={toggleTodo} onRemove={deleteTodo} />

      {isAdmin && <OtherTodos todos={otherTodos} onRemove={deleteTodo} />}
    </div>
  );
}
