from src.verification_agent import run_verification_demo


def test_verification_corrects_silent_error():
    result = run_verification_demo("8 * 8")

    assert result["answer"] == "64"
    assert result["verified"] is False
    assert result["correction_made"] is True
    assert len(result["trajectory"]) == 2

    assert result["trajectory"][0]["observation"] == "63"
    assert result["trajectory"][1]["observation"] == "64"


def test_verification_accepts_correct_result():
    result = run_verification_demo("7 + 9")

    assert result["answer"] == "16"
    assert result["verified"] is True
    assert result["correction_made"] is False