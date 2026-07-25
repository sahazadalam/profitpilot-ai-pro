import React from 'react';

interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

export const Avatar = ({ children, className = '', ...props }: AvatarProps) => (
  <div className={`relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full ${className}`} {...props}>
    {children}
  </div>
);

export const AvatarImage = ({ src, alt = '', className = '', ...props }: any) => (
  <img src={src} alt={alt} className={`aspect-square h-full w-full ${className}`} {...props} />
);

export const AvatarFallback = ({ children, className = '', ...props }: any) => (
  <div className={`flex h-full w-full items-center justify-center rounded-full bg-gray-100 text-gray-600 ${className}`} {...props}>
    {children}
  </div>
);

export default Avatar;