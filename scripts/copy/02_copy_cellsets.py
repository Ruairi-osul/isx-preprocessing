from isx_preprocessing.path_parcers.raw import (
    OFLFirstIsxMouseDir, IsxRootParserOFLFirst
)
from isx_preprocessing.path_parcers.output import (
    OutputRootParserOFLRepeated, OutputMouseDirOFLRepeated
)
from isx_preprocessing.exporting import IsxExporter
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm
import shutil

SOURCE_DIR = Path(r"E:\OFL\Raw ISX data\Cohort 1")
DEST_DIR = Path(r"F:\Raw OFL")
ON_EXISTS = "skip"



def get_mouse_dir(
    source: OFLFirstIsxMouseDir, target_dirs: Sequence[OutputMouseDirOFLRepeated]
) -> Optional[OutputMouseDirOFLRepeated]:

    for target in target_dirs:
        if source.mouse_name == target.mouse_name:
            return target
    return None


def main():
    source_mouse_dirs = IsxRootParserOFLFirst.from_root_dir(
        SOURCE_DIR,
    ).mouse_dirs
    target_mouse_dirs = IsxRootParserOFLFirst.from_root_dir(
        DEST_DIR, 
    ).mouse_dirs


    for source_mouse_dir in tqdm(source_mouse_dirs):
        target_mouse_dir = get_mouse_dir(source_mouse_dir, target_mouse_dirs)

        source_sessions = source_mouse_dir.day_dirs[1:]
        tartget_sessions = target_mouse_dir.day_dirs[1:]
        
        for source_session_dir, target_session_dir in zip(
            source_sessions, tartget_sessions
        ):
            source_cellset = source_session_dir.cnmfe_cellset
            target_cellset = target_session_dir.session_dir / source_session_dir.cnmfe_cellset.name
            shutil.copy(str(source_cellset), str(target_cellset))

if __name__ == "__main__":
    main()
