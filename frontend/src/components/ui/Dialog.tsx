import React, { createContext, useContext } from 'react';

interface DialogContextType {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const DialogContext = createContext<DialogContextType>({ open: false, onOpenChange: () => {} });

interface DialogProps {
  children?: React.ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export const Dialog = ({ children, open = false, onOpenChange = () => {} }: DialogProps) => (
  <DialogContext.Provider value={{ open, onOpenChange }}>
    {children}
  </DialogContext.Provider>
);

export const DialogTrigger = ({ children, onClick, ...props }: any) => {
  const { onOpenChange } = useContext(DialogContext);
  return <div onClick={() => { onOpenChange(true); onClick?.(); }} {...props}>{children}</div>;
};

export const DialogContent = ({ children, className = '', ...props }: any) => {
  const { open, onOpenChange } = useContext(DialogContext);
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className={`bg-white rounded-lg p-6 max-w-lg w-full ${className}`} {...props}>
        {children}
        <button 
          onClick={() => onOpenChange(false)} 
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export const DialogHeader = ({ children, className = '', ...props }: any) => (
  <div className={`mb-4 ${className}`} {...props}>{children}</div>
);

export const DialogTitle = ({ children, className = '', ...props }: any) => (
  <h3 className={`text-lg font-semibold ${className}`} {...props}>{children}</h3>
);

export const DialogDescription = ({ children, className = '', ...props }: any) => (
  <p className={`text-sm text-gray-500 ${className}`} {...props}>{children}</p>
);

export const DialogFooter = ({ children, className = '', ...props }: any) => (
  <div className={`flex justify-end gap-2 mt-4 ${className}`} {...props}>
    {children}
  </div>
);

export default Dialog;