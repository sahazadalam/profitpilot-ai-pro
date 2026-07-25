export interface User {
  id: string;
  full_name: string;
  email: string;
  role: 'admin' | 'manager' | 'employee' | 'viewer';
  is_active: boolean;
  created_at: string;
  last_login?: string;
  avatar?: string;
  department?: string;
  permissions: string[];
}

export interface Role {
  id: string;
  name: string;
  description: string;
  permissions: string[];
  user_count: number;
  created_at: string;
}

export interface AuditLog {
  id: string;
  user_id: string;
  user_name: string;
  action: string;
  resource: string;
  details: any;
  ip_address: string;
  user_agent: string;
  created_at: string;
}

export interface SystemStatus {
  api: {
    status: 'healthy' | 'degraded' | 'down';
    response_time: number;
    uptime: number;
  };
  database: {
    status: 'healthy' | 'degraded' | 'down';
    connections: number;
    response_time: number;
  };
  server: {
    status: 'healthy' | 'degraded' | 'down';
    memory_usage: number;
    cpu_usage: number;
    storage_usage: number;
  };
  network: {
    status: 'healthy' | 'degraded' | 'down';
    latency: number;
    bandwidth: number;
  };
}

export interface AdminStats {
  users: number;
  products: number;
  sales: number;
  revenue: number;
  active_users: number;
}

