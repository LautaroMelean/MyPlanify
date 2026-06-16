import apiClient from '@/lib/axios'
import type { ApiResponse, Place } from '@/types'

interface ExternalPlacesParams {
  lat: number
  lon: number
  radius?: number
  type?: string
}

export const externalPlacesService = {
  async getNearby({ lat, lon, radius = 1500, type = '' }: ExternalPlacesParams): Promise<Place[]> {
    const params: Record<string, unknown> = { lat, lon, radius }
    if (type) params.type = type
    const { data } = await apiClient.get<ApiResponse<Place[]>>('/external/places/', { params })
    return data.data
  },
}
