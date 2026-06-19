import apiClient from '@/lib/axios'
import type { ApiResponse, UserPreference } from '@/types'

export const preferencesService = {
  async list(): Promise<UserPreference[]> {
    const { data } = await apiClient.get<ApiResponse<UserPreference[]>>('/users/me/preferences/')
    return data.data
  },

  async set(preferences: Pick<UserPreference, 'category' | 'value' | 'weight'>[]): Promise<UserPreference[]> {
    const { data } = await apiClient.post<ApiResponse<UserPreference[]>>('/users/me/preferences/', preferences)
    return data.data
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`/users/me/preferences/${id}/`)
  },
}
