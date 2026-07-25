import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { usePrediction } from '@/hooks/prediction/usePrediction';
import { useState } from 'react';

export const ProfitForecast = () => {
  const [days, setDays] = useState(30);
  const { profit } = usePrediction();

  const handlePredict = () => {
    profit.mutate({ days });
  };

  const forecastData = profit.data?.forecast || [];

  return (
    <Card>
      <CardContent className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">Profit Forecast</h3>
          <div className="flex items-center gap-2">
            <Input
              type="number"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value) || 30)}
              className="w-20 h-8"
              min={7}
              max={365}
            />
            <Button size="sm" onClick={handlePredict} disabled={profit.isPending}>
              {profit.isPending ? 'Loading...' : 'Predict'}
            </Button>
          </div>
        </div>
        <div className="h-48">
          {forecastData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="date" className="text-xs" tick={{ fontSize: 10 }} />
                <YAxis className="text-xs" />
                <Tooltip
                  contentStyle={{
                    background: 'var(--background)',
                    border: '1px solid var(--border)',
                    borderRadius: '8px',
                  }}
                  formatter={(value) => ['$' + value, 'Profit']}
                />
                <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Click "Predict" to see forecast
            </div>
          )}
        </div>
        {profit.data?.explanation && (
          <p className="text-xs text-muted-foreground">{profit.data.explanation}</p>
        )}
      </CardContent>
    </Card>
  );
};

