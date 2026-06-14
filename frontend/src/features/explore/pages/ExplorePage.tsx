import { useState } from 'react'
import { MapPin, Activity, Calendar, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { usePlaces } from '@/hooks/usePlaces'
import { useActivities } from '@/hooks/useActivities'
import { useEvents } from '@/hooks/useEvents'
import { useTrending } from '@/hooks/useTrending'
import PlaceCard from '@/components/ui/PlaceCard'
import ActivityCard from '@/components/ui/ActivityCard'
import EventCard from '@/components/ui/EventCard'
import SearchBar from '@/components/ui/SearchBar'
import Loading from '@/components/common/Loading'
import EmptyState from '@/components/common/EmptyState'

type Tab = 'lugares' | 'actividades' | 'eventos'

export default function ExplorePage() {
  const [tab, setTab] = useState<Tab>('lugares')
  const [search, setSearch] = useState('')
  const navigate = useNavigate()

  const places = usePlaces({ city: search || undefined })
  const activities = useActivities({ category: search || undefined })
  const events = useEvents({ category: search || undefined })
  const { data: trending } = useTrending()

  const showTrending = !search

  const tabs: { id: Tab; label: string; icon: React.ReactNode }[] = [
    { id: 'lugares', label: 'Lugares', icon: <MapPin className="h-4 w-4" /> },
    { id: 'actividades', label: 'Actividades', icon: <Activity className="h-4 w-4" /> },
    { id: 'eventos', label: 'Eventos', icon: <Calendar className="h-4 w-4" /> },
  ]

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Explorar</h1>
        <p className="text-gray-500 text-sm">Descubrí lugares, actividades y eventos cerca tuyo.</p>
      </div>

      <SearchBar
        value={search}
        onChange={setSearch}
        placeholder={tab === 'lugares' ? 'Buscar por ciudad...' : 'Buscar por categoría...'}
        className="max-w-md"
      />

      {/* Trending section — shown only when no search active */}
      {showTrending && trending && (
        <>
          {trending.places.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="h-4 w-4 text-primary-600" />
                <h2 className="text-sm font-semibold text-gray-700">Lugares más populares</h2>
              </div>
              <div className="flex gap-3 overflow-x-auto pb-1 -mx-1 px-1">
                {trending.places.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => navigate(`/places/${p.id}`)}
                    className="flex-shrink-0 w-44 bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow text-left"
                  >
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className="w-full h-24 object-cover" />
                    ) : (
                      <div className="w-full h-24 bg-primary-50 flex items-center justify-center">
                        <MapPin className="h-8 w-8 text-primary-300" />
                      </div>
                    )}
                    <div className="p-2">
                      <p className="text-xs font-semibold text-gray-900 truncate">{p.name}</p>
                      <p className="text-xs text-gray-400 truncate">{p.city}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {trending.events.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="h-4 w-4 text-primary-600" />
                <h2 className="text-sm font-semibold text-gray-700">Eventos más guardados</h2>
              </div>
              <div className="flex gap-3 overflow-x-auto pb-1 -mx-1 px-1">
                {trending.events.map((e) => (
                  <button
                    key={e.id}
                    onClick={() => navigate(`/events/${e.id}`)}
                    className="flex-shrink-0 w-44 bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow text-left"
                  >
                    {e.image_url ? (
                      <img src={e.image_url} alt={e.title} className="w-full h-24 object-cover" />
                    ) : (
                      <div className="w-full h-24 bg-indigo-50 flex items-center justify-center">
                        <Calendar className="h-8 w-8 text-indigo-300" />
                      </div>
                    )}
                    <div className="p-2">
                      <p className="text-xs font-semibold text-gray-900 truncate">{e.title}</p>
                      <p className="text-xs text-gray-400">
                        {new Date(e.start_date).toLocaleDateString('es-AR', { day: 'numeric', month: 'short' })}
                      </p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-200">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px ${
              tab === t.id
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.icon}
            {t.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {tab === 'lugares' && (
        <TabContent isLoading={places.isLoading} isEmpty={!places.data?.length}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {places.data?.map((place) => <PlaceCard key={place.id} place={place} />)}
          </div>
        </TabContent>
      )}

      {tab === 'actividades' && (
        <TabContent isLoading={activities.isLoading} isEmpty={!activities.data?.length}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {activities.data?.map((activity) => <ActivityCard key={activity.id} activity={activity} />)}
          </div>
        </TabContent>
      )}

      {tab === 'eventos' && (
        <TabContent isLoading={events.isLoading} isEmpty={!events.data?.length}>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {events.data?.map((event) => <EventCard key={event.id} event={event} />)}
          </div>
        </TabContent>
      )}
    </div>
  )
}

function TabContent({
  isLoading,
  isEmpty,
  children,
}: {
  isLoading: boolean
  isEmpty: boolean
  children: React.ReactNode
}) {
  if (isLoading) return <Loading message="Cargando..." />
  if (isEmpty)
    return (
      <EmptyState
        title="Sin resultados"
        description="No encontramos nada con ese criterio. Probá con otro término."
      />
    )
  return <>{children}</>
}
