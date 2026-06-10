import apiClient from '@/lib/axios'
import type { ApiResponse, Recommendation } from '@/types'

export interface RecommendationFilters {
  lat?: number
  lon?: number
  budget?: number
  people?: number
}

export const recommendationsService = {
  async list(filters: RecommendationFilters = {}): Promise<Recommendation[]> {
    const { data } = await apiClient.get<ApiResponse<Recommendation[]>>('/recommendations/', { params: filters })
    return data.data
  },
}
