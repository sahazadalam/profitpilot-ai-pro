import { Search, Bell, Moon, Sun, User, Sparkles } from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';
import { Input } from '@/components/ui/input';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Link } from 'react-router-dom';

export const TopNavbar = () => {
  const { theme, toggleTheme } = useTheme();
  const { user, isDemoMode } = useAuth();

  return (
    <header className="flex h-16 items-center border-b px-4 md:px-6">
      <div className="flex flex-1 items-center gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search..."
            className="pl-9"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        {isDemoMode && (
          <Badge variant="warning" className="gap-1">
            <Sparkles className="h-3 w-3" />
            Demo
          </Badge>
        )}

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleTheme}
          className="rounded-lg p-2 hover:bg-accent"
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </motion.button>

        <button className="rounded-lg p-2 hover:bg-accent">
          <Bell size={20} />
        </button>

        <Link to="/profile">
          <Avatar className="h-8 w-8 cursor-pointer">
            <AvatarFallback className="bg-primary/10 text-primary">
              {user?.full_name?.charAt(0).toUpperCase() || 'U'}
            </AvatarFallback>
          </Avatar>
        </Link>
      </div>
    </header>
  );
};



