export interface GeneralSettings {
  company_name: string;
  logo: string;
  brand_color: string;
  language: string;
  currency: string;
  timezone: string;
  date_format: string;
  number_format: string;
}

export interface AppearanceSettings {
  theme: 'light' | 'dark' | 'system';
  accent_color: string;
  sidebar_style: 'compact' | 'expanded' | 'floating';
  layout_width: 'full' | 'contained';
  font_size: 'small' | 'medium' | 'large';
  animations: boolean;
}

export interface NotificationSettings {
  email: boolean;
  push: boolean;
  desktop: boolean;
  sms: boolean;
  sound: boolean;
}

export interface ProfileSettings {
  avatar: string;
  name: string;
  email: string;
  phone: string;
  two_factor: boolean;
}

export interface OrganizationSettings {
  name: string;
  industry: string;
  size: string;
  departments: string[];
  branches: string[];
  categories: string[];
}
