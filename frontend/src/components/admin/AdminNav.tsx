import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Users, Shield, Server, 
  Bell, Settings, Activity, Key, UserCog,
  FileText, BarChart3, Lock, Eye, AlertCircle
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const adminNavItems = [
  { to: '/dashboard/admin', icon: LayoutDashboard, label: 'Overview' },
  { to: '/dashboard/admin/users', icon: Users, label: 'Users' },
  { to: '/dashboard/admin/roles', icon: UserCog, label: 'Roles' },
  { to: '/dashboard/admin/security', icon: Shield, label: 'Security' },
  { to: '/dashboard/admin/audit-logs', icon: Activity, label: 'Audit Logs' },
  { to: '/dashboard/admin/system-status', icon: Server, label: 'System Status' },
  { to: '/dashboard/notifications', icon: Bell, label: 'Notifications' },
  { to: '/dashboard/settings', icon: Settings, label: 'Settings' },
];

export const AdminNav = () => {
  return (
    <motion.nav
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-1"
    >
      {adminNavItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent',
              isActive ? 'bg-accent text-accent-foreground font-medium' : 'text-muted-foreground'
            )
          }
        >
          <item.icon className="h-4 w-4" />
          <span>{item.label}</span>
        </NavLink>
      ))}
    </motion.nav>
  );
};
