import { render, screen } from '@testing-library/react'
import WeatherWidget from '../WeatherWidget'
import type { Weather } from '@/types'

const mockWeather: Weather = {
  temperature: 22,
  feels_like: 20,
  condition: 'Clear',
  humidity: 55,
  wind_speed: 4.2,
  clouds: 10,
  is_outdoor_friendly: true,
}

describe('WeatherWidget', () => {
  it('renders weather data correctly', () => {
    render(<WeatherWidget weather={mockWeather} />)
    expect(screen.getByText('22°C')).toBeInTheDocument()
    expect(screen.getByText('Sensación 20°C')).toBeInTheDocument()
    expect(screen.getByText('Despejado')).toBeInTheDocument()
    expect(screen.getByText('55%')).toBeInTheDocument()
    expect(screen.getByText('4.2 m/s')).toBeInTheDocument()
  })

  it('does not render when weather is null', () => {
    const { container } = render(<WeatherWidget weather={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('does not render when weather is undefined', () => {
    const { container } = render(<WeatherWidget weather={undefined} />)
    expect(container.firstChild).toBeNull()
  })

  it('renders rain condition correctly', () => {
    render(<WeatherWidget weather={{ ...mockWeather, condition: 'Rain', is_outdoor_friendly: false }} />)
    expect(screen.getByText('Lluvia')).toBeInTheDocument()
  })

  it('renders unknown condition with fallback label', () => {
    render(<WeatherWidget weather={{ ...mockWeather, condition: 'Ash' }} />)
    expect(screen.getByText('Ash')).toBeInTheDocument()
  })
})
