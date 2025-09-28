import unittest
import json
from src.agents.scoring import (
    run_scorer,
    calculate_research_impact,
    calculate_methodology_score,
    calculate_innovation_score,
    calculate_feasibility_score,
    calculate_budget_score
)

class TestScoring(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.sample_summary = {
            "Objectives": {
                "text": "This research aims to develop a novel approach for quantum computing optimization using machine learning techniques. The project will advance the field of quantum algorithms.",
                "pages": [1, 2],
                "references": ["page 1: intro", "page 2: objectives"],
                "notes": "Clear objectives with good potential impact"
            },
            "Methodology": {
                "text": "We will use controlled experiments with replicated trials to validate our approach. The methodology includes detailed measurement protocols and statistical analysis frameworks.",
                "pages": [3, 4],
                "references": ["page 3-4: methods"],
                "notes": "Well-structured methodology"
            },
            "ExpectedOutcomes": {
                "text": "The project will significantly improve quantum computing efficiency and create breakthrough algorithms with wide-ranging impact across multiple domains.",
                "pages": [5],
                "references": ["page 5: outcomes"],
                "notes": "Strong potential outcomes"
            },
            "Innovation": {
                "text": "This is a unique and novel approach that goes beyond existing quantum computing paradigms. The innovative methodology represents a breakthrough in the field.",
                "pages": [2],
                "references": ["page 2: innovation"],
                "notes": "Highly innovative"
            },
            "Feasibility": {
                "text": "Our team has the required expertise and resources. The timeline is well-planned with clear milestones. The facility is equipped with necessary quantum computing equipment.",
                "pages": [6],
                "references": ["page 6: feasibility"],
                "notes": "Feasible with available resources"
            }
        }
        
        self.minimal_summary = {
            "Objectives": {"text": "Basic research objective"},
            "Methodology": {"text": "Simple method description"},
            "ExpectedOutcomes": {"text": "Expected results"},
            "Innovation": {"text": "New approach"},
            "Feasibility": {"text": "Can be done"}
        }
        
        self.empty_summary = {}

    def test_research_impact_calculation(self):
        """Test research impact scoring"""
        score, feedback = calculate_research_impact(self.sample_summary)
        self.assertLessEqual(score, 25)
        self.assertGreater(score, 0)
        self.assertTrue(isinstance(feedback, str))
        
        # Test with minimal content
        score_min, feedback_min = calculate_research_impact(self.minimal_summary)
        self.assertLessEqual(score_min, score)
        
        # Test with empty content
        score_empty, feedback_empty = calculate_research_impact(self.empty_summary)
        self.assertEqual(score_empty, 0)

    def test_methodology_score_calculation(self):
        """Test methodology scoring"""
        score, feedback = calculate_methodology_score(self.sample_summary)
        self.assertLessEqual(score, 25)
        self.assertGreater(score, 0)
        self.assertTrue(isinstance(feedback, str))
        
        # Test with minimal content
        score_min, _ = calculate_methodology_score(self.minimal_summary)
        self.assertLessEqual(score_min, score)

    def test_innovation_score_calculation(self):
        """Test innovation scoring"""
        score, feedback = calculate_innovation_score(self.sample_summary)
        self.assertLessEqual(score, 20)
        self.assertGreater(score, 0)
        self.assertTrue(isinstance(feedback, str))
        
        # Test empty content
        score_empty, _ = calculate_innovation_score(self.empty_summary)
        self.assertEqual(score_empty, 0)

    def test_feasibility_score_calculation(self):
        """Test feasibility scoring"""
        score, feedback = calculate_feasibility_score(self.sample_summary)
        self.assertLessEqual(score, 20)
        self.assertGreater(score, 0)
        self.assertTrue(isinstance(feedback, str))

    def test_budget_score_calculation(self):
        """Test budget scoring"""
        score, feedback = calculate_budget_score(self.sample_summary)
        self.assertLessEqual(score, 10)
        self.assertTrue(isinstance(feedback, str))

    def test_run_scorer_integration(self):
        """Test the main scoring function"""
        # Test with dictionary input
        result = run_scorer(self.sample_summary)
        self.assertTrue(isinstance(result, dict))
        self.assertIn("total_score", result)
        self.assertIn("categories", result)
        self.assertIn("recommendation", result)
        self.assertLessEqual(result["total_score"], 100)
        
        # Test with JSON string input
        json_input = json.dumps(self.sample_summary)
        result_json = run_scorer(json_input)
        self.assertEqual(result_json["total_score"], result["total_score"])

    def test_run_scorer_error_handling(self):
        """Test error handling in run_scorer"""
        # Test with invalid JSON string
        result_invalid = run_scorer("invalid json")
        self.assertIn("error", result_invalid)
        self.assertEqual(result_invalid["total_score"], 0)
        
        # Test with empty dictionary
        result_empty = run_scorer({})
        self.assertEqual(result_empty["total_score"], 0)
        
        # Test with minimal content
        result_minimal = run_scorer(self.minimal_summary)
        self.assertLessEqual(result_minimal["total_score"], result_minimal["max_score"])

    def test_score_consistency(self):
        """Test that scores are consistent and properly bounded"""
        result = run_scorer(self.sample_summary)
        
        # Check category scores are within bounds
        self.assertLessEqual(result["categories"]["research_impact"]["score"], 25)
        self.assertLessEqual(result["categories"]["methodology"]["score"], 25)
        self.assertLessEqual(result["categories"]["innovation"]["score"], 20)
        self.assertLessEqual(result["categories"]["feasibility"]["score"], 20)
        self.assertLessEqual(result["categories"]["budget"]["score"], 10)
        
        # Check total score matches sum of categories
        category_sum = sum(cat["score"] for cat in result["categories"].values())
        self.assertAlmostEqual(result["total_score"], category_sum, places=2)

    def test_recommendation_thresholds(self):
        """Test that recommendation thresholds are correctly applied"""
        # Create summaries that should trigger different recommendations
        high_score_summary = self.sample_summary.copy()
        low_score_summary = self.minimal_summary.copy()
        
        result_high = run_scorer(high_score_summary)
        result_low = run_scorer(low_score_summary)
        
        # Test recommendations based on scores
        if result_high["total_score"] >= 85:
            self.assertEqual(result_high["recommendation"], "Strong Accept")
        elif result_high["total_score"] >= 75:
            self.assertEqual(result_high["recommendation"], "Accept")
        elif result_high["total_score"] >= 65:
            self.assertEqual(result_high["recommendation"], "Borderline")
        else:
            self.assertEqual(result_high["recommendation"], "Reject")
            
        # Low score should be Reject or Borderline
        self.assertIn(result_low["recommendation"], ["Reject", "Borderline"])

if __name__ == '__main__':
    unittest.main()