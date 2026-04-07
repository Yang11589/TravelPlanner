import { useEffect, useState } from "react";
import axios from "axios";


export default function TripsPage() {
  const [trips, setTrips] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/trips")
      .then(res => setTrips(res.data.items));
  }, []);


  return (
    <div style={{ padding: 40 }}>
      <h1>📚 Your Trips</h1>

      {trips.map((trip, index) => (
        <div key={index} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
          <h2>{trip.city} ({trip.days} days)</h2>

          {trip.itinerary.map(day => (
            <div key={day.day}>
              <strong>Day {day.day}</strong>
              <ul>
                {day.places.map((p, i) => (
                  <li key={i}>{p.name}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

