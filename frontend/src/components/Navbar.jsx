import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from "react-router-dom";
import { UserCircle, LogOut } from 'lucide-react';
import { getCurrentUser, logout as logoutApi } from '../api/api';

const Navbar = () => {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [username, setUsername] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Check user status on mount and when location changes
  const checkUserStatus = async () => {
    const token = localStorage.getItem('access_token');
    const hasValidToken = token && token !== 'undefined' && token !== 'null';

    if (hasValidToken) {
      try {
        const response = await getCurrentUser();
        setUsername(response.data.username);
        setIsLoggedIn(true);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_id');
          localStorage.removeItem('username');
        }
        setIsLoggedIn(false);
        setUsername(null);
      }
    } else {
      localStorage.removeItem('access_token');
      setIsLoggedIn(false);
      setUsername(null);
    }
  };

  // Check user status on mount and when location changes
  useEffect(() => {
    checkUserStatus();
  }, [location]);

  const handleLogout = async () => {
    try {
      await logoutApi();
    } catch (err) {
      console.error('Logout API error:', err);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('username');
      setUsername(null);
      setIsLoggedIn(false);
      setShowUserMenu(false);
      navigate('/');
    }
  };

  // Utility function to get user initials for avatar
  const getInitials = (name) => {
    if (!name) return '';
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <nav className="fixed top-0 w-full z-50 bg-[#f7f9fb]/80 backdrop-blur-xl shadow-sm shadow-cyan-900/5">
      <div className="flex justify-between items-center w-full px-8 py-4 max-w-7xl mx-auto">
        {/* Logo */}
        <div className="text-2xl serif-italic font-bold text-primary">
          The Curated Expedition
        </div>

        <div className="flex items-center gap-4">
          {/* My Trips */}
          {isLoggedIn ? (
            <Link 
              to="/trips"            
              className="text-slate-600 font-medium hover:text-primary hover:opacity-80 transition-all duration-300 active:scale-95">
              My Trips
            </Link>
          ) : (
            <button 
              disabled
              title="Sign in to view your trips"
              className="text-slate-300 font-medium cursor-not-allowed opacity-50">
              My Trips
            </button>
          )}

          {/* User Menu */}
          <div className="relative">
            {isLoggedIn ? (
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center font-semibold text-sm hover:opacity-90 transition-all cursor-pointer"
                title={username}
              >
                {getInitials(username)}
              </button>
            ) : (
              <Link to="/login" className="text-slate-600 hover:text-primary transition-colors cursor-pointer">
                <UserCircle size={28} />
              </Link>
            )}

            {/* User Dropdown Menu */}
            {isLoggedIn && showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 overflow-hidden z-50">
                <div className="px-4 py-3 border-b border-slate-200 bg-slate-50">
                  <p className="text-sm font-semibold text-slate-900">{username}</p>
                </div>
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 transition-colors"
                >
                  <LogOut size={16} />
                  Sign Out
                </button>
              </div>
            )}
          </div>

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
};

export default Navbar;