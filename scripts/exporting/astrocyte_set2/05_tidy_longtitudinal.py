from isx_preprocessing.path_parcers.output import OutputRootParserAstrocyte
from isx_preprocessing.exporting.tidy_output import LongRegTidier
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path(r"G:\AS-Gq-GRIN")
DEST_DIR = Path(r"F:\Astrocyte\Export")
ON_EXISTS = "overwrite"


def main():
    mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        DEST_DIR,
    ).mouse_dirs

    tidier = LongRegTidier(
        sessions=(
            "cond",
            "ret",
            "ext",
            "diff-ret",
            "late-ret",
            "renewal",
        ),
        session_cell_id="session_cell_id",
        mouse_cell_id="mouse_cell_id",
        on_exists=ON_EXISTS,
    )

    for mouse_dir in tqdm(mouse_dirs):
        if mouse_dir.long_reg_csv.exists():
            tidier(
                source_long_reg_file=mouse_dir.long_reg_csv,
                output_long_reg_file=mouse_dir.long_reg_tidy_csv,
            )


if __name__ == "__main__":
    main()
