from app.ai_utils import parse_contract_description, analyze_cv


def test_parse_contract_description_defaults():
    parsed = parse_contract_description("Need experts for enterprise workshops")
    assert parsed["subject"] == "Programming"
    assert parsed["required_trainers"] == 2


def test_parse_contract_description_extracts_values():
    parsed = parse_contract_description("Looking for 4 trainers in Data Science and Python")
    assert parsed["subject"] in {"Data Science", "Python"}
    assert parsed["required_trainers"] == 4


def test_analyze_cv_score_caps():
    score = analyze_cv("python_cv.pdf", "Python", "Python, NLP", 10)
    assert score <= 100
    assert score == 80
