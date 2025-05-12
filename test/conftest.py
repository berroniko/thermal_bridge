import pytest


@pytest.fixture(scope="session")
def fp_psi_data(tmp_path_factory):
    """return a non-existant filepath to instantiate psi_data"""
    filepath = tmp_path_factory.mktemp('data') / "test_psi_data.json"  # this file can be modified
    return filepath
