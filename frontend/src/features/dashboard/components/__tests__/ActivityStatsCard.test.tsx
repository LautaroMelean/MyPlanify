import { screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import { ActivityStatsCard } from '../ActivityStatsCard'
import type { UserActivityStats } from '@/types'

const makeStats = (overrides: Partial<UserActivityStats> = {}): UserActivityStats => ({
  plans_completed: 5,
  places_visited: 12,
  cities_explored: 3,
  favorite_category: 'gastronomía',
  current_streak_weeks: 2,
  best_streak_weeks: 4,
  total_plans: 10,
  avg_rating_given: 4.2,
  ...overrides,
})

describe('ActivityStatsCard', () => {
  it('shows plans completed', () => {
    renderWithProviders(<ActivityStatsCard stats={makeStats()} />)
    expect(screen.getByText('5')).toBeInTheDocument()
    expect(screen.getByText(/planes completados/i)).toBeInTheDocument()
  })

  it('shows cities explored', () => {
    renderWithProviders(<ActivityStatsCard stats={makeStats()} />)
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText(/ciudades exploradas/i)).toBeInTheDocument()
  })

  it('shows current streak', () => {
    renderWithProviders(<ActivityStatsCard stats={makeStats({ current_streak_weeks: 3 })} />)
    expect(screen.getByText(/3 sem. seguidas/i)).toBeInTheDocument()
  })

  it('shows empty state when all values are zero', () => {
    renderWithProviders(
      <ActivityStatsCard
        stats={makeStats({
          plans_completed: 0,
          places_visited: 0,
          cities_explored: 0,
          current_streak_weeks: 0,
        })}
      />
    )
    expect(screen.getByText(/sin actividad aún/i)).toBeInTheDocument()
  })

  it('shows favorite category when present', () => {
    renderWithProviders(<ActivityStatsCard stats={makeStats({ favorite_category: 'cine' })} />)
    expect(screen.getByText(/favorita: cine/i)).toBeInTheDocument()
  })

  it('does not show streak badge when streak is zero', () => {
    renderWithProviders(
      <ActivityStatsCard stats={makeStats({ current_streak_weeks: 0, plans_completed: 3, places_visited: 1, cities_explored: 1 })} />
    )
    expect(screen.queryByText(/sem. seguidas/i)).not.toBeInTheDocument()
  })
})
