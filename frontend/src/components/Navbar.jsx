import { Link, useNavigate } from "react-router-dom";
import { Moon, Sun, LogOut, User, Search } from "lucide-react";
import { useTheme } from "@/components/ThemeProvider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import axios from "axios";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Navbar = ({ user, onLogout }) => {
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.trim().length > 0) {
      try {
        const response = await axios.get(`${API}/users/search?q=${query}`);
        setSearchResults(response.data);
        setShowResults(true);
      } catch (error) {
        console.error("Search error:", error);
      }
    } else {
      setSearchResults([]);
      setShowResults(false);
    }
  };

  const handleUserClick = (userId) => {
    setShowResults(false);
    setSearchQuery("");
    setTimeout(() => {
      navigate(`/profile/${userId}`);
      window.location.reload();
    }, 100);
  };

  return (
    <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">CA</span>
          </div>
          <span className="font-bold text-xl">CSS Animations</span>
        </Link>

        <div className="flex-1 max-w-md mx-8 relative">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              data-testid="search-users-input"
              type="text"
              placeholder="Search users..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              onBlur={() => setTimeout(() => setShowResults(false), 300)}
              onFocus={() => searchQuery && setShowResults(true)}
              className="pl-9"
            />
          </div>
          {showResults && searchResults.length > 0 && (
            <div className="absolute top-full mt-2 w-full bg-background border rounded-lg shadow-lg max-h-64 overflow-y-auto z-50">
              {searchResults.map((result) => (
                <div
                  key={result.id}
                  data-testid={`search-result-${result.username}`}
                  className="p-3 hover:bg-muted cursor-pointer flex items-center space-x-3"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    handleUserClick(result.id);
                  }}
                >
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={result.profile_picture} />
                    <AvatarFallback>{result.username[0].toUpperCase()}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium text-sm">{result.username}</p>
                    {result.bio && <p className="text-xs text-muted-foreground truncate">{result.bio}</p>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <Button
            data-testid="theme-toggle-btn"
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" data-testid="user-menu-btn">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user.profile_picture} />
                  <AvatarFallback>{user.username[0].toUpperCase()}</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => navigate(`/profile/${user.id}`)} data-testid="profile-menu-item">
                <User className="mr-2 h-4 w-4" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onLogout} data-testid="logout-menu-item">
                <LogOut className="mr-2 h-4 w-4" />
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
