from isx_preprocessing.path_parcers.raw import (
    AstrocyteSet1IsxMouseDir,
    IsxRootParserAstrocyteSet1,
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirAstrocyte,
    OutputRootParserAstrocyte,
)
from isx_preprocessing.exporting.export_isx_files import IsxExporter
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path(r"D:\raw data")
DEST_DIR = Path(r"F:\Astrocyte\Export")
ON_EXISTS = "overwrite"

TRACE_FILENAME = "traces.csv"
PROPS_FILENAME = "props.csv"
TIFF_SUBDIR = "tiff"
TIFF_FILENAME = "tiff.tif"


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

    isx_exporter = IsxExporter(
        trace_filename=TRACE_FILENAME,
        props_filename=PROPS_FILENAME,
        tiff_subdir=TIFF_SUBDIR,
        tiff_filename=TIFF_FILENAME,
        on_exists=ON_EXISTS,
    )

    for source_mouse_dir in tqdm(source_mouse_dirs):
        target_mouse_dir = get_mouse_dir(source_mouse_dir, target_mouse_dirs)

        source_sessions = [
            source_mouse_dir.cond_dir,
            source_mouse_dir.ret_behavior_dir,
            source_mouse_dir.ext_behavior_dir,
            source_mouse_dir.ext_ret_dir,
            source_mouse_dir.long_ret_dir,
            source_mouse_dir.renew_dir,
        ]
        tartget_sessions = [
            target_mouse_dir.cond_dir,
            target_mouse_dir.ret_behavior_dir,
            target_mouse_dir.ext_behavior_dir,
            target_mouse_dir.ext_ret_dir,
            target_mouse_dir.long_ret_dir,
            target_mouse_dir.renew_dir,
        ]

        for source_session_dir, target_session_dir in zip(
            source_sessions, tartget_sessions
        ):
            
            if source_session_dir.cnmfe_cellset is not None:
                print(source_session_dir.session_dir.name)
                print(target_session_dir.session_dir.name)
                print()
                isx_exporter(
                    cellset_file=source_session_dir.cnmfe_cellset,
                    output_dir=target_session_dir.session_dir,
                )


if __name__ == "__main__":
    main()
