import { useQuery } from '@tanstack/react-query'
import { activitiesService, type ActivitiesFilters } from '@/services/activitiesService'

export function useActivitiesPaginated(filters: ActivitiesFilters & { page: number }) {
  return useQuery({
    queryKey: ['activities-paginated', filters],
    queryFn: () => activitiesService.listPaginated(filters),
    staleTime: 1000 * 60 * 5,
    placeholderData: (prev) => prev,
  })
}

export function useActivity(id: string) {
  return useQuery({
    queryKey: ['activities', id],
    queryFn: () => activitiesService.get(id),
    enabled: !!id,
  })
}
