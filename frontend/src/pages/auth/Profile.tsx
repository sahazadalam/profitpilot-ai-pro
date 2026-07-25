import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { User, Mail, Calendar, LogOut } from 'lucide-react';

export const Profile = () => {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div className="container mx-auto max-w-4xl py-8">
      <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
      <p className="text-muted-foreground">Manage your account settings</p>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <Avatar className="h-16 w-16">
                <AvatarFallback className="bg-primary/10 text-2xl text-primary">
                  {user.full_name.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold">{user.full_name}</h3>
                <p className="text-sm text-muted-foreground">{user.role}</p>
              </div>
            </div>

            <div className="space-y-3 pt-4">
              <div className="flex items-center gap-3 text-sm">
                <User className="h-4 w-4 text-muted-foreground" />
                <span className="font-medium">Full Name</span>
                <span className="text-muted-foreground">{user.full_name}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <span className="font-medium">Email</span>
                <span className="text-muted-foreground">{user.email}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span className="font-medium">Joined</span>
                <span className="text-muted-foreground">
                  {new Date(user.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>

            <Button
              variant="destructive"
              className="w-full gap-2"
              onClick={logout}
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

