import { useEffect, useState } from 'react';
import { Sparkles, FileSearch, BarChart3, CheckCircle2 } from 'lucide-react';

const stages = [
  { icon: FileSearch, label: 'Analyzing Document', duration: 1000 },
  { icon: Sparkles, label: 'Generating Insights', duration: 1200 },
  { icon: BarChart3, label: 'Computing Scores', duration: 1000 },
  { icon: CheckCircle2, label: 'Finalizing Evaluation', duration: 800 }
];

export function LoadingAnimation() {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    if (currentStage >= stages.length) return;

    const timer = setTimeout(() => {
      setCurrentStage(prev => prev + 1);
    }, stages[currentStage].duration);

    return () => clearTimeout(timer);
  }, [currentStage]);

  return (
    <div className="fixed inset-0 bg-navy-900/95 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="max-w-md w-full mx-4">
        <div className="card-premium p-8">
          <div className="flex flex-col items-center gap-6">
            <div className="relative">
              <div className="w-24 h-24 rounded-full bg-gradient-primary opacity-20 animate-pulse-slow"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                {stages.map((stage, index) => {
                  const Icon = stage.icon;
                  return (
                    <Icon
                      key={index}
                      className={`absolute w-12 h-12 transition-all duration-500 ${
                        index === currentStage
                          ? 'text-accent-magenta scale-100 opacity-100'
                          : index < currentStage
                          ? 'text-success scale-75 opacity-0'
                          : 'text-gray-600 scale-75 opacity-0'
                      }`}
                    />
                  );
                })}
              </div>
            </div>

            <div className="w-full space-y-3">
              {stages.map((stage, index) => (
                <div key={index} className="flex items-center gap-3">
                  <div
                    className={`w-3 h-3 rounded-full transition-all duration-300 ${
                      index < currentStage
                        ? 'bg-success shadow-glow-green'
                        : index === currentStage
                        ? 'bg-accent-magenta shadow-glow-pink animate-pulse'
                        : 'bg-charcoal-700'
                    }`}
                  />
                  <span
                    className={`text-sm transition-colors duration-300 ${
                      index <= currentStage ? 'text-gray-200 font-medium' : 'text-gray-500'
                    }`}
                  >
                    {stage.label}
                  </span>
                </div>
              ))}
            </div>

            <div className="w-full bg-charcoal-700 rounded-full h-2 overflow-hidden">
              <div
                className="h-full bg-gradient-primary transition-all duration-500 ease-out"
                style={{
                  width: `${((currentStage + 1) / stages.length) * 100}%`
                }}
              />
            </div>

            <p className="text-gray-400 text-sm text-center">
              Processing your grant application...
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
