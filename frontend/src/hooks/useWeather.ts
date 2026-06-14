import { useQuery } from '@tanstack/react-query'
import { weatherService } from '@/services/weatherService'

export function useWeather(coords: { lat: number; lon: number } | null) {
  return useQuery({
    queryKey: ['weather', coords?.lat, coords?.lon],
    queryFn: () => weatherService.getCurrent(coords!.lat, coords!.lon),
    enabled: coords !== null,
    staleTime: 1000 * 60 * 15, // 15 min — matches Redis TTL
    retry: false,
  })
}
