import React, { createContext, useContext, useState } from 'react';

interface TabsContextType {
  value: string;
  onValueChange: (value: string) => void;
}

const TabsContext = createContext<TabsContextType | undefined>(undefined);

interface TabsProps {
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  children?: React.ReactNode;
  className?: string;
}

export const Tabs = ({ defaultValue, value, onValueChange, children, className = '' }: TabsProps) => {
  const [internalValue, setInternalValue] = useState(defaultValue || '');
  const currentValue = value !== undefined ? value : internalValue;
  
  const handleValueChange = (newValue: string) => {
    if (onValueChange) {
      onValueChange(newValue);
    } else {
      setInternalValue(newValue);
    }
  };
  
  return (
    <TabsContext.Provider value={{ value: currentValue, onValueChange: handleValueChange }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
};

export const TabsList = ({ children, className = '' }: { children?: React.ReactNode; className?: string }) => (
  <div className={`inline-flex h-10 items-center justify-center rounded-lg bg-gray-100 p-1 ${className}`}>
    {children}
  </div>
);

interface TabsTriggerProps {
  value: string;
  children?: React.ReactNode;
  className?: string;
}

export const TabsTrigger = ({ value, children, className = '' }: TabsTriggerProps) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsTrigger must be used within Tabs');
  const isActive = context.value === value;
  
  return (
    <button
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1.5 text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
        isActive ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-900'
      } ${className}`}
      onClick={() => context.onValueChange(value)}
    >
      {children}
    </button>
  );
};

export const TabsContent = ({ value, children, className = '' }: { value: string; children?: React.ReactNode; className?: string }) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsContent must be used within Tabs');
  if (context.value !== value) return null;
  
  return <div className={`mt-2 focus-visible:outline-none ${className}`}>{children}</div>;
};

export default Tabs;