import { useNavigate } from 'react-router-dom'
import { Users, DollarSign, Cloud, Home, MapPin } from 'lucide-react'
import type { Activity } from '@/types'
import FavoriteButton from './FavoriteButton'
import { RatingBadge } from './ReviewSection'
import { formatARS } from '@/lib/format'
import { ACTIVITY_TYPE_LABELS } from '@/lib/activityTypes'

interface ActivityCardProps {
  activity: Activity
}

const typeColors: Record<string, string> = {
  restaurant: 'from-orange-400 to-amber-500',
  bar: 'from-purple-500 to-violet-600',
  cinema: 'from-red-400 to-rose-500',
  museum: 'from-blue-400 to-indigo-500',
  park: 'from-green-400 to-emerald-500',
  sports: 'from-cyan-400 to-sky-500',
  concert: 'from-pink-400 to-fuchsia-500',
  gaming: 'from-violet-400 to-purple-600',
  tourism: 'from-teal-400 to-cyan-500',
  shopping: 'from-yellow-400 to-amber-500',
}

const typeEmojis: Record<string, string> = {
  restaurant: '🍽️', bar: '🍺', cinema: '🎬', museum: '🏛️',
  park: '🌳', sports: '⚽', concert: '🎵', gaming: '🎮',
  tourism: '✈️', shopping: '🛍️',
}

function isFree(value: string | number | null | undefined): boolean {
  if (value === null || value === undefined) return false
  return parseFloat(String(value)) === 0
}

export default function ActivityCard({ activity }: ActivityCardProps) {
  const navigate = useNavigate()
  const gradient = typeColors[activity.activity_type] ?? 'from-primary-400 to-primary-600'

  return (
    <div
      className="group bg-white rounded-xl border border-gray-200 shadow-glass-sm overflow-hidden hover:shadow-neon-sm hover:border-primary-500/30 transition-all cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40 touch-manipulation active:scale-[0.98]"
      onClick={() => navigate(`/activities/${activity.id}`)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate(`/activities/${activity.id}`)}
      role="button"
      tabIndex={0}
      aria-label={activity.name}
    >
      <div className="overflow-hidden h-28 sm:h-40">
        {activity.image_url ? (
          <img
            src={activity.image_url}
            alt=""
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        ) : (
          <div className={`w-full h-full bg-gradient-to-br ${gradient} flex items-center justify-center`} aria-hidden="true">
            <span className="text-3xl sm:text-5xl">{typeEmojis[activity.activity_type] ?? '⚡'}</span>
          </div>
        )}
      </div>

      <div className="p-3 sm:p-4">
        <div className="flex items-start justify-between gap-1.5">
          <div className="min-w-0 flex-1">
            <h3 className="font-semibold text-gray-900 truncate text-sm">{activity.name}</h3>
            <span className="text-xs bg-primary-500/15 text-primary-600 px-1.5 py-0.5 rounded-full font-medium inline-block mt-0.5">
              {ACTIVITY_TYPE_LABELS[activity.activity_type] ?? activity.activity_type}
            </span>
          </div>
          <div onClick={(e) => e.stopPropagation()} className="flex-shrink-0">
            <FavoriteButton itemId={activity.id} itemType="activity" />
          </div>
        </div>

        {/* Description — only on sm+ */}
        {activity.description && (
          <p className="hidden sm:block text-sm text-gray-600 mt-2 line-clamp-2">{activity.description}</p>
        )}

        {/* Address — only on sm+ */}
        {activity.address && (
          <div className="hidden sm:flex items-start gap-1 mt-1.5">
            <MapPin className="h-3.5 w-3.5 text-gray-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
            <span className="text-xs text-gray-500 leading-snug">
              <span className="block">{activity.address}</span>
              {activity.city && <span className="block text-gray-400">{activity.city}</span>}
            </span>
          </div>
        )}

        {/* Rating — always visible */}
        {activity.avg_rating != null && (
          <div className="mt-2">
            <RatingBadge average={activity.avg_rating} count={activity.review_count} />
          </div>
        )}

        {/* Meta badges — only on sm+ */}
        <div className="hidden sm:flex flex-wrap gap-2 mt-3">
          <span className="text-xs text-gray-500 flex items-center gap-1">
            <DollarSign className="h-3 w-3" aria-hidden="true" />
            {isFree(activity.min_budget) ? 'Gratis' : `Desde ${formatARS(activity.min_budget)}`}
          </span>
          {activity.min_people > 1 && (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              <Users className="h-3 w-3" aria-hidden="true" />
              {activity.min_people}+ personas
            </span>
          )}
          {activity.indoor && (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              <Home className="h-3 w-3" aria-hidden="true" />
              Interior
            </span>
          )}
          {activity.outdoor && (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              <Cloud className="h-3 w-3" aria-hidden="true" />
              Exterior
            </span>
          )}
        </div>

        {/* Price — mobile only shorthand */}
        <p className="sm:hidden text-xs text-gray-500 mt-2 flex items-center gap-0.5">
          <DollarSign className="h-3 w-3" aria-hidden="true" />
          {isFree(activity.min_budget) ? 'Gratis' : `Desde ${formatARS(activity.min_budget)}`}
        </p>
      </div>
    </div>
  )
}
