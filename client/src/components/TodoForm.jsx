// New todo form
export default function TodoForm({ title, onTitleChange, onSubmit }) {
  return (
    <form className="row" onSubmit={onSubmit}>
      <input
        placeholder="New todo"
        value={title}
        onChange={(event) => onTitleChange(event.target.value)}
        maxLength={100}
        pattern=".*\S.*"
        title="Todo cannot be blank"
        required
      />
      <button type="submit">Add</button>
    </form>
  );
}
