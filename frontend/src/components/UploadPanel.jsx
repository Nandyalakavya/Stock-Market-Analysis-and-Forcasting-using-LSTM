export default function UploadPanel({ files, onUpload, onSelect }) {
  return (
    <>
      <h3>Upload CSV</h3>
      <input type="file" accept=".csv" onChange={e => onUpload(e.target.files[0])} />

      <h3>Available CSV files</h3>
      <select onChange={e => onSelect(e.target.value)}>
        <option value="">Select CSV</option>
        {files.map((f, i) => (
          <option key={i} value={f}>{f}</option>
      ))}
      </select>
    </>
  );
}
