import pytest
from crrt_calculations import calculate_crrt


def test_cvvh():
    r = calculate_crrt(
        "CVVH", 70,
        pre_replacement_ml_hr=500,
        post_replacement_ml_hr=500,
        net_uf_ml_hr=100
    )
    assert r["effluent_ml_hr"] == 1100


def test_cvvhd():
    r = calculate_crrt(
        "CVVHD", 70,
        dialysate_ml_hr=1000,
        net_uf_ml_hr=100
    )
    assert r["effluent_ml_hr"] == 1100


def test_cvvhdf():
    r = calculate_crrt(
        "CVVHDF", 70,
        dialysate_ml_hr=1000,
        pre_replacement_ml_hr=500,
        post_replacement_ml_hr=500,
        net_uf_ml_hr=100
    )
    assert r["effluent_ml_hr"] == 2100
    assert r["unadjusted_dose_ml_kg_hr"] == pytest.approx(30)


def test_invalid_weight():
    with pytest.raises(ValueError):
        calculate_crrt("CVVHD", 0)


def test_invalid_modality():
    with pytest.raises(ValueError):
        calculate_crrt("INVALID", 70)
