import TodoItem from "./TodoItem";

// Own todos
export default function TodoList({ todos, onToggle, onRemove }) {
  return (
    <ul className="todos">
      {todos.map((t) => (
        <TodoItem key={t.id} todo={t} onToggle={onToggle} onRemove={onRemove} />
      ))}
      {todos.length === 0 && <li className="muted empty">No todos yet.</li>}
    </ul>
  );
}
