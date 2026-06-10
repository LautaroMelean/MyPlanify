import { useQuery } from '@tanstack/react-query'
import { placesService } from '@/services/placesService'

export function usePlaces(filters = {}) {
  return useQuery({
    queryKey: ['places', filters],
    queryFn: () => placesService.list(filters),
    staleTime: 1000 * 60 * 5,
  })
}

export function usePlace(id: string) {
  return useQuery({
    queryKey: ['places', id],
    queryFn: () => placesService.get(id),
    enabled: !!id,
  })
}
