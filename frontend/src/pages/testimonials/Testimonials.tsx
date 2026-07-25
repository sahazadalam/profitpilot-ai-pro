import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';

export const Testimonials = () => {
  const testimonials = [
    {
      name: 'Sarah Johnson',
      role: 'CEO, TechCorp',
      content: 'ProfitPilot AI Pro has transformed how we make business decisions. The AI predictions are incredibly accurate.',
      avatar: 'SJ',
      rating: 5,
      company: 'TechCorp'
    },
    {
      name: 'Michael Chen',
      role: 'CTO, DataFlow',
      content: 'The analytics and forecasting capabilities have given us a competitive edge in the market.',
      avatar: 'MC',
      rating: 5,
      company: 'DataFlow'
    },
    {
      name: 'Emily Rodriguez',
      role: 'Product Manager, InnovateHub',
      content: 'Best business intelligence tool we have ever used. The dashboard is beautiful and intuitive.',
      avatar: 'ER',
      rating: 5,
      company: 'InnovateHub'
    },
    {
      name: 'David Kim',
      role: 'Operations Director, GlobalTech',
      content: 'The inventory management and sales analytics have saved us countless hours and improved our bottom line.',
      avatar: 'DK',
      rating: 5,
      company: 'GlobalTech'
    },
    {
      name: 'Lisa Thompson',
      role: 'CEO, CloudMasters',
      content: 'Incredible platform! The AI insights are spot on and the recommendations are always valuable.',
      avatar: 'LT',
      rating: 5,
      company: 'CloudMasters'
    },
    {
      name: 'James Wilson',
      role: 'VP of Sales, GrowthInc',
      content: 'Our sales team uses ProfitPilot daily. The revenue predictions and customer insights are game-changers.',
      avatar: 'JW',
      rating: 5,
      company: 'GrowthInc'
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
            Testimonials
          </Badge>
          <h1 className="text-4xl font-bold mb-4">What our customers say</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Join thousands of businesses already using ProfitPilot AI Pro
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
            >
              <Card className="h-full transition-all hover:shadow-lg">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-primary to-purple-600 text-white font-semibold">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <h4 className="font-semibold">{testimonial.name}</h4>
                      <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">"{testimonial.content}"</p>
                  <div className="mt-4 flex text-yellow-500">
                    {'?'.repeat(testimonial.rating)}
                  </div>
                  <div className="mt-2 text-xs text-muted-foreground">
                    {testimonial.company}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};

