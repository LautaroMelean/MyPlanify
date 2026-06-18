import { MapPin, Users, Eye, Share2 } from 'lucide-react'
import type { TrendingPlan } from '@/types'

interface Props {
  plan: TrendingPlan
  onUseAsBase: (plan: TrendingPlan) => void
}

export function TrendingPlanCard({ plan, onUseAsBase }: Props) {
  const formattedDate = new Date(plan.date + 'T00:00:00').toLocaleDateString('es-AR', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  })

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-glass-sm hover:shadow-neon-sm hover:border-primary-500/30 transition-all">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-gray-900 truncate">{plan.title}</h3>
          <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              {plan.city}
            </span>
            <span className="flex items-center gap-1">
              <Users className="h-3 w-3" />
              {plan.item_count} ítem{plan.item_count !== 1 ? 's' : ''}
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-1">{formattedDate}</p>
        </div>

        <div className="flex flex-col items-end gap-1 text-xs text-gray-400 flex-shrink-0">
          {plan.view_count > 0 && (
            <span className="flex items-center gap-1">
              <Eye className="h-3 w-3" />
              {plan.view_count}
            </span>
          )}
          {plan.share_count > 0 && (
            <span className="flex items-center gap-1">
              <Share2 className="h-3 w-3" />
              {plan.share_count}
            </span>
          )}
        </div>
      </div>

      <button
        onClick={() => onUseAsBase(plan)}
        aria-label={`Usar como base: ${plan.title}`}
        className="mt-3 w-full text-xs font-medium text-primary-600 hover:text-primary-700 border border-primary-400/30 hover:bg-primary-500/10 rounded-xl py-1.5 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40"
      >
        Usar como base
      </button>
    </div>
  )
}
