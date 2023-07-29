from isx_preprocessing.path_parcers.raw import (
    OFLFirstIsxMouseDir, IsxRootParserOFLFirst
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirOFLFirst, OutputRootParserOFLFirst
)
from isx_preprocessing.exporting import IsxExporter
from typing import Optional, Sequence
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path(r"F:\Raw OFL")
DEST_DIR = Path(r"F:\OFL\ofl-first")
ON_EXISTS = "skip"

TRACE_FILENAME = "traces.csv"
PROPS_FILENAME = "props.csv"
TIFF_SUBDIR = "tiff"
TIFF_FILENAME = "tiff.tif"


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

    isx_exporter = IsxExporter(
        trace_filename=TRACE_FILENAME,
        props_filename=PROPS_FILENAME,
        tiff_subdir=TIFF_SUBDIR,
        tiff_filename=TIFF_FILENAME,
        on_exists=ON_EXISTS,
    )
    print(len(source_mouse_dirs))
    print(len(target_mouse_dirs))


    for source_mouse_dir in tqdm(source_mouse_dirs):
        target_mouse_dir = get_mouse_dir(source_mouse_dir, target_mouse_dirs)

        source_sessions = source_mouse_dir.day_dirs[1:]
        tartget_sessions = target_mouse_dir.day_dirs[1:]
        for source_session_dir, target_session_dir in zip(
            source_sessions, tartget_sessions
        ):
            isx_exporter(
                cellset_file=source_session_dir.cnmfe_cellset,
                output_dir=target_session_dir.session_dir,
            )


if __name__ == "__main__":
    main()
