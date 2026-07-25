import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from '@/components/layout/Layout';
import { Login } from '@/pages/auth/Login';
import { Register } from '@/pages/auth/Register';
import { ForgotPassword } from '@/pages/auth/ForgotPassword';
import { Profile } from '@/pages/auth/Profile';
import { Dashboard } from '@/pages/dashboard/Dashboard';
import { Inventory } from '@/pages/inventory/Inventory';
import { Sales } from '@/pages/sales/Sales';
import { AnalyticsDashboard } from '@/pages/analytics/AnalyticsDashboard';
import { PredictionDashboard } from '@/pages/prediction/PredictionDashboard';
import { RecommendationsDashboard } from '@/pages/recommendations/RecommendationsDashboard';
import { BusinessIntelligenceDashboard } from '@/pages/business-intelligence/BusinessIntelligenceDashboard';
import { AIChat } from '@/pages/ai-chat/AIChat';
import { ReportsDashboard } from '@/pages/reports/ReportsDashboard';
import { AdminDashboard } from '@/pages/admin/AdminDashboard';
import { UserManagement } from '@/pages/admin/UserManagement';
import { RoleManagement } from '@/pages/admin/RoleManagement';
import { SecurityCenter } from '@/pages/security/SecurityCenter';
import { AuditLogs } from '@/pages/audit-logs/AuditLogs';
import { SystemStatus } from '@/pages/system-status/SystemStatus';
import { SettingsPage } from '@/pages/settings/SettingsPage';
import { Landing } from '@/pages/landing/Landing';
import { Features } from '@/pages/features/Features';
import { HowItWorks } from '@/pages/how-it-works/HowItWorks';
import { Testimonials } from '@/pages/testimonials/Testimonials';
import { FAQ } from '@/pages/faq/FAQ';
import { Pricing } from '@/pages/pricing/Pricing';
import { About } from '@/pages/about/About';
import { Contact } from '@/pages/contact/Contact';
import { Privacy } from '@/pages/privacy/Privacy';
import { Terms } from '@/pages/terms/Terms';
import { Security } from '@/pages/security/Security';
import { Cookies } from '@/pages/cookies/Cookies';
import { ROUTES } from '@/constants/routes';
import { useAuth } from '@/contexts/AuthContext';
import { LoadingScreen } from '@/components/common/LoadingScreen';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading, isDemoMode } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated && !isDemoMode) {
    return <Navigate to={ROUTES.LOGIN} replace />;
  }

  return <>{children}</>;
};

const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'Admin' || user?.email === 'sahzadalam114@gmail.com';
  
  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }
  return <>{children}</>;
};

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path={ROUTES.HOME} element={<Landing />} />
      <Route path="/features" element={<Features />} />
      <Route path="/how-it-works" element={<HowItWorks />} />
      <Route path="/testimonials" element={<Testimonials />} />
      <Route path="/faq" element={<FAQ />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/terms" element={<Terms />} />
      <Route path="/security" element={<Security />} />
      <Route path="/cookies" element={<Cookies />} />
      <Route path={ROUTES.LOGIN} element={<Login />} />
      <Route path={ROUTES.REGISTER} element={<Register />} />
      <Route path={ROUTES.FORGOT_PASSWORD} element={<ForgotPassword />} />
      
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="inventory" element={<Inventory />} />
        <Route path="sales" element={<Sales />} />
        <Route path="analytics" element={<AnalyticsDashboard />} />
        <Route path="prediction" element={<PredictionDashboard />} />
        <Route path="recommendations" element={<RecommendationsDashboard />} />
        <Route path="intelligence" element={<BusinessIntelligenceDashboard />} />
        <Route path="chat" element={<AIChat />} />
        <Route path="reports" element={<ReportsDashboard />} />
        <Route path="profile" element={<Profile />} />
        <Route path="settings" element={<SettingsPage />} />
        
        {/* Admin Routes */}
        <Route path="admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
        <Route path="admin/users" element={<AdminRoute><UserManagement /></AdminRoute>} />
        <Route path="admin/roles" element={<AdminRoute><RoleManagement /></AdminRoute>} />
        <Route path="admin/security" element={<AdminRoute><SecurityCenter /></AdminRoute>} />
        <Route path="admin/audit-logs" element={<AdminRoute><AuditLogs /></AdminRoute>} />
        <Route path="admin/system-status" element={<AdminRoute><SystemStatus /></AdminRoute>} />
      </Route>
      
      <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
    </Routes>
  );
};
