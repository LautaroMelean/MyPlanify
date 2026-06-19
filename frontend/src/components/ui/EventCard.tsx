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

  return (
    <div
      className="group bg-white rounded-xl border border-gray-200 shadow-glass-sm overflow-hidden hover:shadow-neon-sm hover:border-primary-500/30 transition-all cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40"
      onClick={() => navigate(`/events/${event.id}`)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate(`/events/${event.id}`)}
      role="button"
      tabIndex={0}
      aria-label={event.title}
    >
      <div className="overflow-hidden h-40">
        {event.image_url ? (
          <img src={event.image_url} alt="" className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" />
        ) : (
          <div className="w-full h-40 bg-indigo-500/10 flex items-center justify-center" aria-hidden="true">
            <Calendar className="h-10 w-10 text-indigo-400" />
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-start gap-3 min-w-0">
            {/* Mini date badge */}
            <div className="flex-shrink-0 w-10 text-center bg-primary-500/10 rounded-lg py-1">
              <p className="text-sm font-bold text-primary-600 leading-none">
                {new Date(event.start_date).getDate()}
              </p>
              <p className="text-[9px] font-medium text-primary-500 uppercase">
                {new Date(event.start_date).toLocaleDateString('es-AR', { month: 'short' })}
              </p>
            </div>
            <div className="min-w-0">
              <h3 className="font-semibold text-gray-900 truncate">{event.title}</h3>
              <p className="text-xs text-gray-500 mt-0.5">
                {formatDateShort(event.start_date)}
              </p>
            </div>
          </div>
          <div onClick={(e) => e.stopPropagation()}>
            <FavoriteButton itemId={event.id} itemType="event" />
          </div>
        </div>

        {event.description && (
          <p className="text-sm text-gray-600 mt-2 line-clamp-2">{event.description}</p>
        )}

        <div className="flex items-center justify-between mt-3">
          <span className="text-xs bg-primary-500/15 text-primary-600 px-2 py-0.5 rounded-full font-medium">
            {event.category}
          </span>
          <div className="flex items-center gap-2">
            {event.avg_rating != null && (
              <RatingBadge average={event.avg_rating} count={event.review_count} />
            )}
            <span className="text-xs text-gray-500 flex items-center gap-0.5">
              <DollarSign className="h-3 w-3" aria-hidden="true" />
              {formatARS(event.price)}
            </span>
          </div>
        </div>

        {event.place_name && (
          <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
            <MapPin className="h-3 w-3" aria-hidden="true" />
            {event.place_name}
          </p>
        )}
      </div>
    </div>
  )
}
