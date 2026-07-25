import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Shield, Plus, Lock } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const RoleManagement = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'Admin' || user?.email === 'sahzadalam114@gmail.com';

  const roles = [
    { id: 1, name: 'Admin', description: 'Full system access', users: 3 },
    { id: 2, name: 'Manager', description: 'Manage teams and reports', users: 8 },
    { id: 3, name: 'User', description: 'Standard user access', users: 25 },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Role Management</h1>
          <p className="text-muted-foreground">Manage roles and permissions</p>
          {!isAdmin && (
            <div className="flex items-center gap-2 mt-1 text-sm text-yellow-500">
              <Lock className="h-4 w-4" />
              <span>Admin access required to manage roles</span>
            </div>
          )}
        </div>
        {isAdmin && (
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Create Role
          </Button>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {roles.map((role) => (
          <Card key={role.id}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-primary" />
                {role.name}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{role.description}</p>
              <p className="mt-2 text-sm">{role.users} users</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </motion.div>
  );
};

