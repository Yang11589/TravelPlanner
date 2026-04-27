import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "./pages/Chat";
import TripsPage from "./pages/TripRecord";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/Login";

function App() {
  return (
    <BrowserRouter>
    <Navbar />
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/trips" element={<TripsPage />} />
        <Route path="/login" element={<LoginPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;