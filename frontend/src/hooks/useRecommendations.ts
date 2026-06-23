import { useQuery } from '@tanstack/react-query'
import { recommendationsService, type RecommendationFilters } from '@/services/recommendationsService'

export function useRecommendations(filters: RecommendationFilters = {}, enabled = true) {
  return useQuery({
    queryKey: ['recommendations', filters],
    queryFn: () => recommendationsService.list(filters),
    staleTime: 0,
    enabled,
  })
}
