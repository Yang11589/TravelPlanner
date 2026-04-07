import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import ChatBox from "../components/ChatBox"

export default function ChatPage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async ({ city, days }) => {
    setLoading(true);

    try {
      await axios.post("http://127.0.0.1:8000/api/plan", {
        city,
        days,
      });

      navigate("/trips");
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>✈️ Travel Planner</h1>

      <ChatBox onSubmit={handleSubmit} loading={loading} />

      <button onClick={() => navigate("/trips")} style={{ marginTop: 20 }}>
        View History →
      </button>
    </div>
  );
}