import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';
import { Shield, Lock, Server, Database, CheckCircle } from 'lucide-react';

export const Security = () => {
  const features = [
    {
      icon: Shield,
      title: 'Data Encryption',
      description: 'All data is encrypted at rest and in transit using industry-standard encryption.'
    },
    {
      icon: Lock,
      title: 'Access Control',
      description: 'Role-based access control ensures only authorized users can access sensitive data.'
    },
    {
      icon: Server,
      title: 'Secure Infrastructure',
      description: 'Our infrastructure is hosted on secure, SOC2-compliant cloud providers.'
    },
    {
      icon: Database,
      title: 'Data Privacy',
      description: 'We never share your data with third parties without your explicit consent.'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-4xl">
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
            Security
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Security at ProfitPilot</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            We take security seriously. Here's how we protect your data.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-lg"
            >
              <div className="mb-4 rounded-lg bg-primary/10 p-3 w-fit">
                <feature.icon className="h-6 w-6 text-primary" />
              </div>
              <h3 className="mb-2 font-semibold">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <div className="mt-12 rounded-xl bg-primary/5 border p-6 text-center">
          <div className="flex items-center justify-center gap-2 text-green-500">
            <CheckCircle className="h-5 w-5" />
            <span className="font-medium">Your data is safe with us</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
