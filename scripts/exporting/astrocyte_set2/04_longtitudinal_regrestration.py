from isx_preprocessing.path_parcers.raw import (
    AstrocyteSet2IsxMouseDir,
    IsxRootParserAstrocyteSet2,
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirAstrocyte,
    OutputRootParserAstrocyte,
)
from isx_preprocessing.exporting.longreg import IsxLongtitudinalRegistration
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm


SOURCE_DIR = Path(r"G:\AS-Gq-GRIN")
DEST_DIR = Path(r"F:\Astrocyte\Export")
ON_EXISTS = "overwrite"


def get_mouse_dir(
    source: AstrocyteSet2IsxMouseDir, target_dirs: Sequence[OutputMouseDirAstrocyte]
) -> Optional[OutputMouseDirAstrocyte]:

    for target in target_dirs:
        if source.mouse_name == target.mouse_name:
            return target
    return None


def main():
    source_mouse_dirs = IsxRootParserAstrocyteSet2.from_root_dir(
        SOURCE_DIR,
    ).mouse_dirs
    target_mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        DEST_DIR,
    ).mouse_dirs

    long_reg = IsxLongtitudinalRegistration(
        min_correlation=0.4, accepted_cells_only=True, on_exists=ON_EXISTS
    )

    for source_mouse_dir in tqdm(source_mouse_dirs):
        target_mouse_dir = get_mouse_dir(source_mouse_dir, target_mouse_dirs)
        print(f"Processing {source_mouse_dir.mouse_name}")

        if source_mouse_dir.mouse_name == "AS-Gq-hSyn-11":
            sessions = [
                source_mouse_dir.cond_dir,
                source_mouse_dir.ret_behavior_dir,
                source_mouse_dir.ext_behavior_dir,
            ]
            missing_indices = [3, 4, 5]
        elif source_mouse_dir.mouse_name == "AS-Gq-hSyn-12":
            sessions = [
                source_mouse_dir.cond_dir,
                source_mouse_dir.ext_behavior_dir,
                source_mouse_dir.long_ret_dir,
                source_mouse_dir.renew_dir,
            ]
            missing_indices = [1, 3]
        elif source_mouse_dir.mouse_name == "AS-Gq-hSyn-14":
            sessions = [
                source_mouse_dir.cond_dir,
                source_mouse_dir.ret_behavior_dir,
                source_mouse_dir.ext_behavior_dir,
                source_mouse_dir.ext_ret_dir,
            ]
            missing_indices = [4, 5]
        else:
            sessions = [
                source_mouse_dir.cond_dir,
                source_mouse_dir.ret_behavior_dir,
                source_mouse_dir.ext_behavior_dir,
                source_mouse_dir.ext_ret_dir,
                source_mouse_dir.long_ret_dir,
                source_mouse_dir.renew_dir,
            ]
            missing_indices = []

        input_cellsets = []
        for i, session in enumerate(sessions):
            if session.cnmfe_cellset is not None:
                input_cellsets.append(session.cnmfe_cellset)

        output_csv_file = target_mouse_dir.long_reg_csv
        try:
            long_reg(
                cellset_files=input_cellsets,
                missing_indices=missing_indices,
                output_csv_file=output_csv_file,
                transform_csv_file=target_mouse_dir.long_reg_translation_csv,
                crop_csv_file=target_mouse_dir.long_reg_crop_csv,
            )
        except Exception as e:
            print(f"Failed on {source_mouse_dir.mouse_name}")
            raise e


if __name__ == "__main__":
    main()
