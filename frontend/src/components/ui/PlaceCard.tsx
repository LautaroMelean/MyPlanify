import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { MapPin, DollarSign, Wifi, TreePine, Ticket } from 'lucide-react'
import type { Place } from '@/types'
import FavoriteButton from './FavoriteButton'
import { RatingBadge } from './ReviewSection'
import { getCategoryImageUrl } from '@/lib/categoryImages'

interface PlaceCardProps {
  place: Place
}

const priceLabels = ['', 'Económico', 'Moderado', 'Caro', 'Muy caro']

export default function PlaceCard({ place }: PlaceCardProps) {
  const navigate = useNavigate()
  const [imgSrc, setImgSrc] = useState(place.image_url || getCategoryImageUrl(place.category))

  return (
    <div
      className="group bg-white rounded-2xl border border-gray-200 shadow-glass-sm overflow-hidden hover:shadow-neon-sm hover:border-primary-500/30 transition-all duration-200 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40 touch-manipulation active:scale-[0.98]"
      onClick={() => navigate(`/places/${place.id}`)}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate(`/places/${place.id}`)}
      role="button"
      tabIndex={0}
      aria-label={place.name}
    >
      {/* Image with overlays */}
      <div className="relative overflow-hidden h-36 sm:h-44">
        <img
          src={imgSrc}
          alt=""
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
          onError={() => setImgSrc(getCategoryImageUrl(place.category))}
        />
        {/* Gradient overlay for readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-black/5 to-transparent" aria-hidden="true" />

        {/* Category badge — bottom left on image */}
        <div className="absolute bottom-2 left-2.5">
          <span className="text-[10px] font-semibold text-white bg-black/50 backdrop-blur-sm border border-white/20 px-2 py-0.5 rounded-full">
            {place.category.split('/')[0].trim()}
          </span>
        </div>

        {/* Open/Closed badge — bottom right on image */}
        {place.is_open_now === true && (
          <div className="absolute bottom-2 right-2.5">
            <span className="text-[10px] font-semibold text-white bg-green-500/80 backdrop-blur-sm px-2 py-0.5 rounded-full">
              Abierto
            </span>
          </div>
        )}
        {place.is_open_now === false && (
          <div className="absolute bottom-2 right-2.5">
            <span className="text-[10px] font-semibold text-white bg-red-500/70 backdrop-blur-sm px-2 py-0.5 rounded-full">
              Cerrado
            </span>
          </div>
        )}

        {/* Favorite button — top right on image */}
        <div onClick={(e) => e.stopPropagation()} className="absolute top-2 right-2">
          <FavoriteButton itemId={place.id} itemType="place" variant="dark" />
        </div>
      </div>

      {/* Info */}
      <div className="p-3 sm:p-4">
        <h3 className="font-semibold text-gray-900 truncate text-sm leading-snug">{place.name}</h3>
        <p className="text-xs text-gray-500 flex items-center gap-0.5 mt-0.5 truncate">
          <MapPin className="h-3 w-3 flex-shrink-0" aria-hidden="true" />
          {place.city}
        </p>

        {/* Description — sm+ */}
        {place.description && (
          <p className="hidden sm:block text-xs text-gray-500 mt-2 line-clamp-2 leading-relaxed">
            {place.description}
          </p>
        )}

        {/* Feature badges — sm+ */}
        {(place.outdoor_seating || place.fee === false || place.internet_access) && (
          <div className="hidden sm:flex flex-wrap gap-1 mt-2">
            {place.outdoor_seating && (
              <span className="text-[10px] bg-emerald-500/12 text-emerald-600 px-1.5 py-0.5 rounded-full flex items-center gap-0.5 font-medium">
                <TreePine className="h-3 w-3" aria-hidden="true" /> Terraza
              </span>
            )}
            {place.fee === false && (
              <span className="text-[10px] bg-blue-500/12 text-blue-600 px-1.5 py-0.5 rounded-full flex items-center gap-0.5 font-medium">
                <Ticket className="h-3 w-3" aria-hidden="true" /> Gratis
              </span>
            )}
            {place.internet_access && (
              <span className="text-[10px] bg-violet-500/12 text-violet-600 px-1.5 py-0.5 rounded-full flex items-center gap-0.5 font-medium">
                <Wifi className="h-3 w-3" aria-hidden="true" /> Wifi
              </span>
            )}
          </div>
        )}

        {/* Rating + Price */}
        {(place.avg_rating != null || place.price_level > 0) && (
          <div className="flex items-center justify-between mt-2.5 pt-2.5 border-t border-gray-100">
            <div>
              {place.avg_rating != null && (
                <RatingBadge average={place.avg_rating} count={place.review_count} />
              )}
            </div>
            {place.price_level > 0 && (
              <span className="text-[10px] text-gray-400 flex items-center gap-0.5">
                <DollarSign className="h-3 w-3" aria-hidden="true" />
                {priceLabels[place.price_level] ?? ''}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
