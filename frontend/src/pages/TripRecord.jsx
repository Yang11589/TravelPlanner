import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import { getTrips } from "../api/api";

export default function TripsPage() {
  const navigate = useNavigate();

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
      <h1>Your Trips</h1>

      {trips.map((trip) => (
        <div
          key={trip.id}
          style={{
            border: "1px solid #ccc",
            margin: 10,
            padding: 10,
            cursor: "pointer",
          }}
          onClick={() => navigate(`/conversation/${trip.id}`)}
        >
          <h2>
            {trip.city} ({trip.days} days)
          </h2>

          {trip.itinerary.map((day) => (
            <div key={day.day}>
              <strong>Day {day.day}</strong>
              <ul>
                {day.places.map((place) => (
                  <li key={`${day.day}-${place.name}`}>
                    {place.name}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}