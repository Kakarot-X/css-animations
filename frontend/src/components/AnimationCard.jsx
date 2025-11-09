import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";
import AnimationPreview from "@/components/AnimationPreview";
import { formatDistanceToNow } from "date-fns";

const AnimationCard = ({ animation, currentUserId, onLike }) => {
  const navigate = useNavigate();
  const isLiked = animation.likes?.includes(currentUserId);

  return (
    <Card 
      className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
      data-testid={`animation-card-${animation.id}`}
    >
      <div onClick={() => navigate(`/animation/${animation.id}`)}>
        <div className="aspect-video bg-muted flex items-center justify-center p-4">
          <AnimationPreview
            cssCode={animation.css_code}
            shape={animation.shape_type}
            isPlaying={true}
            small={true}
          />
        </div>
      </div>

      <CardContent className="p-4">
        <h3 
          className="font-semibold text-lg mb-2 cursor-pointer hover:underline"
          onClick={() => navigate(`/animation/${animation.id}`)}
          data-testid={`animation-title-${animation.id}`}
        >
          {animation.title}
        </h3>

        <div className="flex items-center justify-between">
          <div 
            className="flex items-center gap-2 cursor-pointer hover:opacity-80"
            onClick={() => navigate(`/profile/${animation.user_id}`)}
          >
            <Avatar className="h-8 w-8">
              <AvatarImage src={animation.user_profile_picture} />
              <AvatarFallback>{animation.username[0].toUpperCase()}</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-sm font-medium" data-testid={`animation-username-${animation.id}`}>{animation.username}</p>
              <p className="text-xs text-muted-foreground">
                {formatDistanceToNow(new Date(animation.created_at), { addSuffix: true })}
              </p>
            </div>
          </div>

          <Button
            variant={isLiked ? "default" : "outline"}
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onLike(animation.id);
            }}
            data-testid={`like-btn-${animation.id}`}
          >
            <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
            <span className="ml-2">{animation.likes_count || 0}</span>
          </Button>
        </div>

        <div className="mt-3">
          <span className="inline-block bg-muted px-3 py-1 rounded-full text-xs">
            {animation.category}
          </span>
        </div>
      </CardContent>
    </Card>
  );
};

export default AnimationCard;
