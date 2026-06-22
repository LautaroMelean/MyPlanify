import { Component, type ReactNode } from 'react'
import { AlertTriangle, RotateCcw } from 'lucide-react'

interface Props { children: ReactNode }
interface State { hasError: boolean; message: string }

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, message: '' }

  static getDerivedStateFromError(err: Error): State {
    return { hasError: true, message: err.message }
  }

  componentDidCatch(err: Error, info: { componentStack: string }) {
    console.error('[ErrorBoundary]', err, info.componentStack)
  }

  render() {
    if (!this.state.hasError) return this.props.children

    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-red-500/10 rounded-2xl border border-red-500/20">
              <AlertTriangle className="h-12 w-12 text-red-400" aria-hidden="true" />
            </div>
          </div>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Algo salió mal</h1>
          <p className="text-sm text-gray-500 mb-6">
            Ocurrió un error inesperado. Podés intentar recargar la página.
          </p>
          {import.meta.env.DEV && this.state.message && (
            <p className="text-xs text-gray-400 font-mono bg-gray-100 rounded-lg px-3 py-2 mb-6 text-left break-all">
              {this.state.message}
            </p>
          )}
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 text-white rounded-xl text-sm font-medium hover:bg-primary-700 shadow-neon-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40"
          >
            <RotateCcw className="h-4 w-4" aria-hidden="true" />
            Recargar página
          </button>
        </div>
      </div>
    )
  }
}
