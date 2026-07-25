import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';

interface BusinessHealthProps {
  data: {
    score: number;
    status: string;
    explanation?: string;
  };
}

export const BusinessHealth = ({ data }: BusinessHealthProps) => {
  const score = data?.score || 0;
  const status = data?.status || 'Unknown';

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Excellent': return 'text-green-500';
      case 'Good': return 'text-yellow-500';
      case 'Average': return 'text-orange-500';
      case 'Poor': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const statusColor = getStatusColor(status);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Business Health
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-5xl font-bold">{score}</div>
            <div className={'text-lg font-medium ' + statusColor}>{status}</div>
            <div className="mt-4 h-2 w-full rounded-full bg-secondary">
              <div
                className="h-2 rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500"
                style={{ width: score + '%' }}
              />
            </div>
            {data?.explanation && (
              <p className="mt-4 text-sm text-muted-foreground">{data.explanation}</p>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

