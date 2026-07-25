import { api } from '@/services/api';

export const inventoryApi = {
  async getProducts(params: any = {}) {
    const response = await api.get('/products', { params });
    return response.data;
  },

  async getProduct(id: string) {
    const response = await api.get(`/products`);
    return response.data;
  },

  async createProduct(data: any) {
    const response = await api.post('/products', data);
    return response.data;
  },

  async updateProduct(id: string, data: any) {
    const response = await api.put(`/products`,   data);
    return response.data;
  },

  async deleteProduct(id: string) {
    const response = await api.delete(`/products`);
    return response.data;
  },

  async getSummary() {
    const response = await api.get('/products/summary');
    return response.data;
  },
};

