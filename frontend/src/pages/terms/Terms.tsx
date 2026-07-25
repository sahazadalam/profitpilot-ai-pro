import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';

export const Terms = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-3xl">
        <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
          Terms of Service
        </Badge>
        <h1 className="text-4xl font-bold mb-6">Terms of Service</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: July 2026</p>
        
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4">1. Acceptance of Terms</h2>
            <p className="text-muted-foreground">
              By using ProfitPilot AI Pro, you agree to these Terms of Service.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">2. User Accounts</h2>
            <p className="text-muted-foreground">
              You are responsible for maintaining the security of your account and password.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">3. Acceptable Use</h2>
            <p className="text-muted-foreground">
              You agree to use our services only for lawful purposes and in accordance with these terms.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">4. Service Availability</h2>
            <p className="text-muted-foreground">
              We strive to maintain high availability but do not guarantee uninterrupted access.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">5. Contact</h2>
            <p className="text-muted-foreground">
              For any questions about these terms, please contact us at support@profitpilot.com.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

