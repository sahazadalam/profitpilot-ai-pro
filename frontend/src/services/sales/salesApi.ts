import { api } from '../api';

export const salesApi = {
  // Get all sales
  async getSales(search?: string) {
    const response = await api.get('/sales', { params: { search } });
    return response.data;
  },

  // Get single sale
  async getSale(id: string) {
    const response = await api.get(/sales/);
    return response.data;
  },

  // Create sale
  async createSale(data: any) {
    const response = await api.post('/sales', data);
    return response.data;
  },

  // Delete sale
  async deleteSale(id: string) {
    const response = await api.delete(/sales/);
    return response.data;
  },
};
