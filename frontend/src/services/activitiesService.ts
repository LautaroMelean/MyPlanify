import apiClient from '@/lib/axios'
import type { ApiResponse, PaginatedResponse, Activity } from '@/types'

export interface ActivitiesFilters {
  type?: string
  category?: string
  indoor?: boolean
  outdoor?: boolean
  budget?: number
  free?: boolean
  name?: string
}

export const activitiesService = {
  async listPaginated(filters: ActivitiesFilters & { page: number }): Promise<PaginatedResponse<Activity>> {
    const { data } = await apiClient.get<ApiResponse<PaginatedResponse<Activity>>>('/activities/', { params: filters })
    return data.data
  },

  async get(id: string): Promise<Activity> {
    const { data } = await apiClient.get<ApiResponse<Activity>>(`/activities/${id}/`)
    return data.data
  },
}
