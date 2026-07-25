import { useQuery } from '@tanstack/react-query';
import { adminService } from '@/services/admin';

export const useAdmin = () => {
  const stats = useQuery({
    queryKey: ['admin', 'stats'],
    queryFn: adminService.getStats,
    staleTime: 5 * 60 * 1000,
  });

  const users = useQuery({
    queryKey: ['admin', 'users'],
    queryFn: adminService.getUsers,
    staleTime: 5 * 60 * 1000,
  });

  const roles = useQuery({
    queryKey: ['admin', 'roles'],
    queryFn: adminService.getRoles,
    staleTime: 5 * 60 * 1000,
  });

  const auditLogs = useQuery({
    queryKey: ['admin', 'audit-logs'],
    queryFn: adminService.getAuditLogs,
    staleTime: 5 * 60 * 1000,
  });

  const systemStatus = useQuery({
    queryKey: ['admin', 'system-status'],
    queryFn: adminService.getSystemStatus,
    staleTime: 1 * 60 * 1000,
  });

  return {
    stats: stats.data,
    users: users.data,
    roles: roles.data,
    auditLogs: auditLogs.data,
    systemStatus: systemStatus.data,
    isLoading: stats.isLoading || users.isLoading,
    error: stats.error || users.error,
  };
};

