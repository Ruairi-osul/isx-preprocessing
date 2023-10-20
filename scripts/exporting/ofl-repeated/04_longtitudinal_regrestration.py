from isx_preprocessing.path_parcers.raw import (
    OFLFirstIsxMouseDir, IsxRootParserOFLFirst
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirOFLFirst, OutputRootParserOFLFirst
)
from isx_preprocessing.exporting.longreg import IsxLongtitudinalRegistration
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm


SOURCE_DIR = Path(r"F:\Raw OFL")
DEST_DIR = Path(r"F:\OFL\ofl-first")
ON_EXISTS = "overwrite"


def get_mouse_dir(
    source: OFLFirstIsxMouseDir, target_dirs: Sequence[OutputMouseDirOFLFirst]
) -> Optional[OutputMouseDirOFLFirst]:

    for target in target_dirs:
        if source.mouse_name == target.mouse_name:
            return target
    return None



def main():
    source_mouse_dirs = IsxRootParserOFLFirst.from_root_dir(
        SOURCE_DIR, 
    ).mouse_dirs
    target_mouse_dirs = OutputRootParserOFLFirst.from_root_dir(
        DEST_DIR, 
    ).mouse_dirs


    long_reg = IsxLongtitudinalRegistration(
        min_correlation=0.4, accepted_cells_only=True, on_exists=ON_EXISTS
    )

    for source_mouse_dir in tqdm(source_mouse_dirs):
        target_mouse_dir = get_mouse_dir(source_mouse_dir, target_mouse_dirs)
        sessions = source_mouse_dir.day_dirs[1:]
        input_cellsets = [
            session.cnmfe_cellset for session in sessions
        ]
        output_csv_file = target_mouse_dir.long_reg_csv
        try:
            long_reg(
                cellset_files=input_cellsets,
                output_csv_file=output_csv_file,
                transform_csv_file=target_mouse_dir.long_reg_translation_csv,
                crop_csv_file=target_mouse_dir.long_reg_crop_csv,
            )
        except Exception as e:
            print(f"Failed on {source_mouse_dir.mouse_name}")
            raise e


if __name__ == "__main__":
    main()
