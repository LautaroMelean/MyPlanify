import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles, MapPin, Users, DollarSign, ArrowRight, Compass, Map, Heart, TrendingUp } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { useWeather } from '@/hooks/useWeather'
import { useForecast } from '@/hooks/useForecast'
import { usePlanner } from '@/hooks/usePlanner'
import { usePlaces } from '@/hooks/usePlaces'
import WeatherWidget from '@/components/ui/WeatherWidget'
import WeatherForecastWidget from '@/components/ui/WeatherForecastWidget'
import PlaceCard from '@/components/ui/PlaceCard'

// Buenos Aires coords — foco de la app
const BA = { lat: -34.6037, lon: -58.3816 }

const TODAY = new Date().toISOString().split('T')[0]
const TODAY_LABEL = new Date().toLocaleDateString('es-AR', {
  weekday: 'long', day: 'numeric', month: 'long',
})

const QUICK_ACTIONS = [
  { to: '/explorar',        icon: <Compass className="h-5 w-5 text-blue-600" />,  bg: 'bg-blue-50',   label: 'Explorar' },
  { to: '/mapa',            icon: <Map className="h-5 w-5 text-green-600" />,     bg: 'bg-green-50',  label: 'Mapa' },
  { to: '/favoritos',       icon: <Heart className="h-5 w-5 text-red-500" />,     bg: 'bg-red-50',    label: 'Favoritos' },
  { to: '/recomendaciones', icon: <TrendingUp className="h-5 w-5 text-purple-600" />, bg: 'bg-purple-50', label: 'Para vos' },
]

export default function HomePage() {
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const planner = usePlanner()

  const { data: weather } = useWeather(BA)
  const { data: forecast, isLoading: forecastLoading } = useForecast(BA)
  const { data: places = [] } = usePlaces({ city: 'Buenos Aires' })

  const [budget, setBudget] = useState('5000')
  const [people, setPeople] = useState('2')

  const handleGeneratePlan = () => {
    planner.mutate(
      { date: TODAY, budget, people_count: Number(people), city: 'Buenos Aires' },
      { onSuccess: (plan) => navigate(`/planes/${plan.id}`) },
    )
  }

  const featuredPlaces = places.slice(0, 6)

  return (
    <div className="flex flex-col gap-8 pb-8">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Hola, {user?.first_name} 👋
          </h1>
          <p className="text-gray-500 text-sm capitalize mt-0.5">{TODAY_LABEL} · Buenos Aires</p>
        </div>
        <WeatherWidget weather={weather} />
      </div>

      {/* HERO — generar plan */}
      <div className="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center gap-2 mb-1">
          <Sparkles className="h-5 w-5 text-yellow-300" />
          <span className="text-sm font-semibold text-indigo-200">Plan inteligente</span>
        </div>
        <h2 className="text-xl font-bold mb-4">¿Qué hacés hoy en Buenos Aires?</h2>

        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs text-indigo-200 flex items-center gap-1">
              <DollarSign className="h-3 w-3" /> Presupuesto (ARS)
            </label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-white placeholder-white/50 text-sm focus:outline-none focus:ring-2 focus:ring-white/50"
              placeholder="5000"
              min="0"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs text-indigo-200 flex items-center gap-1">
              <Users className="h-3 w-3" /> Personas
            </label>
            <input
              type="number"
              value={people}
              onChange={(e) => setPeople(e.target.value)}
              className="bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-white placeholder-white/50 text-sm focus:outline-none focus:ring-2 focus:ring-white/50"
              min="1"
              max="20"
            />
          </div>
        </div>

        <button
          onClick={handleGeneratePlan}
          disabled={planner.isPending}
          className="w-full flex items-center justify-center gap-2 bg-white text-indigo-700 font-bold py-3 rounded-xl hover:bg-indigo-50 transition-colors disabled:opacity-60 shadow-sm"
        >
          {planner.isPending ? (
            <>
              <span className="animate-spin h-4 w-4 border-2 border-indigo-400 border-t-transparent rounded-full" />
              Armando tu plan...
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4" />
              Generame un plan para hoy
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>

        {planner.isError && (
          <p className="text-xs text-red-300 mt-2 text-center">
            Error al generar el plan. Intentá de nuevo.
          </p>
        )}

        <p className="text-xs text-indigo-300 text-center mt-2">
          También podés ir al{' '}
          <button onClick={() => navigate('/planner')} className="underline hover:text-white">
            planner completo
          </button>{' '}
          para elegir la fecha
        </p>
      </div>

      {/* Pronóstico semanal */}
      <div>
        <h2 className="text-sm font-semibold text-gray-700 mb-2">Pronóstico de la semana en BA</h2>
        <WeatherForecastWidget forecast={forecast} isLoading={forecastLoading} highlightDate={TODAY} />
      </div>

      {/* Lugares destacados */}
      {featuredPlaces.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary-600" />
              <h2 className="text-sm font-semibold text-gray-700">Lugares en Buenos Aires</h2>
            </div>
            <button
              onClick={() => navigate('/explorar')}
              className="text-xs text-primary-600 hover:underline flex items-center gap-0.5"
            >
              Ver todos <ArrowRight className="h-3 w-3" />
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {featuredPlaces.map((place) => (
              <PlaceCard key={place.id} place={place} />
            ))}
          </div>
          {places.length === 0 && (
            <div className="text-center py-8 text-gray-400 text-sm">
              <MapPin className="h-8 w-8 mx-auto mb-2 text-gray-300" />
              Los lugares de Buenos Aires se cargan automáticamente.
              <br />
              Andá a <button onClick={() => navigate('/explorar')} className="text-primary-600 underline">Explorar → Cerca de mí</button> para sincronizar desde OpenStreetMap.
            </div>
          )}
        </div>
      )}

      {/* Acciones rápidas */}
      <div>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Más opciones</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {QUICK_ACTIONS.map((a) => (
            <button
              key={a.to}
              onClick={() => navigate(a.to)}
              className="flex items-center gap-3 bg-white border border-gray-200 rounded-xl px-4 py-3 hover:shadow-sm hover:border-primary-200 transition-all text-left"
            >
              <div className={`${a.bg} rounded-lg w-8 h-8 flex items-center justify-center flex-shrink-0`}>
                {a.icon}
              </div>
              <span className="text-sm font-medium text-gray-700">{a.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
