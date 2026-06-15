import { useQuery } from '@tanstack/react-query'
import { plannerService } from '@/services/plannerService'

export function useTrendingPlans(params?: { city?: string; period?: string; limit?: number }) {
  return useQuery({
    queryKey: ['trending-plans', params],
    queryFn: () => plannerService.getTrending(params),
    staleTime: 5 * 60 * 1000,
  })
}
