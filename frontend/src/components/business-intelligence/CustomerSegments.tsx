export const CustomerSegments = ({ data }: any) => {
  return (
    <Card>
      <CardHeader><CardTitle>Customer Segments</CardTitle></CardHeader>
      <CardContent>
        {data?.length === 0 ? (
          <p className='text-sm text-muted-foreground'>No customer segments</p>
        ) : (
          <div className='space-y-3'>
            {data?.map((segment: any, i: number) => (
              <div key={i} className='flex items-center justify-between border-b pb-2'>
                <span>{segment.segment_name}</span>
                <span className='font-medium'>{segment.customer_count} customers</span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

