from isx_preprocessing.path_parcers.raw import (
    OFLFirstIsxMouseDir, IsxRootParserOFLFirst
)
from isx_preprocessing.path_parcers.output import (
    OutputMouseDirOFLFirst, OutputRootParserOFLFirst
)
from isx_preprocessing.exporting import TraceTidier, PropsTidier
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = Path(r"F:\Raw OFL")
DEST_DIR = Path(r"F:\OFL\ofl-first")
ON_EXISTS = "skip"


def main():
    mouse_dirs = OutputRootParserOFLFirst.from_root_dir(
        DEST_DIR, 
    ).mouse_dirs

    trace_tidyer = TraceTidier(on_exists=ON_EXISTS)
    props_tidyer = PropsTidier(on_exists=ON_EXISTS)

    for mouse_dir in tqdm(mouse_dirs):
        sessions = mouse_dir.day_dirs[1:]
        for session_dir in sessions:
            trace_tidyer(
                source_trace_file=session_dir.traces,
                output_trace_file=session_dir.traces_tidy,
            )
            props_tidyer(
                source_props_file=session_dir.props,
                output_props_file=session_dir.props_tidy,
            )


if __name__ == "__main__":
    main()
