import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { AlertCircle, CheckCircle, Info, AlertTriangle, Lightbulb } from 'lucide-react';

interface Insight {
  type: string;
  category: string;
  message: string;
  priority: string;
}

interface InsightsProps {
  data: Insight[];
}

export const Insights = ({ data }: InsightsProps) => {
  const getIcon = (type: string) => {
    switch (type) {
      case 'positive': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'negative': return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case 'critical': return <AlertCircle className="h-5 w-5 text-red-600" />;
      default: return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-l-4 border-red-500';
      case 'medium': return 'border-l-4 border-yellow-500';
      default: return 'border-l-4 border-blue-500';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5" />
          Business Insights
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {!data || data.length === 0 ? (
          <p className="text-sm text-muted-foreground">No insights available</p>
        ) : (
          data.map((insight: Insight, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className={'flex items-start gap-3 rounded-lg bg-muted/50 p-4 ' + getPriorityClass(insight.priority)}
            >
              {getIcon(insight.type)}
              <div>
                <p className="text-sm font-medium">{insight.message}</p>
                <p className="text-xs text-muted-foreground">{insight.category}</p>
              </div>
            </motion.div>
          ))
        )}
      </CardContent>
    </Card>
  );
};
