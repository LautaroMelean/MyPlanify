import { useQuery } from '@tanstack/react-query'
import { promotionsService } from '@/services/promotionsService'

export function usePromotions(placeId?: string) {
  return useQuery({
    queryKey: ['promotions', placeId],
    queryFn: () => promotionsService.list(placeId ? { place: placeId } : {}),
    staleTime: 1000 * 60 * 5,
  })
}

