import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Link } from 'react-router-dom';
import { CheckCircle } from 'lucide-react';

export const Pricing = () => {
  const plans = [
    {
      name: 'Free',
      price: '',
      description: 'Perfect for getting started',
      features: [
        'Up to 100 transactions',
        'Basic analytics',
        'Community support',
        '30-day data retention'
      ],
      cta: 'Get Started',
      popular: false
    },
    {
      name: 'Pro',
      price: '',
      description: 'For growing businesses',
      features: [
        'Unlimited transactions',
        'Advanced analytics',
        'Priority support',
        '1-year data retention',
        'AI predictions',
        'Custom reports'
      ],
      cta: 'Start Free Trial',
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      description: 'For large organizations',
      features: [
        'Everything in Pro',
        'Dedicated support',
        'Unlimited data retention',
        'Custom integrations',
        'SLA guarantee',
        'On-premise deployment'
      ],
      cta: 'Contact Sales',
      popular: false
    }
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
            Pricing
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Choose the right plan</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Start free and upgrade as you grow. No hidden fees.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className={'rounded-xl border p-6 shadow-sm transition-all hover:shadow-lg ' + (plan.popular ? 'border-primary shadow-lg' : '')}
            >
              {plan.popular && (
                <Badge className="mb-4 bg-gradient-to-r from-primary to-purple-600">Most Popular</Badge>
              )}
              <h3 className="text-2xl font-bold">{plan.name}</h3>
              <div className="mt-2">
                <span className="text-4xl font-bold">{plan.price}</span>
                {plan.price !== 'Custom' && <span className="text-muted-foreground">/month</span>}
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{plan.description}</p>
              <ul className="mt-6 space-y-2">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    {feature}
                  </li>
                ))}
              </ul>
              <Link to={plan.name === 'Enterprise' ? '/contact' : '/register'}>
                <Button className={'mt-6 w-full ' + (plan.popular ? 'bg-gradient-to-r from-primary to-purple-600' : '')}>
                  {plan.cta}
                </Button>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
