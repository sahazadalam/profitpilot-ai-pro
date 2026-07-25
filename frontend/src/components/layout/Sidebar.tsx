import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  TrendingUp, 
  Brain, 
  Lightbulb, 
  BarChart3, 
  MessageSquare, 
  Settings,
  ChevronLeft,
  ChevronRight,
  LogOut,
  User,
  Shield,
  Users,
  Server
} from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/Button';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/dashboard/inventory', icon: Package, label: 'Inventory' },
  { to: '/dashboard/sales', icon: ShoppingCart, label: 'Sales' },
  { to: '/dashboard/analytics', icon: TrendingUp, label: 'Analytics' },
  { to: '/dashboard/prediction', icon: Brain, label: 'Prediction' },
  { to: '/dashboard/recommendations', icon: Lightbulb, label: 'Recommendations' },
  { to: '/dashboard/intelligence', icon: BarChart3, label: 'Intelligence' },
  { to: '/dashboard/chat', icon: MessageSquare, label: 'AI Chat' },
  { to: '/dashboard/reports', icon: BarChart3, label: 'Reports' },
  { to: '/dashboard/profile', icon: User, label: 'Profile' },
  { to: '/dashboard/admin', icon: Shield, label: 'Admin' },
  { to: '/dashboard/settings', icon: Settings, label: 'Settings' },
];

export const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);
  const { logout } = useAuth();

  return (
    <motion.aside
      initial={false}
      animate={{ width: collapsed ? 72 : 240 }}
      className="flex h-full flex-col border-r bg-background"
      transition={{ duration: 0.2 }}
    >
      <div className="flex h-16 items-center justify-between border-b px-4">
        {!collapsed && (
          <span className="text-lg font-bold text-primary">ProfitPilot</span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="rounded-lg p-1 hover:bg-accent"
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      <nav className="flex-1 space-y-1 p-2 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center rounded-lg px-3 py-2 transition-colors hover:bg-accent',
                isActive ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'
              )
            }
          >
            <Icon size={20} className="flex-shrink-0" />
            {!collapsed && <span className="ml-3">{label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="border-t p-4">
        <Button
          variant="ghost"
          className="w-full justify-start gap-2 text-red-500 hover:bg-red-500/10 hover:text-red-600"
          onClick={logout}
        >
          <LogOut size={20} />
          {!collapsed && <span>Logout</span>}
        </Button>
        {!collapsed && (
          <p className="mt-2 text-xs text-muted-foreground">v1.0.0</p>
        )}
      </div>
    </motion.aside>
  );
};

