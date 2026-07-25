import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Bell, Lock, Palette, Shield, Save, LogOut } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';

export const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);

  const handleSave = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert('Settings saved successfully!');
    }, 1000);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6 min-h-screen"
      style={{ backgroundColor: '#0b1324' }}
    >
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Settings</h1>
        <p className="text-gray-400">Manage your application settings</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="md:col-span-1">
          <Card className="bg-[#111c2f] border-[#1e2a44]">
            <CardContent className="p-4 space-y-2">
              <button
                onClick={() => setActiveTab('profile')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-gray-400 hover:bg-[#1e2a44] hover:text-white"
              >
                <User className="h-4 w-4" />
                Profile
              </button>
              <button
                onClick={() => setActiveTab('security')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-gray-400 hover:bg-[#1e2a44] hover:text-white"
              >
                <Lock className="h-4 w-4" />
                Security
              </button>
              <button
                onClick={() => setActiveTab('appearance')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-gray-400 hover:bg-[#1e2a44] hover:text-white"
              >
                <Palette className="h-4 w-4" />
                Appearance
              </button>
              <button
                onClick={() => setActiveTab('notifications')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-gray-400 hover:bg-[#1e2a44] hover:text-white"
              >
                <Bell className="h-4 w-4" />
                Notifications
              </button>
              <button
                onClick={() => setActiveTab('system')}
                className="w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-gray-400 hover:bg-[#1e2a44] hover:text-white"
              >
                <Shield className="h-4 w-4" />
                System
              </button>
              <div className="pt-4 border-t border-[#1e2a44]">
                <button className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-red-400 hover:bg-red-900/20 hover:text-red-300 transition-colors">
                  <LogOut className="h-4 w-4" />
                  Logout
                </button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Content */}
        <div className="md:col-span-3">
          <Card className="bg-[#111c2f] border-[#1e2a44]">
            <CardHeader>
              <CardTitle className="text-white">
                {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Settings
              </CardTitle>
            </CardHeader>
            <CardContent>
              {activeTab === 'profile' && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-gray-300">Full Name</Label>
                    <Input defaultValue="John Doe" className="bg-[#0b1324] border-[#1e2a44] text-white" />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Email</Label>
                    <Input defaultValue="john@profitpilot.com" className="bg-[#0b1324] border-[#1e2a44] text-white" />
                  </div>
                  <Button onClick={handleSave} disabled={loading} className="bg-blue-600 hover:bg-blue-700 text-white">
                    {loading ? 'Saving...' : 'Save Changes'}
                  </Button>
                </div>
              )}
              {activeTab === 'security' && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-gray-300">Current Password</Label>
                    <Input type="password" placeholder="Enter current password" className="bg-[#0b1324] border-[#1e2a44] text-white" />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">New Password</Label>
                    <Input type="password" placeholder="Enter new password" className="bg-[#0b1324] border-[#1e2a44] text-white" />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-gray-300">Confirm Password</Label>
                    <Input type="password" placeholder="Confirm new password" className="bg-[#0b1324] border-[#1e2a44] text-white" />
                  </div>
                  <Button onClick={handleSave} disabled={loading} className="bg-blue-600 hover:bg-blue-700 text-white">
                    {loading ? 'Updating...' : 'Update Password'}
                  </Button>
                </div>
              )}
              {activeTab === 'appearance' && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-gray-300">Theme</Label>
                    <select className="w-full px-4 py-2 rounded-lg bg-[#0b1324] border-[#1e2a44] text-white">
                      <option value="dark">Dark</option>
                      <option value="light">Light</option>
                      <option value="system">System</option>
                    </select>
                  </div>
                  <Button onClick={handleSave} disabled={loading} className="bg-blue-600 hover:bg-blue-700 text-white">
                    {loading ? 'Saving...' : 'Save Theme'}
                  </Button>
                </div>
              )}
              {activeTab === 'notifications' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between py-2 border-b border-[#1e2a44]">
                    <span className="text-gray-300">Email Notifications</span>
                    <input type="checkbox" defaultChecked className="w-5 h-5 accent-blue-600" />
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-[#1e2a44]">
                    <span className="text-gray-300">Push Notifications</span>
                    <input type="checkbox" className="w-5 h-5 accent-blue-600" />
                  </div>
                  <div className="flex items-center justify-between py-2">
                    <span className="text-gray-300">Sales Alerts</span>
                    <input type="checkbox" defaultChecked className="w-5 h-5 accent-blue-600" />
                  </div>
                  <Button onClick={handleSave} disabled={loading} className="bg-blue-600 hover:bg-blue-700 text-white">
                    {loading ? 'Saving...' : 'Save Preferences'}
                  </Button>
                </div>
              )}
              {activeTab === 'system' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between py-2 border-b border-[#1e2a44]">
                    <span className="text-gray-300">Version</span>
                    <span className="text-white">v1.0.0</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-[#1e2a44]">
                    <span className="text-gray-300">Database Status</span>
                    <span className="text-green-400">Connected</span>
                  </div>
                  <div className="flex items-center justify-between py-2">
                    <span className="text-gray-300">API Status</span>
                    <span className="text-green-400">Online</span>
                  </div>
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                    <Save className="h-4 w-4 mr-2" />
                    Save System Settings
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </motion.div>
  );
};

export default SettingsPage;
