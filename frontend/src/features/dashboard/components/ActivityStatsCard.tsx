import { CheckCircle, MapPin, Globe, Star, Flame, Trophy } from 'lucide-react'
import Card from '@/components/ui/Card'
import type { UserActivityStats } from '@/types'

interface Props {
  stats: UserActivityStats
}

function StatItem({ icon, label, value }: { icon: React.ReactNode; label: string; value: string | number }) {
  return (
    <div className="flex flex-col items-center text-center p-3">
      <div className="mb-1 text-primary-500">{icon}</div>
      <span className="text-xl font-bold text-gray-900">{value}</span>
      <span className="text-xs text-gray-500 mt-0.5">{label}</span>
    </div>
  )
}

export function ActivityStatsCard({ stats }: Props) {
  const isEmpty =
    stats.plans_completed === 0 &&
    stats.places_visited === 0 &&
    stats.cities_explored === 0 &&
    stats.current_streak_weeks === 0

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-gray-800">Mi actividad</h3>
          <p className="text-xs text-gray-500 mt-0.5">Tu historial de planes en Planify.</p>
        </div>
        {stats.current_streak_weeks > 0 && (
          <div className="flex items-center gap-1 bg-orange-500/10 text-orange-400 px-2 py-1 rounded-full text-xs font-semibold">
            <Flame className="h-3.5 w-3.5" />
            {stats.current_streak_weeks} sem. seguidas
          </div>
        )}
      </div>

      {isEmpty ? (
        <p className="text-sm text-gray-400 text-center py-4">
          Sin actividad aún. ¡Completá tu primer plan para ver tus estadísticas!
        </p>
      ) : (
        <>
          <div className="grid grid-cols-3 divide-x divide-gray-200/30 border border-gray-200/30 rounded-xl mb-4">
            <StatItem
              icon={<CheckCircle className="h-5 w-5" />}
              label="Planes completados"
              value={stats.plans_completed}
            />
            <StatItem
              icon={<MapPin className="h-5 w-5" />}
              label="Lugares visitados"
              value={stats.places_visited}
            />
            <StatItem
              icon={<Globe className="h-5 w-5" />}
              label="Ciudades exploradas"
              value={stats.cities_explored}
            />
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            {stats.favorite_category && (
              <span className="flex items-center gap-1 bg-primary-500/15 text-primary-600 px-2.5 py-1 rounded-full font-medium capitalize">
                <Star className="h-3 w-3" />
                Favorita: {stats.favorite_category}
              </span>
            )}
            {stats.best_streak_weeks > 0 && (
              <span className="flex items-center gap-1 bg-yellow-500/15 text-yellow-400 px-2.5 py-1 rounded-full font-medium">
                <Trophy className="h-3 w-3" />
                Mejor racha: {stats.best_streak_weeks} sem.
              </span>
            )}
            {stats.avg_rating_given !== null && (
              <span className="flex items-center gap-1 bg-gray-300/10 text-gray-500 px-2.5 py-1 rounded-full font-medium">
                <Star className="h-3 w-3" />
                Rating promedio: {stats.avg_rating_given}
              </span>
            )}
          </div>
        </>
      )}
    </Card>
  )
}
