import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles } from 'lucide-react'
import { TrendingPlanCard } from './TrendingPlanCard'
import { ClonePlanModal } from './ClonePlanModal'
import { useTrendingPlans, useClonePlan } from '@/hooks/usePlanner'
import type { TrendingPlan } from '@/types'

export function InspireFeed() {
  const navigate = useNavigate()
  const { data: plans = [], isLoading } = useTrendingPlans({ limit: 6 })
  const clonePlan = useClonePlan()
  const [selectedPlan, setSelectedPlan] = useState<TrendingPlan | null>(null)

  const handleClone = (date: string) => {
    if (!selectedPlan) return
    clonePlan.mutate(
      { planId: selectedPlan.id, date },
      {
        onSuccess: (cloned) => {
          setSelectedPlan(null)
          navigate(`/planes/${cloned.id}`)
        },
      }
    )
  }

  if (isLoading) {
    return (
      <div aria-busy="true">
        <p className="sr-only">Cargando planes populares</p>
        <div className="flex items-center gap-2 mb-3">
          <div className="h-4 w-4 bg-gray-200/20 rounded-full animate-pulse" />
          <div className="h-4 w-40 bg-gray-200/20 rounded animate-pulse" />
        </div>
        <div className="grid sm:grid-cols-2 gap-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-white border border-gray-200 rounded-xl p-4 shadow-glass-sm animate-pulse">
              <div className="h-4 w-3/4 bg-gray-200/20 rounded mb-2" />
              <div className="flex gap-3 mb-3">
                <div className="h-3 w-16 bg-gray-200/20 rounded" />
                <div className="h-3 w-12 bg-gray-200/20 rounded" />
              </div>
              <div className="h-7 w-full bg-gray-200/20 rounded-xl" />
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="h-4 w-4 text-primary-500" />
        <h2 className="text-sm font-semibold text-gray-600">Inspirate — Planes populares</h2>
      </div>

      {plans.length === 0 ? (
        <p className="text-sm text-gray-500 text-center py-4">
          Todavía no hay planes populares. ¡Sé el primero en compartir el tuyo!
        </p>
      ) : (
        <div className="grid sm:grid-cols-2 gap-3">
          {plans.map((plan) => (
            <TrendingPlanCard
              key={plan.id}
              plan={plan}
              onUseAsBase={setSelectedPlan}
            />
          ))}
        </div>
      )}

      <ClonePlanModal
        isOpen={selectedPlan !== null}
        onClose={() => setSelectedPlan(null)}
        onConfirm={handleClone}
        isLoading={clonePlan.isPending}
      />
    </div>
  )
}
