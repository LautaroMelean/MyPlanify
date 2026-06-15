import { useMutation, useQueryClient } from '@tanstack/react-query'
import { plannerService } from '@/services/plannerService'
import type { PlanStatus } from '@/types'

export function useAddPlanItem(planId: string) {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: (payload: { entity_type: string; entity_id: string; slot: string; note?: string }) =>
      plannerService.addItem(planId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['plan', planId] })
    },
  })
}

export function useRemovePlanItem(planId: string) {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: (itemId: string) => plannerService.removeItem(planId, itemId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['plan', planId] })
    },
  })
}

export function useUpdatePlan(planId: string) {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: (payload: { is_public?: boolean; status?: PlanStatus; title?: string }) =>
      plannerService.patch(planId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['plan', planId] })
      qc.invalidateQueries({ queryKey: ['my-plans'] })
    },
  })
}

export function useDeletePlan() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: (planId: string) => plannerService.deletePlan(planId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['my-plans'] })
    },
  })
}

export function useUpdatePlanItem(planId: string) {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: ({ itemId, payload }: { itemId: string; payload: { note?: string; order?: number } }) =>
      plannerService.updateItem(planId, itemId, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['plan', planId] })
    },
  })
}

export function useClonePlan() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: ({ planId, date }: { planId: string; date: string }) =>
      plannerService.clonePlan(planId, date),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['my-plans'] })
    },
  })
}

export function useSurprisePlan() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: (date?: string) => plannerService.surprise(date),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['my-plans'] })
    },
  })
}
