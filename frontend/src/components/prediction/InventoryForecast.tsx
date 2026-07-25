import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export const InventoryForecast = ({ data }: any) => {
  const items = data?.data || [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Inventory Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <p className="text-sm text-muted-foreground">No inventory forecast data</p>
        ) : (
          <div className="space-y-3">
            {items.slice(0, 3).map((item: any, index: number) => (
              <div key={index} className="flex items-center justify-between rounded-lg border p-3">
                <div>
                  <p className="font-medium">{item.product_name}</p>
                  <p className="text-xs text-muted-foreground">Stock: {item.current_stock}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">{item.days_until_depletion} days</p>
                  <Badge variant={item.days_until_depletion < 7 ? 'destructive' : 'default'}>
                    {item.days_until_depletion < 7 ? 'Urgent' : 'Ok'}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

