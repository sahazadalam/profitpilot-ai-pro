import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';

export const Privacy = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-3xl">
        <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
          Privacy Policy
        </Badge>
        <h1 className="text-4xl font-bold mb-6">Privacy Policy</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: July 2026</p>
        
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4">1. Information We Collect</h2>
            <p className="text-muted-foreground">
              We collect information you provide directly, such as your name, email address, and payment information.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">2. How We Use Your Information</h2>
            <p className="text-muted-foreground">
              We use your information to provide, maintain, and improve our services.
            </p>
          </div>
          <div>
            <h2 className="text-2xl font-semibold mb-4">3. Data Security</h2>
            <p className="text-muted-foreground">
              We implement appropriate technical and organizational measures to protect your data.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

