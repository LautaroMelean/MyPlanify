import apiClient from '@/lib/axios'
import type { ApiResponse, Favorite } from '@/types'

interface AddFavoritePayload {
  event?: string | null
  place?: string | null
  activity?: string | null
}

export const favoritesService = {
  async list(): Promise<Favorite[]> {
    const { data } = await apiClient.get<ApiResponse<Favorite[]>>('/favorites/')
    return data.data
  },

  async add(payload: AddFavoritePayload): Promise<Favorite> {
    const { data } = await apiClient.post<ApiResponse<Favorite>>('/favorites/', payload)
    return data.data
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`/favorites/${id}/`)
  },
}
