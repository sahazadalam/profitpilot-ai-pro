import { api } from '../api';

export const inventoryApi = {
  // Get all products
  async getProducts(search?: string) {
    const response = await api.get('/products', { params: { search } });
    return response.data;
  },

  // Get single product
  async getProduct(id: string) {
    const response = await api.get(/products/);
    return response.data;
  },

  // Create product
  async createProduct(data: any) {
    const response = await api.post('/products', data);
    return response.data;
  },

  // Update product
  async updateProduct(id: string, data: any) {
    const response = await api.put(/products/, data);
    return response.data;
  },

  // Delete product
  async deleteProduct(id: string) {
    const response = await api.delete(/products/);
    return response.data;
  },

  // Get summary
  async getSummary() {
    const response = await api.get('/products/summary');
    return response.data;
  },
};
