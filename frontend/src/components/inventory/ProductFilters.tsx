import { Button } from '@/components/ui/Button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/Select';

export const ProductFilters = () => {
  return (
    <div className="flex gap-2">
      <Select>
        <SelectTrigger className="w-[150px]">
          <SelectValue placeholder="Category" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Categories</SelectItem>
          <SelectItem value="electronics">Electronics</SelectItem>
          <SelectItem value="clothing">Clothing</SelectItem>
          <SelectItem value="books">Books</SelectItem>
        </SelectContent>
      </Select>
      <Button variant="outline">Filter</Button>
    </div>
  );
};
