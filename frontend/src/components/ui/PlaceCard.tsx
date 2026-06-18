import { useNavigate } from 'react-router-dom'
import { MapPin, DollarSign, Wifi, TreePine, Ticket } from 'lucide-react'
import type { Place } from '@/types'
import FavoriteButton from './FavoriteButton'
import { RatingBadge } from './ReviewSection'

interface PlaceCardProps {
  place: Place
}

const priceLabels = ['', 'Económico', 'Moderado', 'Caro', 'Muy caro']

export default function PlaceCard({ place }: PlaceCardProps) {
  const navigate = useNavigate()

  return (
    <div
      className="group bg-white rounded-xl border border-gray-200 shadow-glass-sm overflow-hidden hover:shadow-neon-sm hover:border-primary-500/30 transition-all cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40"
      onClick={() => navigate(`/places/${place.id}`)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate(`/places/${place.id}`)}
      role="button"
      tabIndex={0}
      aria-label={place.name}
    >
      <div className="overflow-hidden h-40">
        {place.image_url ? (
          <img src={place.image_url} alt={place.name} className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" />
        ) : (
          <div className="w-full h-40 bg-primary-500/10 flex items-center justify-center">
            <MapPin className="h-10 w-10 text-primary-300" />
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h3 className="font-semibold text-gray-900 truncate">{place.name}</h3>
            <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
              <MapPin className="h-3 w-3 flex-shrink-0" />
              {place.city}
            </p>
          </div>
          <div onClick={(e) => e.stopPropagation()}>
            <FavoriteButton itemId={place.id} itemType="place" />
          </div>
        </div>

        {place.description && (
          <p className="text-sm text-gray-600 mt-2 line-clamp-2">{place.description}</p>
        )}

        {/* Enriched badges row */}
        {(place.is_open_now !== null || place.outdoor_seating || place.fee === false || place.internet_access) && (
          <div className="flex flex-wrap gap-1 mt-2">
            {place.is_open_now === true && (
              <span className="text-xs bg-green-500/15 text-green-400 px-2 py-0.5 rounded-full font-medium">
                Abierto ahora
              </span>
            )}
            {place.is_open_now === false && (
              <span className="text-xs bg-red-500/15 text-red-400 px-2 py-0.5 rounded-full font-medium">
                Cerrado
              </span>
            )}
            {place.outdoor_seating && (
              <span className="text-xs bg-emerald-500/15 text-emerald-400 px-2 py-0.5 rounded-full flex items-center gap-0.5">
                <TreePine className="h-3 w-3" />
                Con terraza
              </span>
            )}
            {place.fee === false && (
              <span className="text-xs bg-blue-500/15 text-blue-400 px-2 py-0.5 rounded-full flex items-center gap-0.5">
                <Ticket className="h-3 w-3" />
                Entrada libre
              </span>
            )}
            {place.internet_access && (
              <span className="text-xs bg-violet-500/15 text-violet-400 px-2 py-0.5 rounded-full flex items-center gap-0.5">
                <Wifi className="h-3 w-3" />
                Wifi
              </span>
            )}
          </div>
        )}

        <div className="flex items-center justify-between mt-3">
          <div className="flex items-center gap-1">
            <span className="text-xs bg-primary-500/15 text-primary-600 px-2 py-0.5 rounded-full font-medium">
              {place.category}
            </span>
            {place.cuisine && (
              <span className="text-xs text-gray-500">{place.cuisine.split(';')[0]}</span>
            )}
          </div>
          <div className="flex items-center gap-2">
            {place.avg_rating != null && (
              <RatingBadge average={place.avg_rating} count={place.review_count} />
            )}
            {place.price_level > 0 && (
              <span className="text-xs text-gray-500 flex items-center gap-0.5">
                <DollarSign className="h-3 w-3" />
                {priceLabels[place.price_level] ?? ''}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
