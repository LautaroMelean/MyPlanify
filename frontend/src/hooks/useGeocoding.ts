import { useQuery } from '@tanstack/react-query'
import { geocodingService } from '@/services/geocodingService'

export function useGeocoding(query: string) {
  return useQuery({
    queryKey: ['geocoding', query],
    queryFn: () => geocodingService.geocode(query),
    enabled: query.trim().length >= 3,
    staleTime: 1000 * 60 * 60, // 1 hour — addresses don't change
  })
}

export function useReverseGeocoding(lat: number | null, lon: number | null) {
  return useQuery({
    queryKey: ['geocoding-reverse', lat, lon],
    queryFn: () => geocodingService.reverseGeocode(lat!, lon!),
    enabled: lat !== null && lon !== null,
    staleTime: 1000 * 60 * 60,
  })
}
