import apiClient from '@/lib/axios'
import type { ApiResponse } from '@/types'

export interface GeocodingResult {
  lat: number
  lon: number
  display_name: string
  city: string
  country: string
  country_code: string
}

export const geocodingService = {
  async geocode(query: string): Promise<GeocodingResult | null> {
    try {
      const { data } = await apiClient.get<ApiResponse<GeocodingResult>>('/geocode/', {
        params: { q: query },
      })
      return data.data
    } catch {
      return null
    }
  },

}
