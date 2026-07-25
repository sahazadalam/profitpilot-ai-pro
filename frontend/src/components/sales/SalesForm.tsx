import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface SalesFormProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const SalesForm = ({ open, onClose, onSuccess }: SalesFormProps) => {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Sale</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label>Product</Label>
            <Input placeholder="Select product" />
          </div>
          <div className="space-y-2">
            <Label>Quantity</Label>
            <Input type="number" placeholder="0" />
          </div>
          <div className="space-y-2">
            <Label>Customer Name</Label>
            <Input placeholder="Customer name" />
          </div>
          <div className="flex justify-end gap-3">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={onSuccess}>
              Create Sale
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

