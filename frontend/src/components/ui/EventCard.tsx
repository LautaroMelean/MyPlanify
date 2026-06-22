import { useNavigate } from 'react-router-dom'
import { Calendar, DollarSign, MapPin } from 'lucide-react'
import type { Event } from '@/types'
import FavoriteButton from './FavoriteButton'
import { RatingBadge } from './ReviewSection'
import { formatARS, formatDateShort } from '@/lib/format'

interface EventCardProps {
  event: Event
}

export default function EventCard({ event }: EventCardProps) {
  const navigate = useNavigate()
  const startDate = new Date(event.start_date)

  return (
    <div
      className="group bg-white rounded-xl border border-gray-200 shadow-glass-sm overflow-hidden hover:shadow-neon-sm hover:border-primary-500/30 transition-all cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40 touch-manipulation active:scale-[0.98]"
      onClick={() => navigate(`/events/${event.id}`)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate(`/events/${event.id}`)}
      role="button"
      tabIndex={0}
      aria-label={event.title}
    >
      <div className="overflow-hidden h-28 sm:h-40">
        {event.image_url ? (
          <img src={event.image_url} alt="" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" />
        ) : (
          <div className="w-full h-full bg-indigo-500/10 flex items-center justify-center" aria-hidden="true">
            <Calendar className="h-8 w-8 sm:h-10 sm:w-10 text-indigo-400" />
          </div>
        )}
      </div>

      <div className="p-3 sm:p-4">
        <div className="flex items-start justify-between gap-1.5">
          <div className="flex items-start gap-2 min-w-0 flex-1">
            {/* Mini date badge */}
            <div className="flex-shrink-0 w-9 text-center bg-primary-500/10 rounded-lg py-1">
              <p className="text-sm font-bold text-primary-600 leading-none">
                {startDate.getDate()}
              </p>
              <p className="text-[9px] font-medium text-primary-500 uppercase">
                {startDate.toLocaleDateString('es-AR', { month: 'short' })}
              </p>
            </div>
            <div className="min-w-0 flex-1">
              <h3 className="font-semibold text-gray-900 truncate text-sm">{event.title}</h3>
              <p className="text-xs text-gray-500 mt-0.5">{formatDateShort(event.start_date)}</p>
            </div>
          </div>
          <div onClick={(e) => e.stopPropagation()} className="flex-shrink-0">
            <FavoriteButton itemId={event.id} itemType="event" />
          </div>
        </div>

        {/* Description — only on sm+ */}
        {event.description && (
          <p className="hidden sm:block text-sm text-gray-600 mt-2 line-clamp-2">{event.description}</p>
        )}

        {/* Category + rating + price */}
        <div className="flex items-center justify-between mt-2 gap-1">
          <span className="text-xs bg-primary-500/15 text-primary-600 px-1.5 py-0.5 rounded-full font-medium truncate max-w-[50%]">
            {event.category}
          </span>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            {event.avg_rating != null && (
              <RatingBadge average={event.avg_rating} count={event.review_count} />
            )}
            <span className="text-xs text-gray-500 flex items-center gap-0.5 flex-shrink-0">
              <DollarSign className="h-3 w-3" aria-hidden="true" />
              {formatARS(event.price)}
            </span>
          </div>
        </div>

        {/* Place name — only on sm+ */}
        {event.place_name && (
          <p className="hidden sm:flex text-xs text-gray-500 mt-2 items-center gap-1">
            <MapPin className="h-3 w-3" aria-hidden="true" />
            {event.place_name}
          </p>
        )}
      </div>
    </div>
  )
}
