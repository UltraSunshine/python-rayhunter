"""
Configuration tests.

Fetches the current runtime configuration, modifies test_analyzer and
colorblind_mode, posts it back, and verifies the changes survive a reboot.
Then reverts the device to its original configuration and verifies again.
"""

import time

from rayhunter import RayhunterApi
from rayhunter.configuration import Config

REBOOT_WAIT_SECONDS = 45


def test_fetch_original_config(api: RayhunterApi, config_state: dict):
    """Fetch the current runtime configuration and store it for later restoration."""
    config = api.get_config()

    assert isinstance(config, Config), "Expected get_config() to return a Config instance"
    assert isinstance(config.colorblind_mode, bool), "Expected colorblind_mode to be a bool"
    assert isinstance(config.analyzers.test_analyzer, bool), "Expected test_analyzer to be a bool"

    config_state["original"] = config
    print(f"\nFetched original config — colorblind_mode: {config.colorblind_mode}, test_analyzer: {config.analyzers.test_analyzer}")


def test_modify_and_post_config(api: RayhunterApi, config_state: dict):
    """Enable test_analyzer, toggle colorblind_mode, post the config, then wait for device reboot."""
    assert config_state["original"] is not None, (
        "No original config stored — test_fetch_original_config must run first"
    )

    config = api.get_config()
    config.analyzers.test_analyzer = True
    config.colorblind_mode = not config.colorblind_mode

    print(f"\nPosting modified config — colorblind_mode: {config.colorblind_mode}, test_analyzer: {config.analyzers.test_analyzer}")
    print(f"Waiting {REBOOT_WAIT_SECONDS}s for device to reboot...")
    api.set_config(config)
    time.sleep(REBOOT_WAIT_SECONDS)


def test_verify_modified_config(api: RayhunterApi, config_state: dict):
    """Fetch the config after reboot and verify the expected values were applied."""
    assert config_state["original"] is not None, (
        "No original config stored — test_fetch_original_config must run first"
    )

    original: Config = config_state["original"]
    config = api.get_config()

    assert config.analyzers.test_analyzer is True, (
        f"Expected test_analyzer to be True after modification, got {config.analyzers.test_analyzer}"
    )
    assert config.colorblind_mode == (not original.colorblind_mode), (
        f"Expected colorblind_mode to be {not original.colorblind_mode} after toggle, "
        f"got {config.colorblind_mode}"
    )

    print(f"\nVerified modified config — colorblind_mode: {config.colorblind_mode}, test_analyzer: {config.analyzers.test_analyzer}")


def test_revert_config(api: RayhunterApi, config_state: dict):
    """Post the original configuration back to the device and wait for reboot."""
    assert config_state["original"] is not None, (
        "No original config stored — test_fetch_original_config must run first"
    )

    original: Config = config_state["original"]
    print(f"\nReverting config — colorblind_mode: {original.colorblind_mode}, test_analyzer: {original.analyzers.test_analyzer}")
    print(f"Waiting {REBOOT_WAIT_SECONDS}s for device to reboot...")
    api.set_config(original)
    time.sleep(REBOOT_WAIT_SECONDS)


def test_verify_reverted_config(api: RayhunterApi, config_state: dict):
    """Fetch the config after revert and confirm it matches the original values."""
    assert config_state["original"] is not None, (
        "No original config stored — test_fetch_original_config must run first"
    )

    original: Config = config_state["original"]
    config = api.get_config()

    assert config.colorblind_mode == original.colorblind_mode, (
        f"Expected colorblind_mode to be reverted to {original.colorblind_mode}, "
        f"got {config.colorblind_mode}"
    )
    assert config.analyzers.test_analyzer == original.analyzers.test_analyzer, (
        f"Expected test_analyzer to be reverted to {original.analyzers.test_analyzer}, "
        f"got {config.analyzers.test_analyzer}"
    )

    print(f"\nConfig successfully reverted — colorblind_mode: {config.colorblind_mode}, test_analyzer: {config.analyzers.test_analyzer}")
