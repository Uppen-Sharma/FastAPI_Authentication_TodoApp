// New todo form
export default function TodoForm({ title, onTitleChange, onSubmit }) {
  return (
    <form className="row" onSubmit={onSubmit}>
      <input
        placeholder="New todo"
        value={title}
        onChange={(e) => onTitleChange(e.target.value)}
        required
      />
      <button type="submit">Add</button>
    </form>
  );
}
