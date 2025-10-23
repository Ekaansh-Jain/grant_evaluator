import { useState, useEffect } from 'react';
import { Save } from 'lucide-react';
import { Card } from '../components/Card';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { evaluationService } from '../services/evaluationService';
import type { Settings as SettingsType } from '../types/evaluation';

export function Settings() {
  const [settings, setSettings] = useState<Partial<SettingsType>>({
    max_budget: 500000,
    chunk_size: 1000,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    setIsLoading(true);
    try {
      const data = await evaluationService.getSettings();
      if (data) {
        setSettings({
          max_budget: data.max_budget,
          chunk_size: data.chunk_size,
        });
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    setMessage(null);

    try {
      await evaluationService.updateSettings(settings);
      setMessage({ type: 'success', text: 'Settings saved successfully!' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to save settings. Please try again.' });
      console.error('Failed to save settings:', error);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-6 flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent-purple"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="space-y-2 animate-fade-in">
        <h1 className="text-4xl font-bold gradient-text">Settings</h1>
        <p className="text-gray-400">Configure evaluation parameters and system preferences</p>
      </div>

      <Card className="animate-slide-up">
        <div className="space-y-6">
          <div>
            <h2 className="text-2xl font-semibold text-gray-200 mb-4">Evaluation Parameters</h2>
            <div className="space-y-6">
              <Input
                type="number"
                label="Maximum Allowable Budget ($)"
                value={settings.max_budget || ''}
                onChange={(e) => setSettings({ ...settings, max_budget: Number(e.target.value) })}
                placeholder="500000"
              />

              <Input
                type="number"
                label="Document Chunk Size"
                value={settings.chunk_size || ''}
                onChange={(e) => setSettings({ ...settings, chunk_size: Number(e.target.value) })}
                placeholder="1000"
              />

              <div className="bg-charcoal-900 rounded-xl p-4 border border-charcoal-700">
                <h3 className="font-medium text-gray-300 mb-2">About These Settings</h3>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li>
                    <strong className="text-gray-300">Maximum Allowable Budget:</strong> Sets the budget threshold for flagging proposals that exceed this amount.
                  </li>
                  <li>
                    <strong className="text-gray-300">Document Chunk Size:</strong> Controls how the AI processes large documents. Larger chunks may provide more context but use more resources.
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {message && (
            <div
              className={`p-4 rounded-xl border ${
                message.type === 'success'
                  ? 'bg-success/10 border-success text-success'
                  : 'bg-error/10 border-error text-error'
              }`}
            >
              {message.text}
            </div>
          )}

          <div className="flex justify-end pt-4">
            <Button onClick={handleSave} isLoading={isSaving} className="flex items-center gap-2">
              <Save className="w-5 h-5" />
              Save Settings
            </Button>
          </div>
        </div>
      </Card>

      <Card className="animate-slide-up bg-gradient-dark">
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-gray-200">System Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-charcoal-800/50 rounded-xl">
              <p className="text-sm text-gray-400 mb-1">Version</p>
              <p className="text-lg font-semibold text-gray-200">1.0.0</p>
            </div>
            <div className="p-4 bg-charcoal-800/50 rounded-xl">
              <p className="text-sm text-gray-400 mb-1">Model</p>
              <p className="text-lg font-semibold text-gray-200">GPT-4 Turbo</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
