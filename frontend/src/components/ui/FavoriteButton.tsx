import { Heart } from 'lucide-react'
import { useFavorites, useAddFavorite, useRemoveFavorite } from '@/hooks/useFavorites'

interface FavoriteButtonProps {
  itemId: string
  itemType: 'event' | 'place' | 'activity'
  className?: string
}

export default function FavoriteButton({ itemId, itemType, className = '' }: FavoriteButtonProps) {
  const { data: favorites = [] } = useFavorites()
  const add = useAddFavorite()
  const remove = useRemoveFavorite()

  const existing = favorites.find((f) => {
    if (itemType === 'event') return f.event === itemId
    if (itemType === 'place') return f.place === itemId
    return f.activity === itemId
  })

  const isFavorite = !!existing
  const isLoading = add.isPending || remove.isPending

  const toggle = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (isFavorite && existing) {
      remove.mutate(existing.id)
    } else {
      add.mutate({
        event: itemType === 'event' ? itemId : null,
        place: itemType === 'place' ? itemId : null,
        activity: itemType === 'activity' ? itemId : null,
      })
    }
  }

  return (
    <button
      onClick={toggle}
      disabled={isLoading}
      aria-label={isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'}
      className={`p-1.5 rounded-full hover:bg-gray-100 transition-colors disabled:opacity-50 flex-shrink-0 ${className}`}
    >
      <Heart
        className={`h-5 w-5 transition-colors ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-400'}`}
      />
    </button>
  )
}
