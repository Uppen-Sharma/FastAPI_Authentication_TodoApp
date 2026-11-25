import TodoItem from "./TodoItem";

// Other users' todos, grouped by owner
export default function OtherTodos({ todos, onRemove }) {
  const owners = [...new Set(todos.map((t) => t.owner))];

  return (
    <>
      <h2 className="section">Other users&apos; todos</h2>
      {owners.map((owner) => (
        <div key={owner} className="owner">
          <h3>{owner}</h3>
          <ul className="todos">
            {todos
              .filter((t) => t.owner === owner)
              .map((t) => (
                <TodoItem key={t.id} todo={t} onRemove={onRemove} />
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
