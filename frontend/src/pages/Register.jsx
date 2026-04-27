import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Lock, ArrowRight, UserPlus } from 'lucide-react';
import { register } from '../api/api';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username.trim() || !password.trim()) {
      setError('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await register({ username, password });
      // Save token and user info to localStorage
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user_id', response.data.user_id);
      localStorage.setItem('username', response.data.username);
      // Redirect to home page
      navigate('/');
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Registration failed. Please try again.';
      setError(errorMessage);
      console.error('Register error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-8 py-24">
      <div className="w-full max-w-md bg-surface-container-lowest rounded-2xl shadow-xl overflow-hidden border border-primary/5">
        <div className="p-10">
          <div className="text-center mb-10">
            <h2 className="font-headline text-4xl font-bold text-primary mb-2">Create Account</h2>
            <p className="text-on-surface-variant font-body tracking-tight">Join our intentional travelers community.</p>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-primary ml-1">Username</label>
              <div className="flex items-center bg-surface-container-highest rounded-lg px-4 py-3 focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                <User size={18} className="text-outline mr-3" />
                <input 
                  type="text"
                  className="w-full bg-transparent border-none focus:outline-none text-on-surface placeholder:text-outline" 
                  placeholder="Choose a username" 
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-primary ml-1">Password</label>
              <div className="flex items-center bg-surface-container-highest rounded-lg px-4 py-3 focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                <Lock size={18} className="text-outline mr-3" />
                <input 
                  type="password"
                  className="w-full bg-transparent border-none focus:outline-none text-on-surface placeholder:text-outline" 
                  placeholder="Create a password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-primary ml-1">Confirm Password</label>
              <div className="flex items-center bg-surface-container-highest rounded-lg px-4 py-3 focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                <Lock size={18} className="text-outline mr-3" />
                <input 
                  type="password"
                  className="w-full bg-transparent border-none focus:outline-none text-on-surface placeholder:text-outline" 
                  placeholder="Repeat your password" 
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>

            <button 
              type="submit"
              disabled={loading}
              className="mt-4 bg-primary text-on-primary py-4 rounded-lg shadow-sm font-bold hover:opacity-90 active:scale-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? "Creating Account..." : <><UserPlus size={18} /> Sign Up</>}
            </button>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}
          </form>

          <div className="mt-10 text-center">
            <p className="text-on-surface-variant text-sm">
              Already have an account?{' '}
              <Link to="/login" className="text-primary font-bold hover:underline underline-offset-4">
                Log in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;