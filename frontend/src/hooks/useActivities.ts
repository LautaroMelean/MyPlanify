import { useQuery } from '@tanstack/react-query'
import { activitiesService } from '@/services/activitiesService'

export function useActivities(filters = {}) {
  return useQuery({
    queryKey: ['activities', filters],
    queryFn: () => activitiesService.list(filters),
    staleTime: 1000 * 60 * 5,
  })
}

export function useActivity(id: string) {
  return useQuery({
    queryKey: ['activities', id],
    queryFn: () => activitiesService.get(id),
    enabled: !!id,
  })
}
