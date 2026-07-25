import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

export const ProductForm = ({ initialData, onSubmit, isLoading }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Product Form</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={(e) => { e.preventDefault(); onSubmit({}); }}>
          <div className="space-y-4">
            <div>
              <label>Name</label>
              <input type="text" className="border p-2 w-full" />
            </div>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Saving...' : 'Save'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

