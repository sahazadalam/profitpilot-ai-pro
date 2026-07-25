import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Server, Database, Globe, Activity, CheckCircle, Lock } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const SystemStatus = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.email === 'sahzadalam114@gmail.com';

  const statuses = [
    { name: 'API Server', icon: Server, status: 'Operational', color: 'text-green-500' },
    { name: 'Database', icon: Database, status: 'Operational', color: 'text-green-500' },
    { name: 'Network', icon: Globe, status: 'Operational', color: 'text-green-500' },
    { name: 'Performance', icon: Activity, status: 'Healthy', color: 'text-green-500' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div>
        <h1 className="text-3xl font-bold tracking-tight">System Status</h1>
        <p className="text-muted-foreground">Monitor system health and performance</p>
        {!isAdmin && (
          <div className="flex items-center gap-2 mt-1 text-sm text-yellow-500">
            <Lock className="h-4 w-4" />
            <span>Admin access required to view system status</span>
          </div>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statuses.map((item) => (
          <Card key={item.name}>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="rounded-lg bg-primary/10 p-3">
                  <item.icon className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-medium">{item.name}</p>
                  <div className="flex items-center gap-1">
                    <CheckCircle className={'h-4 w-4 ' + item.color} />
                    <span className={'text-sm ' + item.color}>{item.status}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {isAdmin && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>System Metrics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Response Time</span>
                <span className="font-medium text-green-500">28ms</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">CPU Usage</span>
                <span className="font-medium">32%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Memory Usage</span>
                <span className="font-medium">45%</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Uptime</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm">Today</span>
                <span className="font-medium text-green-500">99.9%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">This Week</span>
                <span className="font-medium text-green-500">99.8%</span>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </motion.div>
  );
};


