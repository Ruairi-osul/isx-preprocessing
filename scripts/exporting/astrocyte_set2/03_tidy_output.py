from isx_preprocessing.path_parcers.output import (
    OutputRootParserAstrocyte,
)
from isx_preprocessing.exporting.tidy_output import TraceTidier, PropsTidier
from pathlib import Path
from tqdm import tqdm

DEST_DIR = Path(r"F:\Astrocyte\Export")
ON_EXISTS = "overwrite"


def main():
    mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        DEST_DIR,
    ).mouse_dirs

    trace_tidyer = TraceTidier(on_exists=ON_EXISTS)
    props_tidyer = PropsTidier(on_exists=ON_EXISTS)

    for mouse_dir in tqdm(mouse_dirs):
        sessions = [
            mouse_dir.cond_dir,
            mouse_dir.ret_behavior_dir,
            mouse_dir.ext_behavior_dir,
            mouse_dir.ext_ret_dir,
            mouse_dir.long_ret_dir,
            mouse_dir.renew_dir,
        ]

        for session_dir in sessions:
            if session_dir.traces.exists():
                trace_tidyer(
                    source_trace_file=session_dir.traces,
                    output_trace_file=session_dir.traces_tidy,
                )
            if session_dir.props.exists():
                props_tidyer(
                    source_props_file=session_dir.props,
                    output_props_file=session_dir.props_tidy,
                )


if __name__ == "__main__":
    main()
