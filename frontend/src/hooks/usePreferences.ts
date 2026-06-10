import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { preferencesService } from '@/services/preferencesService'

export function usePreferences() {
  return useQuery({
    queryKey: ['preferences'],
    queryFn: preferencesService.list,
  })
}

export function useSetPreferences() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: preferencesService.set,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['preferences'] }),
  })
}

export function useRemovePreference() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: preferencesService.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['preferences'] }),
  })
}
