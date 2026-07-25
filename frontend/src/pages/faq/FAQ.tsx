import { motion } from 'framer-motion';
import { useState } from 'react';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';
import { ChevronDown, ChevronUp } from 'lucide-react';

export const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs = [
    {
      question: 'What is ProfitPilot AI Pro?',
      answer: 'ProfitPilot AI Pro is an autonomous business intelligence platform that uses AI to help businesses make better decisions, predict trends, and optimize operations.'
    },
    {
      question: 'How does the AI forecasting work?',
      answer: 'Our AI uses advanced machine learning algorithms like Prophet, ARIMA, and deep learning to analyze your business data and generate accurate predictions.'
    },
    {
      question: 'Is my data secure?',
      answer: 'Yes! We use enterprise-grade encryption, secure authentication, and follow industry best practices to protect your data.'
    },
    {
      question: 'Can I try it for free?',
      answer: 'Absolutely! Start with our free demo mode to explore all features without any commitment.'
    },
    {
      question: 'What kind of businesses use ProfitPilot?',
      answer: 'Businesses of all sizes use ProfitPilot - from startups to enterprises across retail, e-commerce, manufacturing, and services.'
    },
    {
      question: 'Do you offer customer support?',
      answer: 'Yes! We offer 24/7 email support, live chat during business hours, and a comprehensive knowledge base.'
    },
    {
      question: 'Can I cancel anytime?',
      answer: 'Yes, you can cancel your subscription at any time with no hidden fees or penalties.'
    },
    {
      question: 'Is there a mobile app?',
      answer: 'Yes, our platform is fully responsive and works on all devices. Mobile apps for iOS and Android are coming soon!'
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
            FAQ
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Frequently asked questions</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Everything you need to know about ProfitPilot AI Pro
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Card 
                className="cursor-pointer transition-all hover:shadow-md"
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">{faq.question}</h3>
                    {openIndex === index ? (
                      <ChevronUp className="h-5 w-5 text-muted-foreground" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-muted-foreground" />
                    )}
                  </div>
                  {openIndex === index && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      transition={{ duration: 0.3 }}
                      className="mt-4 pt-4 border-t"
                    >
                      <p className="text-muted-foreground">{faq.answer}</p>
                    </motion.div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
