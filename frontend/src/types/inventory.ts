export interface Product {
  id: string;
  name: string;
  sku: string;
  category: string;
  price: number;
  stock: number;
  description?: string;
  supplier?: string;
  purchase_price?: number;
  selling_price?: number;
  minimum_stock?: number;
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ProductFormData {
  name: string;
  sku: string;
  category: string;
  price: number;
  stock: number;
  description?: string;
  supplier?: string;
  purchase_price?: number;
  selling_price?: number;
  minimum_stock?: number;
  status?: string;
}
