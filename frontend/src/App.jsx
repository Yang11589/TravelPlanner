import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "./pages/Chat";
import TripsPage from "./pages/TripRecord";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/trips" element={<TripsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;