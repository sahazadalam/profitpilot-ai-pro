import { Card, CardContent } from '@/components/ui/Card';
import { Label } from '@/components/ui/Label';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';

export const PredictionFilters = ({ filters, setFilters }: any) => {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          <div>
            <Label className="text-xs">Days</Label>
            <Input
              type="number"
              value={filters.days}
              onChange={(e) => setFilters({ ...filters, days: parseInt(e.target.value) || 30 })}
              className="w-20 h-8"
              min={7}
              max={365}
            />
          </div>
          <div>
            <Label className="text-xs">Model</Label>
            <Select
              value={filters.model}
              onValueChange={(value) => setFilters({ ...filters, model: value })}
            >
              <SelectTrigger className="w-32 h-8">
                <SelectValue placeholder="Model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="prophet">Prophet</SelectItem>
                <SelectItem value="arima">ARIMA</SelectItem>
                <SelectItem value="linear">Linear</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button size="sm" className="mt-4">Apply</Button>
        </div>
      </CardContent>
    </Card>
  );
};

