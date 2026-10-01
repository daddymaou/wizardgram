from wizardgram import VerificationStatus, status


def test_known_method_is_verified() -> None:
    assert status("sendMessage") is VerificationStatus.VERIFIED


def test_unknown_method_is_unverified() -> None:
    assert status("notARealMethod") is VerificationStatus.UNVERIFIED
