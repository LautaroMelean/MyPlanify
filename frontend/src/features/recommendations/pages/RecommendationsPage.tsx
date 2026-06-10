import { useEffect, useState } from 'react'
import { Sparkles, MapPin, Activity, Calendar } from 'lucide-react'
import { useRecommendations } from '@/hooks/useRecommendations'
import FavoriteButton from '@/components/ui/FavoriteButton'
import Loading from '@/components/common/Loading'
import EmptyState from '@/components/common/EmptyState'
import type { Recommendation } from '@/types'

export default function RecommendationsPage() {
  const [coords, setCoords] = useState<{ lat: number; lon: number } | null>(null)

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition(
      (pos) => setCoords({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      () => setCoords(null),
    )
  }, [])

  const { data: recommendations = [], isLoading } = useRecommendations(
    coords ? { lat: coords.lat, lon: coords.lon } : {},
  )

  if (isLoading) return <Loading message="Generando recomendaciones..." fullPage />

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1 flex items-center gap-2">
          <Sparkles className="h-6 w-6 text-primary-600" />
          Para vos
        </h1>
        <p className="text-gray-500 text-sm">
          Recomendaciones personalizadas basadas en tus preferencias
          {coords ? ' y tu ubicación actual' : ''}.
        </p>
      </div>

      {recommendations.length === 0 ? (
        <EmptyState
          title="Sin recomendaciones todavía"
          description="Configurá tus preferencias en el perfil para recibir sugerencias personalizadas."
          icon={<Sparkles className="h-12 w-12 text-gray-300" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {recommendations.map((rec) => (
            <RecommendationCard key={rec.id} rec={rec} />
          ))}
        </div>
      )}
    </div>
  )
}

function RecommendationCard({ rec }: { rec: Recommendation }) {
  const score = Math.round(parseFloat(rec.score))

  const name =
    rec.activity_detail?.name ??
    rec.event_detail?.title ??
    rec.place_detail?.name ??
    '—'

  const category =
    rec.activity_detail?.category ??
    rec.event_detail?.category ??
    rec.place_detail?.category ??
    ''

  const itemId =
    rec.activity ?? rec.event ?? rec.place ?? ''

  const icon =
    rec.item_type === 'activity' ? <Activity className="h-4 w-4" /> :
    rec.item_type === 'event' ? <Calendar className="h-4 w-4" /> :
    <MapPin className="h-4 w-4" />

  const typeLabel =
    rec.item_type === 'activity' ? 'Actividad' :
    rec.item_type === 'event' ? 'Evento' : 'Lugar'

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-4 flex flex-col gap-3 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 text-xs text-gray-500 mb-1">
            {icon}
            <span>{typeLabel}</span>
          </div>
          <h3 className="font-semibold text-gray-900 truncate">{name}</h3>
          {category && (
            <span className="text-xs bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full">
              {category}
            </span>
          )}
        </div>
        <div className="flex flex-col items-center flex-shrink-0">
          <span className="text-lg font-bold text-primary-600">{score}</span>
          <span className="text-xs text-gray-400">pts</span>
        </div>
      </div>

      {rec.recommendation_reason && (
        <p className="text-xs text-gray-500 italic">{rec.recommendation_reason}</p>
      )}

      {itemId && rec.item_type && (
        <div className="flex justify-end">
          <FavoriteButton itemId={itemId} itemType={rec.item_type} />
        </div>
      )}
    </div>
  )
}
