import { useState } from "react";

// Checkbox disabled for users without onToggle prop
export default function TodoItem({ todo, onToggle, onRemove }) {
  // Waiting for delete confirmation
  const [confirming, setConfirming] = useState(false);

  // Confirm delete
  const onConfirm = () => {
    setConfirming(false);
    onRemove(todo.id);
  };

  return (
    <li className={todo.done ? "done" : ""}>
      <input
        type="checkbox"
        checked={todo.done}
        onChange={onToggle && (() => onToggle(todo))}
        disabled={!onToggle}
      />
      <span>{todo.title}</span>
      {confirming ? (
        <div className="confirm">
          <button className="danger solid" onClick={onConfirm}>
            Confirm
          </button>
          <button
            className="secondary small"
            onClick={() => setConfirming(false)}
          >
            Cancel
          </button>
        </div>
      ) : (
        <button className="danger" onClick={() => setConfirming(true)}>
          Delete
        </button>
      )}
    </li>
  );
}
