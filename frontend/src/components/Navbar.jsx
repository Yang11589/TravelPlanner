import React from 'react';
import { Link } from "react-router-dom";
import { UserCircle } from 'lucide-react';

const Navbar = () => (
  <nav className="fixed top-0 w-full z-50 bg-[#f7f9fb]/80 backdrop-blur-xl shadow-sm shadow-cyan-900/5">
    <div className="flex justify-between items-center w-full px-8 py-4 max-w-7xl mx-auto">
      {/* Logo */}
      <div className="text-2xl serif-italic font-bold text-primary">
        The Curated Expedition
      </div>

      <div className="flex items-center gap-4">
        {/* My Trips */}
        <Link 
          to="/trips"            
          className="text-slate-600 font-medium hover:text-primary hover:opacity-80 transition-all duration-300 active:scale-95">
           My Trips
        </Link>

        {/* User Icon */}
        <Link to="/login" className="text-slate-600 hover:text-primary transition-colors cursor-pointer">
            <UserCircle size={28} />
        </Link>

        {/* Plan */}
        <Link
          to="/"
          className="bg-gradient-to-br from-primary to-primary-container text-on-primary px-6 py-2 rounded-lg font-semibold hover:opacity-80 transition-all duration-300 active:scale-95">
           Plan Now
        </Link>
      </div>
    </div>
  </nav>
);

export default Navbar