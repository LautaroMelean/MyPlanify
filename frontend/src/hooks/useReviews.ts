import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { reviewService } from '@/services/reviewService'
import type { ReviewEntityType } from '@/types'

export function useReviews(entityType: ReviewEntityType, entityId: string) {
  return useQuery({
    queryKey: ['reviews', entityType, entityId],
    queryFn: () => reviewService.getForEntity(entityType, entityId),
    enabled: Boolean(entityId),
    staleTime: 2 * 60 * 1000,
  })
}

export function useCreateReview(entityType: ReviewEntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (params: { stars: number; text: string }) =>
      reviewService.create({ entity_type: entityType, entity_id: entityId, ...params }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', entityType, entityId] })
    },
  })
}

export function useDeleteReview(entityType: ReviewEntityType, entityId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => reviewService.delete(entityType, entityId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', entityType, entityId] })
    },
  })
}
