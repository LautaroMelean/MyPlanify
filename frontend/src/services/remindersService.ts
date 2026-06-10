import apiClient from '@/lib/axios'
import type { ApiResponse, Reminder } from '@/types'

export const remindersService = {
  async list(): Promise<Reminder[]> {
    const { data } = await apiClient.get<ApiResponse<Reminder[]>>('/reminders/')
    return data.data
  },

  async create(eventId: string, reminderDate: string): Promise<Reminder> {
    const { data } = await apiClient.post<ApiResponse<Reminder>>('/reminders/', {
      event: eventId,
      reminder_date: reminderDate,
    })
    return data.data
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`/reminders/${id}/`)
  },
}
