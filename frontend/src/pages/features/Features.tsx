import { motion } from 'framer-motion';
import { 
  Brain, BarChart3, Shield, Zap, TrendingUp, Users, 
  Database, Cloud, Lock, Globe, PieChart, Smartphone,
  Code, Layers, Target, Briefcase, GraduationCap, Building2,
  LineChart, Settings, UserCircle, Bell, Calendar, FileText
} from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/Button';

export const Features = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI Forecasting',
      description: 'Predict future sales and demand with 95% accuracy using advanced machine learning algorithms.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: BarChart3,
      title: 'Advanced Analytics',
      description: 'Real-time business insights with beautiful charts, trends, and comprehensive performance tracking.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Shield,
      title: 'Risk Management',
      description: 'Identify and mitigate business risks proactively with AI-powered risk assessment and alerts.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Zap,
      title: 'Smart Automation',
      description: 'Intelligent recommendations and automated workflows to optimize your business operations.',
      color: 'from-orange-500 to-amber-500'
    },
    {
      icon: TrendingUp,
      title: 'Growth Insights',
      description: 'Discover growth opportunities with AI-driven insights and actionable recommendations.',
      color: 'from-red-500 to-rose-500'
    },
    {
      icon: Users,
      title: 'Customer Intelligence',
      description: 'Understand your customers better with AI-powered segmentation and behavior analysis.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: Database,
      title: 'Data Integration',
      description: 'Seamlessly connect with your existing data sources and business applications.',
      color: 'from-teal-500 to-cyan-500'
    },
    {
      icon: Cloud,
      title: 'Cloud Native',
      description: 'Fully cloud-native platform with automatic scaling and enterprise-grade reliability.',
      color: 'from-sky-500 to-blue-500'
    },
    {
      icon: Lock,
      title: 'Enterprise Security',
      description: 'Bank-grade security with encryption, authentication, and compliance features.',
      color: 'from-slate-500 to-gray-500'
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
            Features
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Everything you need to grow</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            AI-powered tools to make better business decisions, predict trends, and optimize operations.
          </p>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="group rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1"
            >
              <div className={'mb-4 rounded-lg bg-gradient-to-r ' + feature.color + ' p-3 w-fit group-hover:scale-110 transition-transform'}>
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="mb-2 font-semibold text-lg">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
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
