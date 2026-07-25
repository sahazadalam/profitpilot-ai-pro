import React from 'react';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'warning' | 'success' | 'info';
  children?: React.ReactNode;
}

export const Badge = ({ children, variant = 'default', className = '', ...props }: BadgeProps) => {
  const variants = {
    default: 'bg-blue-100 text-blue-800',
    secondary: 'bg-gray-100 text-gray-800',
    destructive: 'bg-red-100 text-red-800',
    outline: 'border border-gray-300 text-gray-700',
    warning: 'bg-yellow-100 text-yellow-800',
    success: 'bg-green-100 text-green-800',
    info: 'bg-cyan-100 text-cyan-800'
  };
  
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${variants[variant] || variants.default} ${className}`} {...props}>
      {children}
    </span>
  );
};

export default Badge;