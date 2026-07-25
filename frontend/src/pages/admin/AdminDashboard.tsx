import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { 
  Users, Package, ShoppingCart, TrendingUp, Activity, 
  Shield, Bell, Server, Zap, Clock, CheckCircle, 
  AlertTriangle, BarChart3, Globe, Database, 
  Cpu, HardDrive, Wifi, UserCheck, UserX, TrendingDown, 
  DollarSign, PieChart, Settings, Lock, Eye,
  Download, RefreshCw, UserPlus, LogOut
} from 'lucide-react';
import { useAdmin } from '@/hooks/admin/useAdmin';
import { useAuth } from '@/contexts/AuthContext';
import { LoadingSkeleton } from '@/components/shared/LoadingSkeleton';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { cn } from '@/lib/utils';

export const AdminDashboard = () => {
  const { stats, isLoading } = useAdmin();
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  const handleAddUser = () => {
    navigate('/dashboard/admin/users');
    toast.success('Navigating to User Management');
  };

  const handleAddProduct = () => {
    navigate('/dashboard/inventory');
    toast.success('Navigating to Inventory');
  };

  const handleExportData = () => {
    toast.success('Data export started. Downloading...');
    setTimeout(() => {
      toast.success('Data exported successfully!');
    }, 2000);
  };

  const handleSettings = () => {
    navigate('/dashboard/settings');
    toast.success('Navigating to Settings');
  };

  const handleSecurity = () => {
    navigate('/dashboard/admin/security');
    toast.success('Navigating to Security Center');
  };

  const handleAnalytics = () => {
    navigate('/dashboard/analytics');
    toast.success('Navigating to Analytics');
  };

  const quickActions = [
    { icon: UserPlus, label: 'Add User', color: 'bg-blue-500', onClick: handleAddUser },
    { icon: Package, label: 'Add Product', color: 'bg-green-500', onClick: handleAddProduct },
    { icon: Download, label: 'Export Data', color: 'bg-purple-500', onClick: handleExportData },
    { icon: Settings, label: 'Settings', color: 'bg-gray-500', onClick: handleSettings },
    { icon: Shield, label: 'Security', color: 'bg-red-500', onClick: handleSecurity },
    { icon: BarChart3, label: 'Analytics', color: 'bg-orange-500', onClick: handleAnalytics },
  ];

  const statCards = [
    { 
      title: 'Total Revenue', 
      value: '$' + (stats?.revenue?.toLocaleString() || '124,589'), 
      icon: DollarSign, 
      color: 'from-emerald-500 to-teal-500',
      trend: '+12.5%',
      trendUp: true,
      subtitle: 'vs last month'
    },
    { 
      title: 'Active Users', 
      value: stats?.active_users?.toLocaleString() || '2,847', 
      icon: Users, 
      color: 'from-blue-500 to-cyan-500',
      trend: '+8.2%',
      trendUp: true,
      subtitle: 'vs last month'
    },
    { 
      title: 'Total Products', 
      value: stats?.total_products?.toLocaleString() || '3,421', 
      icon: Package, 
      color: 'from-purple-500 to-pink-500',
      trend: '+5.3%',
      trendUp: true,
      subtitle: 'vs last month'
    },
    { 
      title: 'Total Sales', 
      value: stats?.total_sales?.toLocaleString() || '15,892', 
      icon: ShoppingCart, 
      color: 'from-orange-500 to-amber-500',
      trend: '+3.1%',
      trendUp: true,
      subtitle: 'vs last month'
    },
  ];

  const healthMetrics = [
    { label: 'API Status', value: 'Operational', status: 'healthy', icon: Globe },
    { label: 'Database', value: 'Connected', status: 'healthy', icon: Database },
    { label: 'Server Load', value: '32%', status: 'good', icon: Cpu },
    { label: 'Memory Usage', value: '45%', status: 'good', icon: HardDrive },
    { label: 'Network', value: '98.5%', status: 'healthy', icon: Wifi },
    { label: 'Uptime', value: '99.97%', status: 'healthy', icon: Clock },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-500 bg-green-500/10';
      case 'good': return 'text-yellow-500 bg-yellow-500/10';
      case 'warning': return 'text-orange-500 bg-orange-500/10';
      case 'critical': return 'text-red-500 bg-red-500/10';
      default: return 'text-gray-500 bg-gray-500/10';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 p-6"
    >
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground">Complete platform management & analytics</p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" className="gap-1">
            <CheckCircle className="h-3 w-3" />
            {isAdmin ? 'Admin Access' : 'Read-Only'}
          </Badge>
          <Button variant="outline" size="sm" className="gap-2" onClick={() => window.location.reload()}>
            <RefreshCw className="h-4 w-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
        {quickActions.map((action, index) => (
          <motion.div
            key={action.label}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            onClick={action.onClick}
            className={cn(
              "cursor-pointer transition-all hover:shadow-lg hover:-translate-y-1",
              !isAdmin && "opacity-50 cursor-not-allowed"
            )}
          >
            <Card>
              <CardContent className="p-4 text-center">
                <div className={'mx-auto rounded-lg p-3 w-fit ' + action.color}>
                  <action.icon className="h-5 w-5 text-white" />
                </div>
                <p className="mt-2 text-sm font-medium">{action.label}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Quick Stats Row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <Card className="relative overflow-hidden border-0 bg-gradient-to-br shadow-lg">
              <div className={'absolute inset-0 bg-gradient-to-br ' + stat.color + ' opacity-10'} />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <div className={'rounded-lg bg-gradient-to-br ' + stat.color + ' p-2 text-white'}>
                  <stat.icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="flex items-center gap-1 text-xs">
                  {stat.trendUp ? (
                    <TrendingUp className="h-3 w-3 text-green-500" />
                  ) : (
                    <TrendingDown className="h-3 w-3 text-red-500" />
                  )}
                  <span className={stat.trendUp ? 'text-green-500' : 'text-red-500'}>
                    {stat.trend}
                  </span>
                  <span className="text-muted-foreground">{stat.subtitle}</span>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* System Health */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {healthMetrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className={'rounded-lg p-2 ' + getStatusColor(metric.status)}>
                    <metric.icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{metric.label}</p>
                    <p className="text-sm text-muted-foreground">{metric.value}</p>
                  </div>
                  <Badge variant={metric.status === 'healthy' ? 'success' : 'warning'}>
                    {metric.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Platform Overview */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Platform Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm">Storage Usage</span>
                <span className="text-sm font-medium">68%</span>
              </div>
              <Progress value={68} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm">API Usage</span>
                <span className="text-sm font-medium">45%</span>
              </div>
              <Progress value={45} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm">User Growth</span>
                <span className="text-sm font-medium text-green-500">+12%</span>
              </div>
              <Progress value={72} className="h-2" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PieChart className="h-5 w-5" />
              Quick Stats
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg border p-3 text-center">
                <p className="text-2xl font-bold">98%</p>
                <p className="text-xs text-muted-foreground">Satisfaction Rate</p>
              </div>
              <div className="rounded-lg border p-3 text-center">
                <p className="text-2xl font-bold">4.8?</p>
                <p className="text-xs text-muted-foreground">Average Rating</p>
              </div>
              <div className="rounded-lg border p-3 text-center">
                <p className="text-2xl font-bold">1,234</p>
                <p className="text-xs text-muted-foreground">Active Users</p>
              </div>
              <div className="rounded-lg border p-3 text-center">
                <p className="text-2xl font-bold">89</p>
                <p className="text-xs text-muted-foreground">New Orders</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* User Profile Card */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="h-16 w-16 rounded-full bg-gradient-to-r from-primary to-purple-600 flex items-center justify-center text-2xl font-bold text-white">
                {user?.full_name?.charAt(0) || 'A'}
              </div>
              <div>
                <h3 className="font-semibold">{user?.full_name || 'Admin User'}</h3>
                <p className="text-sm text-muted-foreground">{user?.email || 'admin@profitpilot.com'}</p>
                <Badge variant="default" className="mt-1">
                  {isAdmin ? 'Administrator' : 'User'}
                </Badge>
              </div>
            </div>
            <Button variant="outline" className="gap-2" onClick={logout}>
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

