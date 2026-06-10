import { Tag, MapPin, Calendar, Percent } from 'lucide-react'
import { usePromotions } from '@/hooks/usePromotions'
import Loading from '@/components/common/Loading'
import EmptyState from '@/components/common/EmptyState'
import type { Promotion } from '@/types'

function formatDate(iso: string) {
  return new Intl.DateTimeFormat('es-AR', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(iso))
}

function PromotionCard({ promo }: { promo: Promotion }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden hover:shadow-md transition-shadow">
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 px-4 py-3 flex items-center justify-between">
        <span className="text-white font-bold text-xl flex items-center gap-1">
          <Percent className="h-5 w-5" />
          {promo.discount_percentage}% OFF
        </span>
        <Tag className="h-5 w-5 text-white/80" />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-gray-900">{promo.title}</h3>
        {promo.description && (
          <p className="text-sm text-gray-500 mt-1 line-clamp-2">{promo.description}</p>
        )}
        <div className="flex items-center gap-4 mt-3">
          {promo.place_name && (
            <span className="text-xs text-gray-400 flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              {promo.place_name}
            </span>
          )}
          <span className="text-xs text-gray-400 flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            Hasta {formatDate(promo.end_date)}
          </span>
        </div>
      </div>
    </div>
  )
}

export default function PromotionsPage() {
  const { data: promotions = [], isLoading } = usePromotions()

  if (isLoading) return <Loading />

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1 flex items-center gap-2">
          <Tag className="h-6 w-6 text-primary-600" />
          Promociones
        </h1>
        <p className="text-gray-500 text-sm">Descuentos y ofertas activas en lugares cercanos.</p>
      </div>

      {promotions.length === 0 ? (
        <EmptyState
          title="Sin promociones activas"
          description="Por el momento no hay promociones disponibles. Volvé más tarde."
          icon={<Tag className="h-8 w-8 text-gray-400" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {promotions.map((p) => (
            <PromotionCard key={p.id} promo={p} />
          ))}
        </div>
      )}
    </div>
  )
}
