import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Search, Download, Lock } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const AuditLogs = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'Admin' || user?.email === 'sahzadalam114@gmail.com';

  const logs = [
    { id: 1, user: 'John Doe', action: 'Login', resource: 'Authentication', timestamp: '2026-07-21 14:30:00', status: 'Success' },
    { id: 2, user: 'Jane Smith', action: 'Update Product', resource: 'Product ID: 123', timestamp: '2026-07-21 14:15:00', status: 'Success' },
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
          <h1 className="text-3xl font-bold tracking-tight">Audit Logs</h1>
          <p className="text-muted-foreground">Track all system activities</p>
        </div>
        <Button variant="outline" className="gap-2" disabled={!isAdmin}>
          <Download className="h-4 w-4" />
          Export Logs
        </Button>
      </div>

      {!isAdmin && (
        <div className="flex items-center gap-2 p-3 text-sm text-yellow-500 bg-yellow-500/10 rounded-lg">
          <Lock className="h-4 w-4" />
          <span>Admin access required to view audit logs</span>
        </div>
      )}

      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Search logs..." className="pl-9" disabled={!isAdmin} />
            </div>
          </div>
          {isAdmin && (
            <div className="mt-6 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="px-4 py-3 text-left">User</th>
                    <th className="px-4 py-3 text-left">Action</th>
                    <th className="px-4 py-3 text-left">Resource</th>
                    <th className="px-4 py-3 text-left">Timestamp</th>
                    <th className="px-4 py-3 text-left">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log) => (
                    <tr key={log.id} className="border-b hover:bg-muted/50">
                      <td className="px-4 py-3">{log.user}</td>
                      <td className="px-4 py-3">{log.action}</td>
                      <td className="px-4 py-3">{log.resource}</td>
                      <td className="px-4 py-3 text-muted-foreground">{log.timestamp}</td>
                      <td className="px-4 py-3">
                        <span className="rounded-full bg-green-500 px-2 py-1 text-xs text-white">Success</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

