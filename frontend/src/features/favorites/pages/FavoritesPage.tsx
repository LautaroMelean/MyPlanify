import { Heart, Trash2 } from 'lucide-react'
import { useFavorites, useRemoveFavorite } from '@/hooks/useFavorites'
import Loading from '@/components/common/Loading'
import EmptyState from '@/components/common/EmptyState'

export default function FavoritesPage() {
  const { data: favorites = [], isLoading } = useFavorites()
  const remove = useRemoveFavorite()

  const typeLabels = {
    event: 'Evento',
    place: 'Lugar',
    activity: 'Actividad',
    null: '',
  }

  if (isLoading) return <Loading message="Cargando favoritos..." />

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Mis favoritos</h1>
        <p className="text-gray-500 text-sm">Todo lo que guardaste para volver a ver.</p>
      </div>

      {favorites.length === 0 ? (
        <EmptyState
          title="Sin favoritos aún"
          description="Explorá lugares, actividades y eventos, y tocá el corazón para guardarlos acá."
          icon={<Heart className="h-12 w-12 text-gray-300" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {favorites.map((fav) => (
            <div
              key={fav.id}
              className="bg-white rounded-xl border border-gray-200 shadow-sm p-4 flex items-center justify-between gap-3"
            >
              <div className="min-w-0">
                <p className="font-medium text-gray-900 truncate">{fav.item_name ?? '—'}</p>
                <span className="text-xs text-gray-500">
                  {fav.item_type ? typeLabels[fav.item_type] : ''}
                </span>
              </div>
              <button
                onClick={() => remove.mutate(fav.id)}
                disabled={remove.isPending}
                className="text-gray-400 hover:text-red-500 transition-colors p-1.5 rounded-full hover:bg-red-50 flex-shrink-0"
                aria-label="Eliminar favorito"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
