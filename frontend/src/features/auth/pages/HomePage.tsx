import { Link } from 'react-router-dom'
import { MapPin, Calendar, Sparkles, Compass, Heart, Map } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

const QUICK_ACTIONS = [
  {
    to: '/explorar',
    icon: <Compass className="h-6 w-6 text-blue-600" />,
    bg: 'bg-blue-50',
    title: 'Explorar',
    description: 'Buscá lugares, actividades y eventos cerca tuyo.',
  },
  {
    to: '/recomendaciones',
    icon: <Sparkles className="h-6 w-6 text-purple-600" />,
    bg: 'bg-purple-50',
    title: 'Para vos',
    description: 'Recomendaciones personalizadas según tus gustos.',
  },
  {
    to: '/mapa',
    icon: <Map className="h-6 w-6 text-green-600" />,
    bg: 'bg-green-50',
    title: 'Mapa',
    description: 'Visualizá todos los lugares en el mapa interactivo.',
  },
  {
    to: '/favoritos',
    icon: <Heart className="h-6 w-6 text-red-500" />,
    bg: 'bg-red-50',
    title: 'Favoritos',
    description: 'Revisá los lugares y eventos que guardaste.',
  },
]

export default function HomePage() {
  const { user } = useAuthStore()

  return (
    <div className="flex flex-col gap-8">
      <section>
        <h1 className="text-3xl font-bold text-gray-900 mb-1">
          ¡Bienvenido, {user?.first_name}!
        </h1>
        <p className="text-gray-500">
          Descubrí planes personalizados según tu ubicación, estado de ánimo y preferencias.
        </p>
      </section>

      <section>
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Accesos rápidos</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {QUICK_ACTIONS.map((action) => (
            <Link
              key={action.to}
              to={action.to}
              className="bg-white rounded-xl border border-gray-200 p-5 flex flex-col gap-3 shadow-sm hover:shadow-md hover:border-primary-200 transition-all group"
            >
              <div className={`${action.bg} rounded-lg w-10 h-10 flex items-center justify-center group-hover:scale-110 transition-transform`}>
                {action.icon}
              </div>
              <div>
                <h3 className="font-semibold text-gray-800">{action.title}</h3>
                <p className="text-sm text-gray-500 mt-0.5">{action.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <InfoCard
          icon={<MapPin className="h-5 w-5 text-primary-600" />}
          title="Lugares únicos"
          description="Restaurantes, bares, parques, museos y más en Buenos Aires."
        />
        <InfoCard
          icon={<Calendar className="h-5 w-5 text-primary-600" />}
          title="Eventos en vivo"
          description="Conciertos, exposiciones y actividades que pasan hoy."
        />
        <InfoCard
          icon={<Sparkles className="h-5 w-5 text-primary-600" />}
          title="Motor de sugerencias"
          description="Recomendaciones basadas en clima, tus gustos y contexto."
        />
      </section>
    </div>
  )
}

function InfoCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-primary-50 rounded-xl p-5 flex flex-col gap-2">
      <div className="flex items-center gap-2">
        {icon}
        <h3 className="font-semibold text-primary-800 text-sm">{title}</h3>
      </div>
      <p className="text-sm text-primary-700">{description}</p>
    </div>
  )
}
