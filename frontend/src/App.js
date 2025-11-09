import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "@/components/ThemeProvider";
import { Toaster } from "@/components/ui/sonner";
import Navbar from "@/components/Navbar";
import LandingPage from "@/pages/LandingPage";
import Dashboard from "@/pages/Dashboard";
import UserProfile from "@/pages/UserProfile";
import AnimationViewer from "@/pages/AnimationViewer";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (token && storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData, token) => {
    setUser(userData);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <ThemeProvider defaultTheme="dark" storageKey="css-animation-theme">
      <div className="App">
        <BrowserRouter>
          {user && <Navbar user={user} onLogout={handleLogout} />}
          <Routes>
            <Route 
              path="/" 
              element={user ? <Navigate to="/dashboard" /> : <LandingPage onLogin={handleLogin} />} 
            />
            <Route 
              path="/dashboard" 
              element={user ? <Dashboard user={user} /> : <Navigate to="/" />} 
            />
            <Route 
              path="/profile/:userId" 
              element={user ? <UserProfile currentUser={user} /> : <Navigate to="/" />} 
            />
            <Route 
              path="/animation/:animationId" 
              element={user ? <AnimationViewer user={user} /> : <Navigate to="/" />} 
            />
          </Routes>
        </BrowserRouter>
        <Toaster />
      </div>
    </ThemeProvider>
  );
}

export default App;
