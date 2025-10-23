import { Link, useLocation } from 'react-router-dom';
import { Sparkles, Settings } from 'lucide-react';

export function Navbar() {
  const location = useLocation();

  return (
    <nav className="border-b border-charcoal-700 bg-charcoal-900/50 backdrop-blur-lg sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-primary flex items-center justify-center shadow-glow-purple group-hover:scale-110 transition-transform duration-300">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">AI Grant Evaluator</h1>
              <p className="text-xs text-gray-500">Intelligent Proposal Analysis</p>
            </div>
          </Link>

          <div className="flex items-center gap-4">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                location.pathname === '/'
                  ? 'text-accent-magenta'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              Evaluate
            </Link>
            <Link
              to="/settings"
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                location.pathname === '/settings'
                  ? 'text-accent-magenta'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              <Settings className="w-4 h-4" />
              Settings
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
