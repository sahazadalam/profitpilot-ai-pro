import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

export const Card = ({ children, className = '', ...props }: CardProps) => (
  <div className={`rounded-lg border border-gray-200 bg-white shadow-sm ${className}`} {...props}>
    {children}
  </div>
);

export const CardHeader = ({ children, className = '', ...props }: CardProps) => (
  <div className={`flex flex-col space-y-1.5 p-6 ${className}`} {...props}>
    {children}
  </div>
);

export const CardTitle = ({ children, className = '', ...props }: CardProps) => (
  <h3 className={`text-2xl font-semibold leading-none tracking-tight text-gray-900 ${className}`} {...props}>
    {children}
  </h3>
);

export const CardDescription = ({ children, className = '', ...props }: CardProps) => (
  <p className={`text-sm text-gray-500 ${className}`} {...props}>
    {children}
  </p>
);

export const CardContent = ({ children, className = '', ...props }: CardProps) => (
  <div className={`p-6 pt-0 ${className}`} {...props}>
    {children}
  </div>
);

export const CardFooter = ({ children, className = '', ...props }: CardProps) => (
  <div className={`flex items-center p-6 pt-0 ${className}`} {...props}>
    {children}
  </div>
);

export default Card;