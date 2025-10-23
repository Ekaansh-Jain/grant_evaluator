import type { Evaluation, Settings } from '../types/evaluation';

// Backend API base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const evaluationService = {
  async saveEvaluation(file: File): Promise<Evaluation> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/evaluations`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to evaluate grant');
    }

    return await response.json();
  },

  async getEvaluations(): Promise<Evaluation[]> {
    const response = await fetch(`${API_BASE_URL}/evaluations`);

    if (!response.ok) {
      throw new Error('Failed to fetch evaluations');
    }

    return await response.json();
  },

  async getEvaluationById(id: string): Promise<Evaluation | null> {
    const response = await fetch(`${API_BASE_URL}/evaluations/${id}`);

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error('Failed to fetch evaluation');
    }

    return await response.json();
  },

  async getSettings(): Promise<Settings | null> {
    const response = await fetch(`${API_BASE_URL}/settings`);

    if (!response.ok) {
      throw new Error('Failed to fetch settings');
    }

    return await response.json();
  },

  async updateSettings(settings: Partial<Omit<Settings, 'id' | 'created_at' | 'updated_at'>>): Promise<Settings> {
    const response = await fetch(`${API_BASE_URL}/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settings),
    });

    if (!response.ok) {
      throw new Error('Failed to update settings');
    }

    return await response.json();
  },
};
