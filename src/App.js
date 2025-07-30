
import React, { useState } from 'react';
import './App.css';

function App() {
  const [entries, setEntries] = useState([]);
  const [photo, setPhoto] = useState(null);
  const [observation, setObservation] = useState("");

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) setPhoto(URL.createObjectURL(file));
  };

  const handleSubmit = () => {
    if (!photo || !observation) return;
    setEntries([...entries, { photo, observation }]);
    setPhoto(null);
    setObservation("");
  };

  return (
    <div className="App">
      <h1>EHS Site Audit Agent</h1>

      <div className="upload-section">
        <label>Upload Photo:</label>
        <input type="file" accept="image/*" onChange={handleUpload} />

        <label>Your Observation:</label>
        <textarea
          placeholder="Describe what you think is wrong..."
          value={observation}
          onChange={(e) => setObservation(e.target.value)}
        />

        <button onClick={handleSubmit}>Submit Observation</button>
      </div>

      <div className="entries">
        {entries.map((entry, index) => (
          <div key={index} className="entry">
            <img src={entry.photo} alt={`Observation ${index + 1}`} />
            <p><strong>Your Observation:</strong> {entry.observation}</p>
            <p><em>(AI feedback and OSHA ref will go here)</em></p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
