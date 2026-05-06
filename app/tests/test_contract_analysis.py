import json
import pytest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.contract_analysis_service import parse_and_validate_ai_response
from schemas.ai_analysis_response import AIAnalysisResponse

class TestJSONSchemaValidity:
    
    def test_valid_response_with_risks(self):
        
        valid_response = json.dumps({
            "risks": [
                {
                    "type": "Termination",
                    "explanation": "No notice period",
                    "suggested_fix": "Add 30 day notice requirement",
                    "confidence": 0.92,
                    "evidence": "employer may terminate at any time without notice"
                }
            ]
        })
        
        result = parse_and_validate_ai_response(valid_response)
        assert isinstance(result, AIAnalysisResponse)
        assert len(result.risks) == 1
    
    def test_empty_risks_array_is_valid(self):
        
        valid_response = json.dumps({"risks": []})
        
        result = parse_and_validate_ai_response(valid_response)
        assert isinstance(result, AIAnalysisResponse)
        assert result.risks == []
        

class TestEvidenceFieldPresence:
    
    def test_all_risks_have_evidence(self):
    
        response_with_multiple_risks = json.dumps({
            "risks": [
                {
                    "type": "Probation",
                    "explanation": "Long probation",
                    "suggested_fix": "Reduce probation",
                    "confidence": 0.85,
                    "evidence": "probation period of twelve months"
                },
                {
                    "type": "Termination",
                    "explanation": "Immediate termination",
                    "suggested_fix": "Require notice",
                    "confidence": 0.88,
                    "evidence": "end the employment immediately"
                }
            ]
        })
        
        result = parse_and_validate_ai_response(response_with_multiple_risks)
        
        for risk in result.risks:
            assert hasattr(risk, "evidence")
            assert risk.evidence is not None
            assert len(risk.evidence) > 0
            assert isinstance(risk.evidence, str)
            

@pytest.mark.asyncio
class TestStableBehavior:
    
    @patch("services.contract_analysis_service.get_ai_response")
    async def test_tc2_returns_probation_and_termination(self, mock_ai):
        
        from services.contract_analysis_service import analyze_contract
        
        mock_ai.return_value = json.dumps({
            "risks": [
                {
                    "type": "Probation",
                    "explanation": "Long probation",
                    "suggested_fix": "Reduce to 3 months",
                    "confidence": 0.87,
                    "evidence": "probation period of twelve months"
                },
                {
                    "type": "Termination",
                    "explanation": "Immediate termination",
                    "suggested_fix": "Add notice requirement",
                    "confidence": 0.90,
                    "evidence": "may end employment immediately"
                }
            ]
        })
        
        result = await analyze_contract("Test probation contract")
        risks = result.get("content").risks
        
        assert len(risks) == 2
        risk_types = {r.type for r in risks}
        assert "Probation" in risk_types
        assert "Termination" in risk_types
    
    @patch("services.contract_analysis_service.get_ai_response")
    async def test_safe_contract_returns_no_risks(self, mock_ai):
        
        from services.contract_analysis_service import analyze_contract
        
        mock_ai.return_value = json.dumps({"risks": []})
        
        result = await analyze_contract("Safe contract with no issues")
        risks = result.get("content").risks
        
        assert len(risks) == 0