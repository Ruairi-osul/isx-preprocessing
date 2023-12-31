import isx
from typing import Sequence, Optional, Union, List
from pathlib import Path
import tempfile
import random
import pandas as pd
import numpy as np


class IsxLongtitudinalRegistration:
    def __init__(
        self,
        min_correlation: float = 0.5,
        accepted_cells_only: bool = True,
        on_exists: str = "overwrite",
        _created_session_index_col: str = "local_cellset_index",
    ):
        self.min_correlation = min_correlation
        self.on_exists = on_exists
        self.accepted_cells_only = accepted_cells_only
        self._created_session_index_col = _created_session_index_col

    def _gen_temp_cellsets(self, cellset_files: Sequence[Path]) -> Sequence[Path]:
        tmp_dir = Path(tempfile.gettempdir())

        output_cellsets = [
            tmp_dir / (str(i) + str(random.randint(0, 100000)) + Path(f).name)
            for i, f in enumerate(cellset_files)
        ]
        return output_cellsets

    def if_exists(self, file: Path):
        if file.exists():
            if self.on_exists == "overwrite":
                file.unlink()
            elif self.on_exists == "raise":
                raise FileExistsError(f"{file} already exists")
            elif self.on_exists == "skip":
                return True

    def update_indexes(self, output_csv_file: Path, missing_indices: List[int]):
        """
        Update session indexes in the output file to account for any missing sessions
        """
        if len(missing_indices) == 0:
            return

        def adjust_index(index, missing):
            # count the number of missing indices before the current index
            adjustment = np.sum(missing <= index)

            # adjust the index
            new_index = index + adjustment

            # if the adjusted index is also missing, increment it until it's not
            while new_index in missing:
                new_index += 1
                adjustment += 1
                new_index = index + adjustment
            return new_index

        # sort in ascending order
        missing_indices = sorted(missing_indices)
        missing_indices_arr = np.array(missing_indices)

        df = pd.read_csv(output_csv_file)

        session_indices = df[self._created_session_index_col].values
        adjusted_indices = np.array(
            [adjust_index(idx, missing_indices_arr) for idx in session_indices]
        )

        print(session_indices)
        print(adjusted_indices)
        print(missing_indices)

        df[self._created_session_index_col] = adjusted_indices

        df.to_csv(output_csv_file, index=False)

    def __call__(
        self,
        cellset_files: Sequence[Path],
        output_csv_file: Path,
        missing_indices: Optional[List[int]] = None,
        transform_csv_file: Optional[Union[Path, str]] = None,
        crop_csv_file: Optional[Union[Path, str]] = None,
    ):
        self.if_exists(Path(output_csv_file))
        temp_cellsets = self._gen_temp_cellsets(cellset_files)

        if transform_csv_file:
            self.if_exists(Path(transform_csv_file))
        else:
            transform_csv_file = ""

        if crop_csv_file:
            self.if_exists(Path(crop_csv_file))
        else:
            crop_csv_file = ""

        isx.longitudinal_registration(
            input_cell_set_files=[str(f) for f in cellset_files],
            output_cell_set_files=[str(f) for f in temp_cellsets],
            csv_file=str(output_csv_file),
            transform_csv_file=str(transform_csv_file),
            crop_csv_file=str(crop_csv_file),
            min_correlation=self.min_correlation,
            accepted_cells_only=self.accepted_cells_only,
        )

        if missing_indices is not None:
            self.update_indexes(output_csv_file, missing_indices)
