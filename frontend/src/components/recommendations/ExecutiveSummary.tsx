import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import { FileText } from 'lucide-react';

export const ExecutiveSummary = ({ data }: any) => {
  const summary = data || {};

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          Executive Summary
        </CardTitle>
      </CardHeader>
      <CardContent>
        {summary.summary ? (
          <div className="space-y-4">
            <div className="rounded-lg bg-muted/50 p-4">
              <p className="text-sm whitespace-pre-wrap">{summary.summary}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg border p-3">
                <p className="text-xs text-muted-foreground">Total Recommendations</p>
                <p className="text-lg font-bold">{summary.total_recommendations || 0}</p>
              </div>
              <div className="rounded-lg border p-3">
                <p className="text-xs text-muted-foreground">Business Risk</p>
                <p className="text-lg font-bold">{summary.business_risk || 'Unknown'}</p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">No executive summary available</p>
        )}
      </CardContent>
    </Card>
  );
};
