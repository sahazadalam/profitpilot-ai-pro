import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Shield } from 'lucide-react';

interface BusinessRiskProps {
  data: {
    risk_score?: number;
    risk_level?: string;
  };
}

export const BusinessRisk = ({ data }: BusinessRiskProps) => {
  const risk = data || {};
  const score = risk.risk_score || 0;
  const level = risk.risk_level || 'Unknown';

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'Low Risk': return 'bg-green-500';
      case 'Medium Risk': return 'bg-yellow-500';
      case 'High Risk': return 'bg-orange-500';
      case 'Critical Risk': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          Business Risk
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold">{score}</p>
            <p className="text-sm text-muted-foreground">Risk Score</p>
          </div>
          <div className={'rounded-lg px-4 py-2 text-white ' + getRiskColor(level)}>
            {level}
          </div>
        </div>
        {risk.description && (
          <p className="mt-4 text-sm text-muted-foreground">{risk.description}</p>
        )}
      </CardContent>
    </Card>
  );
};
