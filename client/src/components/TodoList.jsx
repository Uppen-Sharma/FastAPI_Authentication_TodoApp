import TodoItem from "./TodoItem";

// Own todos
export default function TodoList({ todos, onToggle, onRemove }) {
  return (
    <ul className="todos">
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} onToggle={onToggle} onRemove={onRemove} />
      ))}
      {todos.length === 0 && <li className="muted empty">No todos yet.</li>}
    </ul>
  );
}
