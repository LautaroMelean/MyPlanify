import apiClient from '@/lib/axios'
import type { ApiResponse, Promotion } from '@/types'

interface PromotionsFilters {
  place?: string
}

export const promotionsService = {
  async list(filters: PromotionsFilters = {}): Promise<Promotion[]> {
    const { data } = await apiClient.get<ApiResponse<Promotion[]>>('/promotions/', { params: filters })
    return data.data
  },

}
