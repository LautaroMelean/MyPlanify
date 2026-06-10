import apiClient from '@/lib/axios'
import type { ApiResponse, Notification } from '@/types'

export const notificationsService = {
  async list(): Promise<Notification[]> {
    const { data } = await apiClient.get<ApiResponse<Notification[]>>('/notifications/')
    return data.data
  },

  async markRead(id: string): Promise<Notification> {
    const { data } = await apiClient.patch<ApiResponse<Notification>>(`/notifications/${id}/read/`)
    return data.data
  },
}
