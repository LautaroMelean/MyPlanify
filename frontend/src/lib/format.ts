/** "$5.000" or "Gratis" when val === 0 */
export function formatARS(val: string | number | null | undefined): string {
  if (val == null) return '—'
  const n = parseFloat(String(val))
  if (isNaN(n)) return '—'
  if (n === 0) return 'Gratis'
  return `$${Math.round(n).toLocaleString('es-AR')}`
}

/** "15 ene 2026" */
export function formatDateShort(iso: string): string {
  return new Date(iso).toLocaleDateString('es-AR', {
    day: 'numeric', month: 'short', year: 'numeric',
  })
}

/** Local date as "YYYY-MM-DD" — avoids UTC offset from toISOString() */
export function localDateString(d = new Date()): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/** Local datetime as "YYYY-MM-DDTHH:MM" for datetime-local inputs */
export function localDateTimeString(d = new Date()): string {
  return `${localDateString(d)}T${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
