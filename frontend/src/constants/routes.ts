export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  DASHBOARD: '/dashboard',
  INVENTORY: '/dashboard/inventory',
  SALES: '/dashboard/sales',
  ANALYTICS: '/dashboard/analytics',
  PREDICTION: '/dashboard/prediction',
  RECOMMENDATIONS: '/dashboard/recommendations',
  INTELLIGENCE: '/dashboard/intelligence',
  CHAT: '/dashboard/chat',
  PROFILE: '/dashboard/profile',
  SETTINGS: '/dashboard/settings',
} as const

export const PROTECTED_ROUTES = [
  ROUTES.DASHBOARD,
  ROUTES.INVENTORY,
  ROUTES.SALES,
  ROUTES.ANALYTICS,
  ROUTES.PREDICTION,
  ROUTES.RECOMMENDATIONS,
  ROUTES.INTELLIGENCE,
  ROUTES.CHAT,
  ROUTES.PROFILE,
  ROUTES.SETTINGS,
]

