import TodoItem from "./TodoItem";

// Other users' todos, grouped by owner
export default function OtherTodos({ todos, onRemove }) {
  const owners = [...new Set(todos.map((todo) => todo.owner))];

  return (
    <>
      <h2 className="section">Other users&apos; todos</h2>
      {owners.map((owner) => (
        <div key={owner} className="owner">
          <h3>{owner}</h3>
          <ul className="todos">
            {todos
              .filter((todo) => todo.owner === owner)
              .map((todo) => (
                <TodoItem key={todo.id} todo={todo} onRemove={onRemove} />
              ))}
          </ul>
        </div>
      ))}
      {owners.length === 0 && (
        <p className="muted">No todos from other users.</p>
      )}
    </>
  );
}
