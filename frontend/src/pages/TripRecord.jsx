import { useEffect } from "react";
import { useApi } from "../hooks/useApi";
import { getTrips } from "../api/api";

export default function TripsPage() {
  const {
    request: fetchTrips,
    data,
    loading,
  } = useApi(getTrips);

  useEffect(() => {
    fetchTrips();
  }, [fetchTrips]);

  const trips = data?.items || [];

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: 40 }}>
      <h1>📚 Your Trips</h1>

      {trips.map((trip, index) => (
        <div key={index} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
          <h2>{trip.city} ({trip.days} days)</h2>

          {trip.itinerary.map((day) => (
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