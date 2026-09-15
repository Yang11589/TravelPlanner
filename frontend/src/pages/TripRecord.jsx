import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { MessageCircle, Trash2 } from "lucide-react";
import { useApi } from "../hooks/useApi";
import { deleteTrip, getTrips } from "../api/api";

export default function TripsPage() {
  const navigate = useNavigate();

  const {
    request: fetchTrips,
    data,
    loading,
    error,
  } = useApi(getTrips);

  const {
    request: removeTrip,
    loading: deleting,
  } = useApi(deleteTrip);

  useEffect(() => {
    fetchTrips();
  }, [fetchTrips]);

  const trips = data?.items || [];

  const handleDelete = async (tripId) => {
    const confirmed = window.confirm(
      "Delete this trip and its conversation history?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await removeTrip(tripId);
      await fetchTrips();
    } catch {
      // The existing API hook exposes the request error.
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-background px-6 pb-12 pt-28">
        <p className="mx-auto max-w-5xl text-on-surface-variant">
          Loading trips...
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background px-6 pb-12 pt-28">
      <div className="mx-auto max-w-5xl">
        <div className="mb-10">
          <p className="mb-2 text-sm font-bold uppercase tracking-[0.2em] text-primary">
            Travel archive
          </p>
          <h1 className="font-headline text-4xl font-bold text-on-surface">
            Your Trips
          </h1>
          <p className="mt-2 text-on-surface-variant">
            Revisit a plan or continue its conversation.
          </p>
        </div>

        {error && (
          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            Failed to load your trips.
          </div>
        )}

        {trips.length === 0 ? (
          <div className="rounded-xl border border-outline-variant bg-surface-container-lowest p-10 text-center">
            <h2 className="font-headline text-2xl font-bold text-on-surface">
              No saved trips yet
            </h2>
            <p className="mt-2 text-on-surface-variant">
              Create a travel plan to see it here.
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2">
            {trips.map((trip) => (
              <article
                key={trip.id}
                className="flex flex-col rounded-xl border border-outline-variant bg-surface-container-lowest p-6 shadow-sm"
              >
                <div className="flex-1">
                  <p className="text-sm font-semibold uppercase tracking-wider text-primary">
                    {trip.days} days
                  </p>

                  <h2 className="mt-2 font-headline text-3xl font-bold text-on-surface">
                    {trip.city}
                  </h2>

                  <div className="mt-5 space-y-3">
                    {trip.itinerary?.slice(0, 2).map((day) => (
                      <div key={day.day}>
                        <p className="font-semibold text-on-surface">
                          Day {day.day}
                        </p>
                        <p className="mt-1 line-clamp-2 text-sm text-on-surface-variant">
                          {day.places?.map((place) => place.name).join(" · ")}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-8 flex flex-col gap-3 border-t border-outline-variant pt-5 sm:flex-row">
                  <button
                    type="button"
                    onClick={() => navigate(`/conversation/${trip.id}`)}
                    className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-primary px-4 py-3 font-semibold text-on-primary transition hover:opacity-90"
                  >
                    <MessageCircle size={18} />
                    Continue conversation
                  </button>

                  <button
                    type="button"
                    disabled={deleting}
                    onClick={() => handleDelete(trip.id)}
                    className="flex items-center justify-center gap-2 rounded-lg border border-red-200 px-4 py-3 font-semibold text-red-600 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <Trash2 size={18} />
                    {deleting ? "Deleting..." : "Delete"}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}