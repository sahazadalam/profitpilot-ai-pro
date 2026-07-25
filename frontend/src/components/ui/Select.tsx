import React, { createContext, useContext } from 'react';

interface SelectContextType {
  value: string;
  onValueChange: (value: string) => void;
}

const SelectContext = createContext<SelectContextType>({ value: '', onValueChange: () => {} });

interface SelectProps {
  children?: React.ReactNode;
  value?: string;
  onValueChange?: (value: string) => void;
}

export const Select = ({ children, value = '', onValueChange = () => {} }: SelectProps) => (
  <SelectContext.Provider value={{ value, onValueChange }}>
    <div className="relative">{children}</div>
  </SelectContext.Provider>
);

export const SelectTrigger = ({ children, className = '', ...props }: any) => (
  <button className={`flex h-10 w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ${className}`} {...props}>
    {children}
  </button>
);

export const SelectValue = ({ placeholder, className = '', ...props }: any) => {
  const { value } = useContext(SelectContext);
  return <span className={className}>{value || placeholder}</span>;
};

export const SelectContent = ({ children, className = '', ...props }: any) => (
  <div className={`absolute z-50 mt-1 w-full rounded-md border border-gray-200 bg-white shadow-lg ${className}`} {...props}>
    {children}
  </div>
);

export const SelectItem = ({ value, children, className = '', ...props }: any) => {
  const { onValueChange } = useContext(SelectContext);
  return (
    <div className={`px-3 py-2 hover:bg-gray-100 cursor-pointer ${className}`} onClick={() => onValueChange(value)} {...props}>
      {children}
    </div>
  );
};

export default Select;