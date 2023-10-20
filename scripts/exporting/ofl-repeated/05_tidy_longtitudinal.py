from isx_preprocessing.path_parcers.output import (
    OutputMouseDirOFLFirst,
    OutputRootParserOFLFirst,
)
from isx_preprocessing.exporting.tidy_output import LongRegTidier
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path(r"F:\Raw OFL")
DEST_DIR = Path(r"F:\OFL\ofl-first")
ON_EXISTS = "overwrite"


def main():
    mouse_dirs = OutputRootParserOFLFirst.from_root_dir(
        DEST_DIR,
    ).mouse_dirs

    tidier = LongRegTidier(
        sessions=("day1", "day2", "day3", "day4"),
        session_cell_id="session_cell_id",
        mouse_cell_id="mouse_cell_id",
        on_exists=ON_EXISTS,
    )

    for mouse_dir in tqdm(mouse_dirs):
        tidier(
            source_long_reg_file=mouse_dir.long_reg_csv,
            output_long_reg_file=mouse_dir.long_reg_tidy_csv,
        )


if __name__ == "__main__":
    main()
