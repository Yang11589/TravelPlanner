import { useState } from "react";
import { Sparkles, Send, MapPin, Calendar, LogIn } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { createPlan } from "../api/api"
import { motion } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";

const ChatBox = () => {
  const [city, setCity] = useState('');
  const [days, setDays] = useState(1);
  const [cityError, setCityError] = useState('');
  const { request: getTravelPlan, loading, error, data: result } = useApi(createPlan);
  const isLoggedIn = !!localStorage.getItem("access_token");
  const navigate = useNavigate();


  const handleSend = async () => {
  if (!city.trim()) {
    setCityError("Please enter a destination");
    return;
  }

  try {
    const generatedPlan = await getTravelPlan({ city, days });

    const conversationState = {
      city: generatedPlan.city,
      days: generatedPlan.days,
      itinerary: generatedPlan.itinerary,
      tripId: generatedPlan.id ?? null,
      messages: [],
    };

    navigate(
      generatedPlan.id
        ? `/conversation/${generatedPlan.id}`
        : "/conversation",
      { state: conversationState },
    );
  } catch (err) {
  }
};

  return (
    <section className="max-w-7xl mx-auto px-8 py-12 lg:py-20 flex flex-col items-center">
      <div className="text-center mb-12">
        <span className="font-label text-sm uppercase tracking-widest text-primary font-bold mb-4 block">Personalized Travel Planning</span>
        <h1 className="font-headline text-5xl md:text-7xl font-bold text-on-surface max-w-4xl leading-tight">
          Where will your next <span className="serif-italic text-secondary">story</span> begin?
        </h1>
      </div>

      <div className="w-full max-w-4xl flex flex-col gap-8">
        <div className="bg-surface-container-lowest rounded-xl shadow-sm p-2 flex flex-col relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none"></div>
          <div className="p-6 md:p-10 flex flex-col gap-6 z-10">

            {/* Prompt */}
            <div className="flex gap-4 items-start">
              <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Sparkles className="text-on-primary" size={20} />
              </div>
              <div className="bg-surface-container-low p-4 rounded-xl rounded-tl-none max-w-[80%]">
                <p className="text-on-surface leading-relaxed">Hello! I'm your expedition curator. Tell me where you'd like to go and for how long.</p>
              </div>
            </div>
            
            {/* City */}
            <div className="mt-4 flex flex-col md:flex-row gap-4 items-stretch md:items-end">
              <div className="flex-grow flex flex-col gap-2">
                <label className="text-xs font-bold uppercase tracking-wider text-primary ml-1">Destination</label>
                <div className="flex items-center bg-surface-container-highest rounded-lg px-4 py-3 focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                  <MapPin size={18} className="text-outline mr-3" />
                  <input 
                    type="text"
                    className="w-full bg-transparent border-none focus:outline-none text-on-surface placeholder:text-outline" 
                    placeholder="Where do you want to go?" 
                    value={city}
                    onChange={(e) => {
                      setCity(e.target.value);
                      if (cityError) setCityError('');
                    }}
                  />
                </div>
                {cityError && (
                  <p className="text-red-500 text-sm ml-1">{cityError}</p>
                )}
              </div>

              {/* Days */}
              <div className="w-full md:w-32 flex flex-col gap-2">
                <label className="text-xs font-bold uppercase tracking-wider text-primary ml-1">Days</label>
                <div className="flex items-center bg-surface-container-highest rounded-lg px-4 py-3 focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                  <Calendar size={18} className="text-outline mr-3" />
                  <input 
                    type="number"
                    min="1"
                    className="w-full bg-transparent border-none focus:outline-none text-on-surface" 
                    value={days}
                    onChange={(e) => setDays(parseInt(e.target.value) || 1)}
                  />
                </div>
              </div>

              {/* Generate Button */}
              <button 
                onClick={handleSend}
                disabled={loading}
                className="bg-primary text-on-primary px-8 py-4 rounded-lg shadow-sm hover:opacity-90 active:scale-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2 font-bold cursor-pointer"
              >
                {loading ? "Generating..." : <><Send size={18} /> Generate</>}
              </button>
            </div>
            
            {error && (
              <div className="text-red-500 text-sm mt-2 px-2 bg-red-50 p-3 rounded border border-red-200">
                <strong>Error:</strong> {error.response?.data?.detail || error.message || "Request failed"}
              </div>
            )}
          </div>
        </div>

        {/* Result */}
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-surface-container-lowest rounded-xl shadow-md p-8 border border-primary/10"
          >
            <div className="flex justify-between items-start mb-6">
              <h3 className="font-headline text-2xl font-bold text-primary">Your Curated Itinerary</h3>
              {!result.is_saved && (
                <div className="text-xs bg-amber-50 border border-amber-200 text-amber-700 px-3 py-1 rounded-full">
                  ⚠️ Not Saved
                </div>
              )}
              {result.is_saved && (
                <div className="text-xs bg-green-50 border border-green-200 text-green-700 px-3 py-1 rounded-full">
                  ✓ Saved
                </div>
              )}
            </div>

            {!result.is_saved && !isLoggedIn && (
              <div className="mb-6 bg-blue-50 border-l-4 border-primary p-4 rounded">
                <p className="text-sm text-on-surface mb-3">
                  Your plan will be temporary. <Link to="/login" className="text-primary font-semibold hover:underline">Sign in</Link> to save it permanently.
                </p>
              </div>
            )}
            
            <div className="prose prose-slate max-w-none text-on-surface-variant leading-relaxed">
              <h2>
                {result.city} ({result.days} days)
              </h2>

              {result.itinerary.map((day) => (
                <div key={day.day} style={{ marginTop: 20 }}>
                  <h3>Day {day.day}</h3>

                  <ul>
                    {day.places.map((p, i) => (
                      <li key={i}>
                        {p.type === "attraction" ? "sight: " : "food: "} {p.name}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
              <p className="whitespace-pre-wrap">{result.createPlan}</p>
              <button
                type="button"
                onClick={() =>
                  navigate(
                    result.id
                      ? `/conversation/${result.id}`
                      : "/conversation",
                    {
                      state: {
                        city: result.city,
                        days: result.days,
                        itinerary: result.itinerary,
                        tripId: result.id ?? null,
                        messages: [],
                      },
                    },
                  )
                }
                className="bg-primary text-on-primary px-6 py-3 rounded-lg"
              >
                Adjust Plan with AI Assistant
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default ChatBox;