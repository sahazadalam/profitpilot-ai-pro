import { api } from '@/services/api';

export const salesApi = {
  async getSales(params: any = {}) {
    const response = await api.get('/sales', { params });
    return response.data;
  },

  async getSale(id: string) {
    const response = await api.get(`/sales`);
    return response.data;
  },

  async createSale(data: any) {
    const response = await api.post('/sales', data);
    return response.data;
  },

  async deleteSale(id: string) {
    const response = await api.delete(`/sales`);
    return response.data;
  },
};

