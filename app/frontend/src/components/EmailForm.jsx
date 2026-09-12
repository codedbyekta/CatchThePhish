export default function EmailForm({ subject, body, onSubjectChange, onBodyChange, onSubmit, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form className="email-form" onSubmit={handleSubmit}>
      <label htmlFor="subject">
        Subject <span className="optional">(optional)</span>
      </label>
      <input
        id="subject"
        type="text"
        placeholder="e.g. Urgent: Verify your account"
        value={subject}
        onChange={(e) => onSubjectChange(e.target.value)}
        maxLength={2000}
      />

      <label htmlFor="body">
        Body <span className="required">*</span>
      </label>
      <textarea
        id="body"
        rows={10}
        placeholder="Paste the full email body here..."
        value={body}
        onChange={(e) => onBodyChange(e.target.value)}
        maxLength={20000}
        required
      />

      <button type="submit" disabled={loading || body.trim().length === 0}>
        {loading ? "Analyzing..." : "Check Email"}
      </button>
    </form>
  );
}
