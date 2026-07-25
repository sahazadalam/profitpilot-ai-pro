import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Shield, Lock, Key, LogOut, CheckCircle, AlertTriangle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const SecurityCenter = () => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.email === 'sahzadalam114@gmail.com';

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Security Center</h1>
        <p className="text-muted-foreground">Manage your security settings</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              Password & Login
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button variant="outline" className="w-full justify-start gap-2">
              Change Password
            </Button>
            <Button variant="outline" className="w-full justify-start gap-2">
              <Lock className="h-4 w-4" />
              Enable Two-Factor Authentication
            </Button>
            <Button variant="outline" className="w-full justify-start gap-2 text-red-500 hover:text-red-700">
              <LogOut className="h-4 w-4" />
              Logout All Devices
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Active Sessions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between rounded-lg border p-3">
                <div>
                  <p className="font-medium">Chrome on Windows</p>
                  <p className="text-sm text-muted-foreground">Current session</p>
                </div>
                <span className="rounded-full bg-green-500 px-2 py-1 text-xs text-white">Active</span>
              </div>
              <div className="flex items-center justify-between rounded-lg border p-3">
                <div>
                  <p className="font-medium">Safari on iPhone</p>
                  <p className="text-sm text-muted-foreground">2 hours ago</p>
                </div>
                <span className="rounded-full bg-gray-500 px-2 py-1 text-xs text-white">Inactive</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5" />
              Security Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 text-green-500">
              <CheckCircle className="h-5 w-5" />
              <span>Your account is secure</span>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">Last security check: 2 minutes ago</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Security Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">No security alerts</p>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
};


