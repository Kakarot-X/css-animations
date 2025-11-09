import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { UserPlus, UserMinus, Calendar } from "lucide-react";
import axios from "axios";
import { toast } from "sonner";
import AnimationCard from "@/components/AnimationCard";
import { format } from "date-fns";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const UserProfile = ({ currentUser }) => {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [animations, setAnimations] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(true);

  const isOwnProfile = currentUser.id === userId;

  useEffect(() => {
    loadProfile();
    loadAnimations();
  }, [userId]);

  const loadProfile = async () => {
    try {
      const response = await axios.get(`${API}/users/${userId}`);
      setProfile(response.data);
      setIsFollowing(currentUser.following?.includes(userId) || false);
      setLoading(false);
    } catch (error) {
      console.error("Error loading profile:", error);
      toast.error("Failed to load profile");
    }
  };

  const loadAnimations = async () => {
    try {
      const response = await axios.get(`${API}/users/${userId}/animations`);
      setAnimations(response.data);
    } catch (error) {
      console.error("Error loading animations:", error);
    }
  };

  const handleFollow = async () => {
    try {
      const token = localStorage.getItem('token');
      if (isFollowing) {
        await axios.post(`${API}/users/${userId}/unfollow?token=${token}`);
        toast.success("Unfollowed successfully");
        setIsFollowing(false);
        
        // Update current user's following list
        const updatedUser = {
          ...currentUser,
          following: currentUser.following.filter(id => id !== userId)
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));
      } else {
        await axios.post(`${API}/users/${userId}/follow?token=${token}`);
        toast.success("Followed successfully");
        setIsFollowing(true);
        
        // Update current user's following list
        const updatedUser = {
          ...currentUser,
          following: [...(currentUser.following || []), userId]
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      loadProfile();
    } catch (error) {
      console.error("Error following/unfollowing:", error);
      toast.error("Action failed");
    }
  };

  const handleLike = async (animationId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/animations/${animationId}/like?token=${token}`);
      loadAnimations();
    } catch (error) {
      console.error("Error liking animation:", error);
    }
  };

  if (loading || !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
              <Avatar className="h-24 w-24">
                <AvatarImage src={profile.profile_picture} />
                <AvatarFallback className="text-3xl">{profile.username[0].toUpperCase()}</AvatarFallback>
              </Avatar>

              <div className="flex-1">
                <div className="flex items-center gap-4 mb-2">
                  <h1 className="text-3xl font-bold" data-testid="profile-username">{profile.username}</h1>
                  {!isOwnProfile && (
                    <Button
                      onClick={handleFollow}
                      variant={isFollowing ? "outline" : "default"}
                      data-testid="follow-btn"
                    >
                      {isFollowing ? (
                        <><UserMinus className="mr-2 h-4 w-4" />Unfollow</>
                      ) : (
                        <><UserPlus className="mr-2 h-4 w-4" />Follow</>
                      )}
                    </Button>
                  )}
                </div>
                <p className="text-muted-foreground mb-3" data-testid="profile-email">{profile.email}</p>
                {profile.bio && <p className="mb-4" data-testid="profile-bio">{profile.bio}</p>}

                <div className="flex items-center gap-6 text-sm">
                  <div>
                    <span className="font-bold" data-testid="animations-count">{profile.animations_count}</span>
                    <span className="text-muted-foreground ml-1">Animations</span>
                  </div>
                  <div>
                    <span className="font-bold" data-testid="followers-count">{profile.followers_count}</span>
                    <span className="text-muted-foreground ml-1">Followers</span>
                  </div>
                  <div>
                    <span className="font-bold" data-testid="following-count">{profile.following_count}</span>
                    <span className="text-muted-foreground ml-1">Following</span>
                  </div>
                  <div className="flex items-center text-muted-foreground">
                    <Calendar className="h-4 w-4 mr-1" />
                    <span>Joined {format(new Date(profile.joined_date), 'MMM yyyy')}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div>
          <h2 className="text-2xl font-bold mb-6">Animations</h2>
          {animations.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              {isOwnProfile ? "You haven't created any animations yet." : "This user hasn't created any animations yet."}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {animations.map((animation) => (
                <AnimationCard
                  key={animation.id}
                  animation={animation}
                  currentUserId={currentUser.id}
                  onLike={handleLike}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
