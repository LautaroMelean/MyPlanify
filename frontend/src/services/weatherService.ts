import apiClient from '@/lib/axios'
import type { ApiResponse, Weather } from '@/types'

export const weatherService = {
  async getCurrent(lat: number, lon: number): Promise<Weather | null> {
    const { data } = await apiClient.get<ApiResponse<Weather | null>>('/weather/current/', {
      params: { lat, lon },
    })
    return data.data
  },
}
