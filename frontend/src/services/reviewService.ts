import apiClient from '@/lib/axios'
import type { ApiResponse, ReviewsResponse, Review, ReviewEntityType } from '@/types'

export const reviewService = {
  async getForEntity(entityType: ReviewEntityType, entityId: string): Promise<ReviewsResponse> {
    const { data } = await apiClient.get<ApiResponse<ReviewsResponse>>(
      `/reviews/${entityType}/${entityId}/`,
    )
    return data.data
  },

  async create(params: {
    entity_type: ReviewEntityType
    entity_id: string
    stars: number
    text: string
  }): Promise<Review> {
    const { data } = await apiClient.post<ApiResponse<Review>>('/reviews/', params)
    return data.data
  },

  async delete(entityType: ReviewEntityType, entityId: string): Promise<void> {
    await apiClient.delete(`/reviews/${entityType}/${entityId}/delete/`)
  },
}
