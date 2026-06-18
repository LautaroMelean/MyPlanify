import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { MapPin, LogOut, Compass, Heart, Sparkles, Map, Settings, Menu, X, Bell, Search, CalendarDays, LayoutDashboard, Clock, FolderOpen } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { useLogout } from '@/hooks/useAuth'
import { useUnreadCount } from '@/hooks/useNotifications'
import Avatar from '@/components/ui/Avatar'
import Button from '@/components/ui/Button'
import type { UserRole } from '@/types'

const NAV_LINKS = [
  { to: '/planner',         label: 'Planner',         icon: <CalendarDays className="h-4 w-4" /> },
  { to: '/recomendaciones', label: 'Para vos',        icon: <Sparkles className="h-4 w-4" /> },
  { to: '/explorar',        label: 'Explorar',        icon: <Compass className="h-4 w-4" /> },
  { to: '/mapa',            label: 'Mapa',            icon: <Map className="h-4 w-4" /> },
  { to: '/favoritos',       label: 'Favoritos',       icon: <Heart className="h-4 w-4" /> },
]

function getDashboardLink(role: UserRole | undefined) {
  if (role === 'business_owner' || role === 'admin' || role === 'moderator') {
    return { to: '/dashboard/business', label: 'Mi Negocio', icon: <LayoutDashboard className="h-4 w-4" /> }
  }
  if (role === 'event_organizer') {
    return { to: '/dashboard/organizer', label: 'Mis Eventos', icon: <LayoutDashboard className="h-4 w-4" /> }
  }
  return null
}

export default function Navbar() {
  const { user, isAuthenticated } = useAuthStore()
  const logout = useLogout()
  const navigate = useNavigate()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const unreadCount = useUnreadCount()
  const dashboardLink = getDashboardLink(user?.role)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const q = searchQuery.trim()
    if (q) {
      navigate(`/search?q=${encodeURIComponent(q)}`)
      setSearchQuery('')
    }
  }

  const isActive = (to: string) => location.pathname === to || (to !== '/' && location.pathname.startsWith(to))

  return (
    <header className="sticky top-0 z-30 glass-nav">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* Logo + desktop nav */}
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl flex-shrink-0 neon-text">
            <MapPin className="h-6 w-6 text-primary-600" />
            Planify
          </Link>

          {isAuthenticated && (
            <nav className="hidden md:flex items-center gap-1">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                    isActive(link.to)
                      ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm'
                      : 'text-gray-600 hover:text-gray-800 hover:bg-white/5'
                  }`}
                >
                  {link.icon}
                  {link.label}
                </Link>
              ))}
              {dashboardLink && (
                <Link
                  to={dashboardLink.to}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                    isActive(dashboardLink.to)
                      ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm'
                      : 'text-gray-600 hover:text-gray-800 hover:bg-white/5'
                  }`}
                >
                  {dashboardLink.icon}
                  {dashboardLink.label}
                </Link>
              )}
            </nav>
          )}
        </div>

        {/* Search bar */}
        <form onSubmit={handleSearch} className="hidden md:flex items-center">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar lugares, eventos..."
              className="pl-9 pr-4 py-1.5 text-sm border border-white/10 rounded-lg bg-white/5 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary-500/50 focus:border-primary-500/30 focus:bg-white/8 w-56 transition-all"
            />
          </div>
        </form>

        {/* Desktop right */}
        <nav className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <Link
                to="/notificaciones"
                className={`hidden sm:flex relative p-1.5 rounded-lg transition-all ${isActive('/notificaciones') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-500 hover:text-gray-700 hover:bg-white/5'}`}
                aria-label="Notificaciones"
              >
                <Bell className="h-5 w-5" />
                {unreadCount > 0 && (
                  <span className="absolute -top-0.5 -right-0.5 bg-primary-500 text-white text-[10px] font-bold rounded-full min-w-[16px] h-4 flex items-center justify-center px-0.5">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </Link>
              <Link
                to="/configuracion"
                className={`hidden sm:flex p-1.5 rounded-lg transition-all ${isActive('/configuracion') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-500 hover:text-gray-700 hover:bg-white/5'}`}
                aria-label="Configuración"
              >
                <Settings className="h-5 w-5" />
              </Link>
              <button
                onClick={() => navigate('/perfil')}
                className="flex items-center gap-2 hover:text-primary-600 text-sm text-gray-600 transition-colors"
              >
                <Avatar name={user?.full_name} size="sm" src={user?.profile_image || undefined} />
                <span className="hidden sm:inline">{user?.first_name}</span>
              </button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => logout.mutate()}
                isLoading={logout.isPending}
                leftIcon={<LogOut className="h-4 w-4" />}
                className="hidden sm:flex"
              >
                Salir
              </Button>
              {/* Mobile hamburger */}
              <button
                className="md:hidden p-1.5 rounded-lg text-gray-500 hover:bg-white/5 transition-colors"
                onClick={() => setMobileOpen(!mobileOpen)}
                aria-label="Menú"
              >
                {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm text-gray-600 hover:text-primary-600 font-medium transition-colors">
                Ingresar
              </Link>
              <Button size="sm" onClick={() => navigate('/register')}>
                Registrarse
              </Button>
            </>
          )}
        </nav>
      </div>

      {/* Mobile menu */}
      {isAuthenticated && mobileOpen && (
        <div className="md:hidden border-t border-white/5 px-4 py-3 flex flex-col gap-1" style={{ background: 'rgba(7,6,15,0.95)', backdropFilter: 'blur(20px)' }}>
          {NAV_LINKS.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive(link.to) ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
              }`}
            >
              {link.icon}
              {link.label}
            </Link>
          ))}
          {dashboardLink && (
            <Link
              to={dashboardLink.to}
              onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive(dashboardLink.to) ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
              }`}
            >
              {dashboardLink.icon}
              {dashboardLink.label}
            </Link>
          )}
          <Link
            to="/notificaciones"
            onClick={() => setMobileOpen(false)}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive('/notificaciones') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
            }`}
          >
            <Bell className="h-4 w-4" />
            Notificaciones
            {unreadCount > 0 && (
              <span className="ml-auto bg-primary-500/20 text-primary-600 text-xs font-bold px-1.5 py-0.5 rounded-full">
                {unreadCount > 9 ? '9+' : unreadCount}
              </span>
            )}
          </Link>
          <Link
            to="/mis-planes"
            onClick={() => setMobileOpen(false)}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive('/mis-planes') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
            }`}
          >
            <FolderOpen className="h-4 w-4" />
            Mis Planes
          </Link>
          <Link
            to="/recordatorios"
            onClick={() => setMobileOpen(false)}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive('/recordatorios') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
            }`}
          >
            <Clock className="h-4 w-4" />
            Recordatorios
          </Link>
          <Link
            to="/configuracion"
            onClick={() => setMobileOpen(false)}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive('/configuracion') ? 'text-primary-600 bg-primary-500/10 shadow-neon-sm' : 'text-gray-600 hover:bg-white/5'
            }`}
          >
            <Settings className="h-4 w-4" />
            Configuración
          </Link>
          <button
            onClick={() => { logout.mutate(); setMobileOpen(false) }}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10 transition-colors"
          >
            <LogOut className="h-4 w-4" />
            Cerrar sesión
          </button>
        </div>
      )}
    </header>
  )
}
