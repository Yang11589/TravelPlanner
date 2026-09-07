import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "./pages/Chat";
import TripsPage from "./pages/TripRecord";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import ConversationPage from "./pages/Conversation";

function App() {
  return (
    <BrowserRouter>
    <Navbar />
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/trips" element={<TripsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/conversation" element={<ConversationPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;