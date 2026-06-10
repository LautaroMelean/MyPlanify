import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { favoritesService } from '@/services/favoritesService'

export function useFavorites() {
  return useQuery({
    queryKey: ['favorites'],
    queryFn: favoritesService.list,
    staleTime: 1000 * 60 * 2,
  })
}

export function useAddFavorite() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: favoritesService.add,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['favorites'] }),
  })
}

export function useRemoveFavorite() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: favoritesService.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['favorites'] }),
  })
}
