import { useQuery } from '@tanstack/react-query'
import { externalPlacesService } from '@/services/externalPlacesService'

interface Coords {
  lat: number
  lon: number
  radius?: number
  type?: string
}

export function useExternalPlaces(coords: Coords | null) {
  return useQuery({
    queryKey: ['external-places', coords],
    queryFn: () => externalPlacesService.getNearby(coords!),
    enabled: coords !== null,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours — OSM data is cached on the backend too
  })
}
