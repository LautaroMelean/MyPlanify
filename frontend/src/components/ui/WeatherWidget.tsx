import { Cloud, Sun, CloudRain, Wind, Droplets } from 'lucide-react'
import type { Weather } from '@/types'

interface WeatherWidgetProps {
  weather: Weather | null | undefined
}

const CONDITION_MAP: Record<string, { icon: React.ReactNode; label: string }> = {
  Clear:        { icon: <Sun className="h-5 w-5 text-yellow-400" />,  label: 'Despejado' },
  Clouds:       { icon: <Cloud className="h-5 w-5 text-gray-400" />,  label: 'Nublado' },
  Rain:         { icon: <CloudRain className="h-5 w-5 text-blue-400" />, label: 'Lluvia' },
  Drizzle:      { icon: <CloudRain className="h-5 w-5 text-blue-300" />, label: 'Llovizna' },
  Thunderstorm: { icon: <CloudRain className="h-5 w-5 text-purple-500" />, label: 'Tormenta' },
  Snow:         { icon: <Cloud className="h-5 w-5 text-blue-200" />,  label: 'Nieve' },
  Fog:          { icon: <Cloud className="h-5 w-5 text-gray-300" />,  label: 'Niebla' },
  Mist:         { icon: <Cloud className="h-5 w-5 text-gray-300" />,  label: 'Neblina' },
  Haze:         { icon: <Cloud className="h-5 w-5 text-gray-300" />,  label: 'Bruma' },
}

export default function WeatherWidget({ weather }: WeatherWidgetProps) {
  if (!weather) return null

  const { icon, label } = CONDITION_MAP[weather.condition] ?? {
    icon: <Cloud className="h-5 w-5 text-gray-400" />,
    label: weather.condition,
  }

  return (
    <div className="flex items-center gap-4 bg-white border border-gray-200 rounded-xl px-4 py-3 shadow-glass-sm w-fit">
      <div className="flex items-center gap-2">
        {icon}
        <span className="text-sm font-medium text-gray-600">{label}</span>
      </div>
      <div className="h-4 w-px bg-gray-200" />
      <span className="text-lg font-bold text-gray-900">{weather.temperature}°C</span>
      <span className="text-xs text-gray-400">Sensación {weather.feels_like}°C</span>
      <div className="h-4 w-px bg-gray-200" />
      <div className="flex items-center gap-1 text-xs text-gray-500">
        <Droplets className="h-3.5 w-3.5" />
        {weather.humidity}%
      </div>
      <div className="flex items-center gap-1 text-xs text-gray-500">
        <Wind className="h-3.5 w-3.5" />
        {weather.wind_speed} m/s
      </div>
    </div>
  )
}
