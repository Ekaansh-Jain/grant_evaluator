import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Download, CheckCircle, XCircle, AlertCircle, TrendingUp, TrendingDown, Check, X, AlertTriangle, DollarSign } from 'lucide-react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Tabs } from '../components/Tabs';
import { RadarChartComponent } from '../components/charts/RadarChart';
import { BarChartComponent } from '../components/charts/BarChart';
import { evaluationService } from '../services/evaluationService';
import type { Evaluation } from '../types/evaluation';

export function Results() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!id) {
      navigate('/');
      return;
    }

    loadEvaluation(id);
  }, [id, navigate]);

  const loadEvaluation = async (evaluationId: string) => {
    try {
      const data = await evaluationService.getEvaluationById(evaluationId);
      if (!data) {
        navigate('/');
        return;
      }
      setEvaluation(data);
    } catch (error) {
      console.error('Failed to load evaluation:', error);
      navigate('/');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!id) return;
    
    // Create download URL
    const downloadUrl = `http://localhost:8000/api/evaluations/${id}/download`;
    
    // Open in new window to trigger download
    window.open(downloadUrl, '_blank');
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto p-6 flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent-purple"></div>
      </div>
    );
  }

  if (!evaluation) {
    return null;
  }

  const DecisionBadge = () => {
    const config = {
      ACCEPT: { icon: CheckCircle, color: 'text-success', bg: 'bg-success/20', border: 'border-success', shadow: 'shadow-glow-green' },
      REJECT: { icon: XCircle, color: 'text-error', bg: 'bg-error/20', border: 'border-error', shadow: 'shadow-glow-red' },
      REVISE: { icon: AlertCircle, color: 'text-warning', bg: 'bg-warning/20', border: 'border-warning', shadow: 'shadow-glow-purple' },
      'CONDITIONALLY ACCEPT': { icon: CheckCircle, color: 'text-accent-cyan', bg: 'bg-accent-cyan/20', border: 'border-accent-cyan', shadow: 'shadow-glow-cyan' },
    };

    const { icon: Icon, color, bg, border, shadow } = config[evaluation.decision];

    return (
      <div className={`inline-flex items-center gap-2 px-6 py-3 rounded-xl ${bg} ${border} border-2 ${shadow}`}>
        <Icon className={`w-6 h-6 ${color}`} />
        <span className={`text-xl font-bold ${color}`}>{evaluation.decision}</span>
      </div>
    );
  };

  const tabs = [
    {
      id: 'visual',
      label: 'Visual Dashboard',
      content: (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <h3 className="text-xl font-semibold text-gray-200 mb-4">Critique Domains</h3>
            <RadarChartComponent data={evaluation.critique_domains} />
          </Card>
          <Card>
            <h3 className="text-xl font-semibold text-gray-200 mb-4">Section Scores</h3>
            <BarChartComponent data={evaluation.section_scores} />
          </Card>
        </div>
      ),
    },
    {
      id: 'detailed',
      label: 'Detailed Scoring',
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {evaluation.scores.map((score, index) => (
            <Card key={index} hover>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-gray-200">{score.category}</h3>
                  <div className="text-2xl font-bold gradient-text">
                    {score.score}/{score.maxScore}
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp className="w-4 h-4 text-success" />
                      <span className="font-medium text-success text-sm">Strengths</span>
                    </div>
                    <ul className="space-y-1">
                      {score.strengths.map((strength, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                          <Check className="w-4 h-4 text-success mt-0.5 flex-shrink-0" />
                          <span>{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingDown className="w-4 h-4 text-warning" />
                      <span className="font-medium text-warning text-sm">Weaknesses</span>
                    </div>
                    <ul className="space-y-1">
                      {score.weaknesses.map((weakness, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                          <X className="w-4 h-4 text-warning mt-0.5 flex-shrink-0" />
                          <span>{weakness}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ),
    },
    {
      id: 'critique',
      label: 'Full Critique',
      content: (
        <Card>
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-semibold text-gray-200 mb-4">Summary</h3>
              <p className="text-gray-300 leading-relaxed">{evaluation.full_critique.summary}</p>
            </div>

            <div>
              <h3 className="text-2xl font-semibold text-gray-200 mb-4">Issues Identified</h3>
              <div className="space-y-3">
                {evaluation.full_critique.issues.map((issue, index) => {
                  const severityConfig = {
                    high: { color: 'text-error', bg: 'bg-error/20', border: 'border-error' },
                    medium: { color: 'text-warning', bg: 'bg-warning/20', border: 'border-warning' },
                    low: { color: 'text-blue-400', bg: 'bg-blue-400/20', border: 'border-blue-400' },
                  };
                  const config = severityConfig[issue.severity];

                  return (
                    <div key={index} className={`p-4 rounded-xl ${config.bg} border ${config.border}`}>
                      <div className="flex items-start gap-3">
                        <AlertTriangle className={`w-5 h-5 ${config.color} mt-0.5 flex-shrink-0`} />
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className={`text-xs font-semibold uppercase ${config.color}`}>
                              {issue.severity}
                            </span>
                            <span className="text-xs text-gray-400">•</span>
                            <span className="text-sm font-medium text-gray-300">{issue.category}</span>
                          </div>
                          <p className="text-sm text-gray-300">{issue.description}</p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-semibold text-gray-200 mb-4">Recommendations</h3>
              <div className="space-y-3">
                {evaluation.full_critique.recommendations.map((rec, index) => {
                  const priorityConfig = {
                    high: { color: 'text-accent-magenta', icon: '!' },
                    medium: { color: 'text-accent-purple', icon: '•' },
                    low: { color: 'text-gray-400', icon: '·' },
                  };
                  const config = priorityConfig[rec.priority];

                  return (
                    <div key={index} className="flex items-start gap-3 p-4 bg-charcoal-900 rounded-xl">
                      <span className={`text-xl font-bold ${config.color}`}>{config.icon}</span>
                      <div className="flex-1">
                        <span className={`text-xs font-semibold uppercase ${config.color} mb-1 block`}>
                          {rec.priority} Priority
                        </span>
                        <p className="text-sm text-gray-300">{rec.recommendation}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </Card>
      ),
    },
    {
      id: 'budget',
      label: 'Budget Analysis',
      content: (
        <div className="space-y-6">
          <Card>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-semibold text-gray-200">Budget Overview</h3>
              <div className="text-right">
                <p className="text-sm text-gray-400">Total Budget</p>
                <p className="text-3xl font-bold gradient-text">
                  ${evaluation.budget_analysis.totalBudget.toLocaleString()}
                </p>
              </div>
            </div>

            <div className="space-y-3">
              {evaluation.budget_analysis.breakdown.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-300">{item.category}</span>
                    <div className="flex items-center gap-3">
                      <span className="text-gray-400">{item.percentage}%</span>
                      <span className="font-semibold text-gray-200">
                        ${item.amount.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  <div className="w-full bg-charcoal-700 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-full bg-gradient-primary transition-all duration-500"
                      style={{ width: `${item.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <h3 className="text-2xl font-semibold text-gray-200 mb-4">Budget Flags</h3>
            <div className="space-y-3">
              {evaluation.budget_analysis.flags.map((flag, index) => {
                const flagConfig = {
                  warning: { icon: AlertTriangle, color: 'text-warning', bg: 'bg-warning/20', border: 'border-warning' },
                  error: { icon: XCircle, color: 'text-error', bg: 'bg-error/20', border: 'border-error' },
                  info: { icon: DollarSign, color: 'text-blue-400', bg: 'bg-blue-400/20', border: 'border-blue-400' },
                };
                const config = flagConfig[flag.type];
                const Icon = config.icon;

                return (
                  <div key={index} className={`flex items-start gap-3 p-4 rounded-xl ${config.bg} border ${config.border}`}>
                    <Icon className={`w-5 h-5 ${config.color} mt-0.5 flex-shrink-0`} />
                    <p className="text-sm text-gray-300">{flag.message}</p>
                  </div>
                );
              })}
            </div>
          </Card>

          <Card>
            <h3 className="text-2xl font-semibold text-gray-200 mb-4">Summary</h3>
            <p className="text-gray-300 leading-relaxed">{evaluation.budget_analysis.summary}</p>
          </Card>
        </div>
      ),
    },
  ];

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6 animate-fade-in">
      <Card className="bg-gradient-dark">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <DecisionBadge />
              <div className="text-5xl font-bold gradient-text">
                {evaluation.overall_score}/10
              </div>
            </div>
            <div>
              <p className="text-sm text-gray-400">File: {evaluation.file_name}</p>
              <p className="text-sm text-gray-400">
                Evaluated: {new Date(evaluation.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <Button onClick={handleDownloadPDF} className="flex items-center gap-2">
            <Download className="w-5 h-5" />
            Download PDF Report
          </Button>
        </div>
      </Card>

      <Tabs tabs={tabs} defaultTab="visual" />
    </div>
  );
}
