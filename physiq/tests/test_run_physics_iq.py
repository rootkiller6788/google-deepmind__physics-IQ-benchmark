# Copyright 2026 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import pytest
from run_physics_iq import generated_mask_file_name, validate_folder_files_exist

REAL_MASK = "0001_video-masks_24FPS_perspective-left_take-1_trimmed-lit-candle.mp4"


def _write(folder, *names):
    folder.mkdir(parents=True, exist_ok=True)
    for name in names:
        (folder / name).touch()
    return str(folder)


def test_validate_folder_files_exist_detects_missing_files(tmp_path):
    folder = _write(tmp_path / "masks", REAL_MASK)
    missing = "0002_video-masks_24FPS_perspective-center_take-1_trimmed-lit-candle.mp4"
    with pytest.raises(FileNotFoundError, match="missing files"):
        validate_folder_files_exist(folder, {REAL_MASK, missing}, "masks at FPS 24")


def test_validate_folder_files_exist_passes_when_complete(tmp_path):
    folder = _write(tmp_path / "masks", REAL_MASK)
    validate_folder_files_exist(folder, {REAL_MASK}, "masks at FPS 24")


def test_validate_folder_files_exist_normalises_30fps_expected(tmp_path):
    # Expected names derived from the 30FPS naming convention should be
    # normalised to the target FPS before the comparison.
    folder = _write(tmp_path / "masks", REAL_MASK)
    expected_30fps = {REAL_MASK.replace("24FPS", "30FPS")}
    validate_folder_files_exist(folder, expected_30fps, "masks at FPS 24")


def test_validate_folder_files_exist_missing_folder(tmp_path):
    with pytest.raises(FileNotFoundError, match="does not exist"):
        validate_folder_files_exist(
            str(tmp_path / "does-not-exist"), {REAL_MASK}, "masks at FPS 24"
        )


def test_generated_mask_file_name_matches_generate_mask_output():
    assert (
        generated_mask_file_name("0001_perspective-left_trimmed-lit-candle.mp4", 24)
        == REAL_MASK
    )
