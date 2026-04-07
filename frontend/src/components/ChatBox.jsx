import { useState } from "react";

export default function ChatBox({ onSubmit, loading }) {
  const [city, setCity] = useState("");
  const [days, setDays] = useState(1);

  const handleClick = () => {
    onSubmit({ city, days });
  };

  return (
    <div style={{ marginTop: 20 }}>
      <input
        placeholder="Where do you want to go?"
        value={city}
        onChange={(e) => setCity(e.target.value)}
      />

      <input
        type="number"
        value={days}
        onChange={(e) => setDays(e.target.value)}
      />

      <button onClick={handleClick} disabled={loading}>
        {loading ? "Generating..." : "Generate Trip"}
      </button>
    </div>
  );
}