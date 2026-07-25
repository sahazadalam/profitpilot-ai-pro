import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

interface ModelComparisonProps {
  models: {
    best_model?: string;
    models?: Record<string, any>;
  };
}

export const ModelComparison = ({ models }: ModelComparisonProps) => {
  const bestModel = models?.best_model || 'No comparison data';
  const modelList = models?.models || {};

  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Comparison</CardTitle>
      </CardHeader>
      <CardContent>
        {bestModel !== 'No comparison data' ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Best Model</span>
              <Badge variant="default">{bestModel}</Badge>
            </div>
            {Object.entries(modelList).map(([name, metrics]: [string, any]) => (
              <div key={name} className="rounded-lg border p-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{name}</span>
                  <span className="text-sm text-muted-foreground">
                    R²: {metrics.r2?.toFixed(3) || 'N/A'}
                  </span>
                </div>
                <div className="mt-1 grid grid-cols-3 gap-2 text-xs text-muted-foreground">
                  <span>MAE: {metrics.mae?.toFixed(2) || 'N/A'}</span>
                  <span>RMSE: {metrics.rmse?.toFixed(2) || 'N/A'}</span>
                  <span>MAPE: {metrics.mape?.toFixed(2) || 'N/A'}%</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">{bestModel}</p>
        )}
      </CardContent>
    </Card>
  );
};

