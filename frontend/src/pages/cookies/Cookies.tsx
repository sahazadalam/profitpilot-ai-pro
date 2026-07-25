import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';

export const Cookies = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-3xl">
        <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
          Cookie Policy
        </Badge>
        <h1 className="text-4xl font-bold mb-6">Cookie Policy</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: July 2026</p>
        
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4">1. What Are Cookies</h2>
            <p className="text-muted-foreground">
              Cookies are small text files stored on your device that help us improve your experience.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">2. How We Use Cookies</h2>
            <p className="text-muted-foreground">
              We use cookies to analyze usage, personalize content, and improve our services.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">3. Managing Cookies</h2>
            <p className="text-muted-foreground">
              You can manage or disable cookies in your browser settings.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
