import apiClient from '@/lib/axios'
import type { ApiResponse, PaginatedResponse, Place } from '@/types'

export interface PlacesFilters {
  city?: string
  category?: string
  name?: string
  lat?: number
  lon?: number
  radius_km?: number
  outdoor_seating?: boolean
  fee?: boolean
  wheelchair?: string
  cuisine?: string
  open_now?: boolean
}

export const placesService = {
  async list(filters: PlacesFilters = {}): Promise<Place[]> {
    const { data } = await apiClient.get<ApiResponse<Place[]>>('/places/', { params: filters })
    return data.data
  },

  async listPaginated(filters: PlacesFilters & { page: number }): Promise<PaginatedResponse<Place>> {
    const { data } = await apiClient.get<ApiResponse<PaginatedResponse<Place>>>('/places/', { params: filters })
    return data.data
  },

  async get(id: string): Promise<Place> {
    const { data } = await apiClient.get<ApiResponse<Place>>(`/places/${id}/`)
    return data.data
  },
}
