import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Search, UserPlus, Edit, Trash2, Shield, Lock } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const UserManagement = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'Admin' || user?.email === 'sahzadalam114@gmail.com';

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">User Management</h1>
          <p className="text-muted-foreground">Manage users and their permissions</p>
          {!isAdmin && (
            <div className="flex items-center gap-2 mt-1 text-sm text-yellow-500">
              <Lock className="h-4 w-4" />
              <span>Admin access required to manage users</span>
            </div>
          )}
        </div>
        {isAdmin && (
          <Button className="gap-2">
            <UserPlus className="h-4 w-4" />
            Add User
          </Button>
        )}
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Search users..." className="pl-9" />
            </div>
          </div>
          <div className="mt-6">
            <p className="text-center text-muted-foreground">
              {isAdmin ? 'User management interface will appear here' : 'Admin access required'}
            </p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

