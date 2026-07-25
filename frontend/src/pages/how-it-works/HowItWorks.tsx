import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  Database, Brain, TrendingUp, Users, Zap, Shield,
  BarChart3, Clock, CheckCircle, ArrowRight
} from 'lucide-react';

export const HowItWorks = () => {
  const steps = [
    {
      icon: Database,
      title: 'Connect Your Data',
      description: 'Integrate with your existing business data sources effortlessly.',
      details: 'Connect your sales, inventory, and customer data in minutes.'
    },
    {
      icon: Brain,
      title: 'AI Analysis',
      description: 'Our AI analyzes your data and generates actionable insights.',
      details: 'Advanced algorithms identify patterns, trends, and opportunities.'
    },
    {
      icon: TrendingUp,
      title: 'Make Decisions',
      description: 'Use AI-powered recommendations to make better business decisions.',
      details: 'Get personalized recommendations and predictive insights.'
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
            How It Works
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Simple, powerful, effective</h1>
          <p className="text-muted-foreground">
            Get started in minutes with our intuitive platform
          </p>
        </div>

        <div className="space-y-12">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex flex-col md:flex-row gap-6 items-center"
            >
              <div className="flex-shrink-0">
                <div className="flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-r from-primary to-purple-600">
                  <step.icon className="h-10 w-10 text-white" />
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl font-bold mb-2">{step.title}</h3>
                <p className="text-lg text-muted-foreground">{step.description}</p>
                <p className="text-sm text-muted-foreground mt-2">{step.details}</p>
              </div>
              <div className="flex-shrink-0">
                <Badge variant="outline" className="text-lg px-4 py-2">
                  Step {index + 1}
                </Badge>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <Link to="/register">
            <Button size="lg" className="bg-gradient-to-r from-primary to-purple-600">
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};

