// ===================================================================
// FILE: frontend/src/App.jsx
// ===================================================================
import React, { useState, useEffect } from 'react';
import { User, Wallet, Trophy, CreditCard, Lock, Mail, Check, X } from 'lucide-react';

// API Base URL
const API_BASE = 'http://localhost:8000';

// Authentication Context
const AuthContext = React.createContext(null);

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const login = (userData, token) => {
    setUser(userData);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center">
        <div className="text-white text-2xl">Loading...</div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {!user ? <AuthPage /> : <MainApp />}
    </AuthContext.Provider>
  );
};

// Authentication Page Component
const AuthPage = () => {
  const { login } = React.useContext(AuthContext);
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!isLogin) {
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }
        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters');
          setLoading(false);
          return;
        }

        const response = await fetch(`${API_BASE}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            email: formData.email,
            password: formData.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Registration failed');
        }

        const loginResponse = await fetch(`${API_BASE}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password
          })
        });

        const loginData = await loginResponse.json();
        
        if (!loginResponse.ok) {
          throw new Error(loginData.detail || 'Login failed');
        }

        login(loginData.user, loginData.token);
      } else {
        const response = await fetch(`${API_BASE}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || 'Invalid credentials');
        }

        login(data.user, data.token);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 w-full max-w-md border border-white/20">
        <div className="text-center mb-8">
          <div className="inline-block bg-gradient-to-r from-yellow-400 to-orange-500 p-3 rounded-full mb-4">
            <Trophy className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">BetMasterX</h1>
          <p className="text-gray-300">Your Ultimate Betting Platform</p>
        </div>

        <div className="flex mb-6 bg-white/5 rounded-lg p-1">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 rounded-md transition-all ${
              isLogin
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                : 'text-gray-300'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 rounded-md transition-all ${
              !isLogin
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                : 'text-gray-300'
            }`}
          >
            Register
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Username
            </label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter username"
                required
              />
            </div>
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Enter email"
                  required
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Enter password"
                required
              />
            </div>
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Confirm password"
                  required
                />
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : isLogin ? 'Login' : 'Create Account'}
          </button>
        </div>

        <div className="mt-6 text-center text-gray-400 text-sm">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-purple-400 hover:text-purple-300 font-semibold"
          >
            {isLogin ? 'Register' : 'Login'}
          </button>
        </div>
      </div>
    </div>
  );
};

// Main Application Component
const MainApp = () => {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <Header setCurrentPage={setCurrentPage} />
      
      {currentPage === 'home' && <HomePage setCurrentPage={setCurrentPage} />}
      {currentPage === 'horse' && <HorseRacePage />}
      {currentPage === 'coming-soon' && <ComingSoonPage />}
    </div>
  );
};

// Header Component
const Header = ({ setCurrentPage }) => {
  const { user, logout } = React.useContext(AuthContext);
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    fetchBalance();
  }, []);

  const fetchBalance = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/user/balance`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setBalance(data.balance);
    } catch (err) {
      console.error('Failed to fetch balance:', err);
    }
  };

  return (
    <header className="bg-black/30 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div
            onClick={() => setCurrentPage('home')}
            className="flex items-center space-x-3 cursor-pointer"
          >
            <div className="bg-gradient-to-r from-yellow-400 to-orange-500 p-2 rounded-lg">
              <Trophy className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">BetMasterX</span>
          </div>

          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-full">
              <Wallet className="w-5 h-5 text-yellow-400" />
              <span className="text-white font-semibold">${balance.toFixed(2)}</span>
            </div>

            <div className="flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-full">
              <User className="w-5 h-5 text-purple-400" />
              <span className="text-white">{user.username}</span>
            </div>

            <button
              onClick={logout}
              className="bg-red-500/20 hover:bg-red-500/30 text-red-300 px-4 py-2 rounded-lg transition-all"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

// Home Page Component
const HomePage = ({ setCurrentPage }) => {
  const categories = [
    {
      id: 'horse',
      name: 'Horse Race',
      icon: '🐎',
      description: 'Bet on exciting horse races',
      available: true,
      gradient: 'from-green-500 to-emerald-600'
    },
    {
      id: 'cricket',
      name: 'Cricket',
      icon: '🏏',
      description: 'Coming Soon',
      available: false,
      gradient: 'from-blue-500 to-cyan-600'
    },
    {
      id: 'football',
      name: 'Football',
      icon: '⚽',
      description: 'Coming Soon',
      available: false,
      gradient: 'from-orange-500 to-red-600'
    },
    {
      id: 'payment',
      name: 'Payment Gateway',
      icon: '💳',
      description: 'Coming Soon',
      available: false,
      gradient: 'from-purple-500 to-pink-600'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-white mb-4">
          Welcome to BetMasterX
        </h1>
        <p className="text-gray-300 text-xl">
          Choose your game and start betting!
        </p>
      </div>

      <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-lg p-4 mb-8 text-center">
        <CreditCard className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
        <p className="text-yellow-200 font-semibold">
          Payment Gateway Integration Coming Soon!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {categories.map((category) => (
          <div
            key={category.id}
            onClick={() => category.available ? setCurrentPage(category.id) : setCurrentPage('coming-soon')}
            className={`bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 cursor-pointer transform transition-all hover:scale-105 hover:shadow-2xl ${
              !category.available ? 'opacity-60' : ''
            }`}
          >
            <div className={`bg-gradient-to-r ${category.gradient} p-4 rounded-lg mb-4 text-center`}>
              <span className="text-5xl">{category.icon}</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {category.name}
            </h3>
            <p className="text-gray-300 text-sm mb-4">
              {category.description}
            </p>
            {category.available ? (
              <div className="flex items-center text-green-400 text-sm">
                <Check className="w-4 h-4 mr-1" />
                Available Now
              </div>
            ) : (
              <div className="flex items-center text-yellow-400 text-sm">
                <X className="w-4 h-4 mr-1" />
                Coming Soon
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// Horse Race Page Component
const HorseRacePage = () => {
  const [selectedHorse, setSelectedHorse] = useState(null);
  const [betAmount, setBetAmount] = useState(10);
  const [racing, setRacing] = useState(false);
  const [result, setResult] = useState(null);
  const [balance, setBalance] = useState(0);

  const horses = [
    { id: 1, name: 'Thunder', color: 'from-red-500 to-orange-500', emoji: '🐎' },
    { id: 2, name: 'Lightning', color: 'from-blue-500 to-cyan-500', emoji: '🐴' },
    { id: 3, name: 'Storm', color: 'from-green-500 to-emerald-500', emoji: '🏇' },
    { id: 4, name: 'Blaze', color: 'from-purple-500 to-pink-500', emoji: '🐎' }
  ];

  useEffect(() => {
    fetchBalance();
  }, []);

  const fetchBalance = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/user/balance`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setBalance(data.balance);
    } catch (err) {
      console.error('Failed to fetch balance:', err);
    }
  };

  const placeBet = async () => {
    if (!selectedHorse) {
      alert('Please select a horse!');
      return;
    }

    if (betAmount > balance) {
      alert('Insufficient balance!');
      return;
    }

    setRacing(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE}/bets/horse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          horse_choice: selectedHorse,
          bet_amount: betAmount
        })
      });

      const data = await response.json();

      setTimeout(() => {
        setResult(data);
        setBalance(data.new_balance);
        setRacing(false);
      }, 3000);
    } catch (err) {
      console.error('Bet failed:', err);
      setRacing(false);
      alert('Failed to place bet. Please try again.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">Horse Race Betting</h1>
        <p className="text-gray-300">Select a horse and place your bet!</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {horses.map((horse) => (
          <div
            key={horse.id}
            onClick={() => !racing && setSelectedHorse(horse.id)}
            className={`bg-white/10 backdrop-blur-lg rounded-xl p-6 border-2 cursor-pointer transform transition-all hover:scale-105 ${
              selectedHorse === horse.id
                ? 'border-yellow-400 shadow-2xl'
                : 'border-white/20'
            } ${racing ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <div className={`bg-gradient-to-r ${horse.color} p-6 rounded-lg mb-4 text-center ${
              racing && result?.winning_horse === horse.id ? 'animate-pulse' : ''
            }`}>
              <span className="text-6xl">{horse.emoji}</span>
            </div>
            <h3 className="text-xl font-bold text-white text-center mb-2">
              Horse #{horse.id}
            </h3>
            <p className="text-gray-300 text-center">{horse.name}</p>
            {selectedHorse === horse.id && (
              <div className="mt-3 text-center">
                <Check className="w-6 h-6 text-yellow-400 mx-auto" />
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="max-w-2xl mx-auto bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
        <div className="mb-6">
          <label className="block text-white font-semibold mb-3">
            Bet Amount: ${betAmount}
          </label>
          <input
            type="range"
            min="10"
            max={Math.min(balance, 1000)}
            step="10"
            value={betAmount}
            onChange={(e) => setBetAmount(Number(e.target.value))}
            disabled={racing}
            className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-gray-400 text-sm mt-2">
            <span>$10</span>
            <span>${Math.min(balance, 1000)}</span>
          </div>
        </div>

        <button
          onClick={placeBet}
          disabled={racing || !selectedHorse}
          className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-4 rounded-lg font-bold text-lg hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {racing ? 'Racing...' : 'Place Bet'}
        </button>

        {result && (
          <div className={`mt-6 p-6 rounded-lg border-2 ${
            result.result === 'win'
              ? 'bg-green-500/20 border-green-500'
              : 'bg-red-500/20 border-red-500'
          }`}>
            <h3 className={`text-2xl font-bold mb-2 ${
              result.result === 'win' ? 'text-green-300' : 'text-red-300'
            }`}>
              {result.result === 'win' ? '🎉 You Won!' : '😔 You Lost'}
            </h3>
            <p className="text-white mb-2">
              Winning Horse: #{result.winning_horse} - {horses.find(h => h.id === result.winning_horse)?.name}
            </p>
            <p className="text-gray-300 mb-2">
              {result.result === 'win' 
                ? `You won $${result.winnings.toFixed(2)}!` 
                : `You lost $${betAmount.toFixed(2)}`}
            </p>
            <p className="text-yellow-400 font-semibold">
              New Balance: ${result.new_balance.toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// Coming Soon Page Component
const ComingSoonPage = () => {
  return (
    <div className="container mx-auto px-4 py-12 flex items-center justify-center min-h-[80vh]">
      <div className="text-center">
        <div className="text-8xl mb-6">🚧</div>
        <h1 className="text-5xl font-bold text-white mb-4">Coming Soon</h1>
        <p className="text-gray-300 text-xl mb-8">
          This feature is under development and will be available soon!
        </p>
        <div className="flex justify-center space-x-4">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
            <p className="text-gray-400 text-sm">Cricket Betting</p>
          </div>
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
            <p className="text-gray-400 text-sm">Football Betting</p>
          </div>
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
            <p className="text-gray-400 text-sm">Payment Gateway</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;