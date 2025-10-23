import type { Evaluation } from '../types/evaluation';

export function generateMockEvaluation(fileName: string, fileSize: number): Omit<Evaluation, 'id' | 'created_at' | 'updated_at'> {
  const overallScore = Math.random() * 3 + 7;
  const decision = overallScore >= 8.5 ? 'ACCEPT' : overallScore >= 7 ? 'REVISE' : 'REJECT';

  return {
    file_name: fileName,
    file_size: fileSize,
    decision,
    overall_score: Number(overallScore.toFixed(1)),
    scores: [
      {
        category: 'Scientific Merit',
        score: 8.5,
        maxScore: 10,
        strengths: [
          'Novel approach to solving a critical problem',
          'Strong theoretical foundation',
          'Clear research objectives'
        ],
        weaknesses: [
          'Limited discussion of alternative approaches',
          'Some methodology details need clarification'
        ]
      },
      {
        category: 'Innovation',
        score: 9.0,
        maxScore: 10,
        strengths: [
          'Groundbreaking methodology',
          'Unique interdisciplinary approach',
          'High potential for transformative impact'
        ],
        weaknesses: [
          'Risk assessment could be more comprehensive'
        ]
      },
      {
        category: 'Feasibility',
        score: 7.5,
        maxScore: 10,
        strengths: [
          'Realistic timeline',
          'Experienced team with relevant expertise'
        ],
        weaknesses: [
          'Resource allocation needs better justification',
          'Contingency plans are underdeveloped',
          'Some milestones are overly ambitious'
        ]
      },
      {
        category: 'Impact',
        score: 8.8,
        maxScore: 10,
        strengths: [
          'Clear societal benefits',
          'Strong dissemination plan',
          'Potential for broad application'
        ],
        weaknesses: [
          'Long-term sustainability plan could be stronger'
        ]
      },
      {
        category: 'Budget Justification',
        score: 7.0,
        maxScore: 10,
        strengths: [
          'Major expenses are explained',
          'Cost-sharing demonstrated'
        ],
        weaknesses: [
          'Some line items lack detailed justification',
          'Equipment costs seem high relative to other expenses',
          'Indirect costs need better explanation'
        ]
      }
    ],
    critique_domains: [
      { domain: 'Scientific Rigor', score: 8.5 },
      { domain: 'Innovation', score: 9.0 },
      { domain: 'Feasibility', score: 7.5 },
      { domain: 'Impact', score: 8.8 },
      { domain: 'Team Capability', score: 8.2 },
      { domain: 'Resource Planning', score: 7.3 },
      { domain: 'Sustainability', score: 7.8 }
    ],
    section_scores: [
      { section: 'Abstract', score: 8.5 },
      { section: 'Objectives', score: 9.0 },
      { section: 'Background', score: 8.3 },
      { section: 'Methodology', score: 8.0 },
      { section: 'Timeline', score: 7.5 },
      { section: 'Team', score: 8.8 },
      { section: 'Budget', score: 7.0 },
      { section: 'Impact', score: 8.9 },
      { section: 'Dissemination', score: 8.4 },
      { section: 'References', score: 8.7 }
    ],
    full_critique: {
      summary: 'This grant proposal demonstrates strong scientific merit and innovation with a novel approach to addressing a critical research gap. The research objectives are clearly defined, and the methodology shows promise for generating significant insights. However, several areas require attention to strengthen the application.',
      issues: [
        {
          severity: 'high',
          category: 'Budget',
          description: 'Equipment costs ($125,000) represent 25% of the total budget but lack detailed justification for specific items and their necessity.'
        },
        {
          severity: 'high',
          category: 'Methodology',
          description: 'Statistical power analysis is missing for the proposed sample size. This is critical for demonstrating feasibility of detecting expected effects.'
        },
        {
          severity: 'medium',
          category: 'Timeline',
          description: 'Milestone 3 (data collection and analysis in 6 months) appears overly ambitious given the proposed sample size and complexity.'
        },
        {
          severity: 'medium',
          category: 'Risk Management',
          description: 'Contingency plans are mentioned but not detailed. What specific actions will be taken if recruitment falls short or equipment fails?'
        },
        {
          severity: 'low',
          category: 'References',
          description: 'Several key recent publications (2023-2024) in the field are not cited, suggesting the literature review may not be fully current.'
        },
        {
          severity: 'low',
          category: 'Dissemination',
          description: 'Open access publication strategy is mentioned but specific journals or repositories are not identified.'
        }
      ],
      recommendations: [
        {
          priority: 'high',
          recommendation: 'Provide itemized equipment list with vendor quotes and detailed justification for each item explaining its necessity for the proposed research.'
        },
        {
          priority: 'high',
          recommendation: 'Include statistical power analysis showing that proposed sample size is adequate to detect effects of the anticipated magnitude with 80% power.'
        },
        {
          priority: 'high',
          recommendation: 'Revise timeline for Milestone 3 to allow 9-10 months for data collection and analysis, or provide strong justification for compressed timeline.'
        },
        {
          priority: 'medium',
          recommendation: 'Develop detailed contingency plans with specific trigger points and alternative strategies for common research challenges.'
        },
        {
          priority: 'medium',
          recommendation: 'Expand the literature review to include recent 2023-2024 publications that demonstrate current state of the field.'
        },
        {
          priority: 'low',
          recommendation: 'Specify target journals for publication and data repositories for sharing results to strengthen open science commitment.'
        },
        {
          priority: 'low',
          recommendation: 'Consider adding quarterly progress reports to the dissemination plan to maintain stakeholder engagement throughout the project.'
        }
      ]
    },
    budget_analysis: {
      totalBudget: 485750,
      breakdown: [
        { category: 'Personnel', amount: 245000, percentage: 50.4 },
        { category: 'Equipment', amount: 125000, percentage: 25.7 },
        { category: 'Supplies', amount: 45000, percentage: 9.3 },
        { category: 'Travel', amount: 28000, percentage: 5.8 },
        { category: 'Publication Costs', amount: 12750, percentage: 2.6 },
        { category: 'Other Direct Costs', amount: 30000, percentage: 6.2 }
      ],
      flags: [
        {
          type: 'warning',
          message: 'Equipment costs (25.7%) are higher than typical NIH averages (15-20%). Ensure detailed justification is provided.'
        },
        {
          type: 'info',
          message: 'Personnel costs (50.4%) are within acceptable range for research projects.'
        },
        {
          type: 'warning',
          message: 'Total budget ($485,750) is approaching the maximum allowed ($500,000). Consider if any costs can be optimized.'
        }
      ],
      summary: 'The budget is generally well-structured with personnel costs at an appropriate level. However, equipment costs require additional justification. Travel and publication budgets appear reasonable. Total budget utilizes 97% of available funding.'
    }
  };
}

export async function simulateEvaluation(fileName: string, fileSize: number): Promise<Omit<Evaluation, 'id' | 'created_at' | 'updated_at'>> {
  await new Promise(resolve => setTimeout(resolve, 4000));
  return generateMockEvaluation(fileName, fileSize);
}
