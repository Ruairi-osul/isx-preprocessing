from isx_preprocessing.path_parcers.raw import (
    AstrocyteSet1IsxMouseDir, IsxRootParserAstrocyteSet1
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirAstrocyte, OutputRootParserAstrocyte
)
from isx_preprocessing.exporting import IsxLongtitudinalRegistration
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm


SOURCE_DIR = Path(r"F:\Raw OFL")
DEST_DIR = Path(r"F:\OFL\ofl-first")
ON_EXISTS = "overwrite"




def get_mouse_dir(
    source: AstrocyteSet1IsxMouseDir, target_dirs: Sequence[OutputMouseDirAstrocyte]
) -> Optional[OutputMouseDirAstrocyte]:

    for target in target_dirs:
        if source.mouse_name == target.mouse_name:
            return target
    return None



def main():
    source_mouse_dirs = IsxRootParserAstrocyteSet1.from_root_dir(
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
        
        sessions = [
            source_mouse_dir.cond_dir,
            source_mouse_dir.ret_behavior_dir,
            source_mouse_dir.ext_behavior_dir,
            source_mouse_dir.ext_ret_dir,
            source_mouse_dir.long_ret_dir,
            source_mouse_dir.renew_dir,
        ]

        input_cellsets = []
        missing_indices = []
        for i, session in enumerate(sessions):
            if session.cellset_file is not None:
                input_cellsets.append(session.cellset_file)
            else:
                missing_indices.append(i)
        
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
