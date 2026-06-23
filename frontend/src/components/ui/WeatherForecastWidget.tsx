import { Cloud, Sun, CloudRain } from 'lucide-react'
import type { ForecastDay } from '@/types'

interface WeatherForecastWidgetProps {
  forecast: ForecastDay[] | undefined
  isLoading: boolean
  highlightDate?: string
}

const CONDITION_ICON: Record<string, React.ReactNode> = {
  Clear:        <Sun className="h-6 w-6 text-yellow-400" />,
  Clouds:       <Cloud className="h-6 w-6 text-gray-400" />,
  Rain:         <CloudRain className="h-6 w-6 text-blue-400" />,
  Drizzle:      <CloudRain className="h-6 w-6 text-blue-300" />,
  Thunderstorm: <CloudRain className="h-6 w-6 text-purple-500" />,
  Snow:         <Cloud className="h-6 w-6 text-blue-200" />,
}

function getIcon(condition: string) {
  return CONDITION_ICON[condition] ?? <Cloud className="h-6 w-6 text-gray-400" />
}

export default function WeatherForecastWidget({
  forecast,
  isLoading,
  highlightDate,
}: WeatherForecastWidgetProps) {
  if (isLoading) {
    return (
      <div className="flex gap-3 overflow-x-auto pb-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="flex-shrink-0 w-24 h-32 bg-gray-100 rounded-xl animate-pulse"
          />
        ))}
      </div>
    )
  }

  if (!forecast || forecast.length === 0) return null

  return (
    <div className="flex gap-3 overflow-x-auto pb-2">
      {forecast.map((day) => {
        const isHighlighted = highlightDate === day.date
        return (
          <div
            key={day.date}
            className={`flex-shrink-0 flex flex-col items-center gap-1 px-4 py-3 rounded-xl border transition-all ${
              isHighlighted
                ? 'bg-primary-500/10 border-primary-500/50 shadow-neon-sm'
                : 'bg-white border-gray-200'
            }`}
          >
            <span className={`text-xs font-semibold uppercase tracking-wide ${isHighlighted ? 'text-primary-600' : 'text-gray-500'}`}>
              {isHighlighted ? 'Hoy' : day.day_name.slice(0, 3)}
            </span>
            {getIcon(day.condition)}
            <div className="text-center">
              <span className="text-sm font-bold text-gray-900">{day.temp_max}°</span>
              <span className="text-xs text-gray-400 ml-1">{day.temp_min}°</span>
            </div>
            <span
              className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                day.is_outdoor_friendly
                  ? 'bg-green-500/15 text-green-400'
                  : 'bg-gray-300/10 text-gray-500'
              }`}
            >
              {day.is_outdoor_friendly ? 'Ideal' : 'Adentro'}
            </span>
          </div>
        )
      })}
    </div>
  )
}
