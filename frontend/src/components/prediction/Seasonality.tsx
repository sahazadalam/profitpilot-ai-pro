import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export const Seasonality = ({ data }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Seasonality Detection</CardTitle>
      </CardHeader>
      <CardContent>
        {!data ? (
          <p className="text-sm text-muted-foreground">No seasonality data</p>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Seasonality Detected</span>
              <Badge variant={data.has_seasonality ? 'default' : 'secondary'}>
                {data.has_seasonality ? 'Yes' : 'No'}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Seasonality Strength</span>
              <span className="text-sm font-medium">
                {(data.seasonality_strength * 100).toFixed(1)}%
              </span>
            </div>
            {data.peak_days && data.peak_days.length > 0 && (
              <div>
                <p className="text-sm text-muted-foreground">Peak Days</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {data.peak_days.map((day: string) => (
                    <Badge key={day} variant="default">{day}</Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

