import { useNavigate } from 'react-router-dom'
import { CalendarDays, Trash2, Globe, Lock, Plus, Loader2 } from 'lucide-react'
import { useMyPlans } from '@/hooks/useMyPlans'
import { useDeletePlan } from '@/hooks/usePlanItem'
import Button from '@/components/ui/Button'
import EmptyState from '@/components/common/EmptyState'

function formatPlanDate(iso: string) {
  return new Date(iso + 'T12:00:00').toLocaleDateString('es-AR', {
    day: 'numeric', month: 'short', year: 'numeric',
  })
}

export default function MyPlansPage() {
  const navigate = useNavigate()
  const { data: plans, isLoading } = useMyPlans()
  const deletePlan = useDeletePlan()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-48 gap-2 text-gray-500 text-sm">
        <Loader2 className="h-5 w-5 animate-spin" />
        Cargando planes...
      </div>
    )
  }

  const handleDelete = (e: React.MouseEvent, planId: string) => {
    e.stopPropagation()
    if (window.confirm('¿Eliminás este plan? Esta acción no se puede deshacer.')) {
      deletePlan.mutate(planId)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <CalendarDays className="h-7 w-7 text-primary-600" />
          <h1 className="text-2xl font-bold text-gray-900">Mis Planes</h1>
        </div>
        <Button size="sm" leftIcon={<Plus className="h-4 w-4" />} onClick={() => navigate('/planner')}>
          Nuevo plan
        </Button>
      </div>

      {(!plans || plans.length === 0) ? (
        <EmptyState
          title="Todavía no tenés planes"
          description="Usá el Planner para generar tu primer itinerario del día."
          icon={<CalendarDays className="h-12 w-12 text-gray-300" />}
          action={{ label: 'Crear mi primer plan', onClick: () => navigate('/planner') }}
        />
      ) : (
        <div className="space-y-3">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-glass-sm hover:border-primary-500/30 hover:shadow-neon-sm transition-all cursor-pointer"
              onClick={() => navigate(`/planes/${plan.id}`)}
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-semibold text-gray-800 truncate">{plan.title}</h3>
                  {plan.is_public ? (
                    <Globe className="h-3.5 w-3.5 text-green-500 flex-shrink-0" aria-label="Público" />
                  ) : (
                    <Lock className="h-3.5 w-3.5 text-gray-400 flex-shrink-0" aria-label="Privado" />
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-0.5">
                  {plan.city} · {formatPlanDate(plan.date)}
                  {plan.items.length > 0 && ` · ${plan.items.length} ${plan.items.length === 1 ? 'actividad' : 'actividades'}`}
                </p>
              </div>
              <button
                onClick={(e) => handleDelete(e, plan.id)}
                className="p-1.5 text-gray-300 hover:text-red-500 transition-colors flex-shrink-0 rounded-lg hover:bg-red-500/10"
                aria-label="Eliminar plan"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
