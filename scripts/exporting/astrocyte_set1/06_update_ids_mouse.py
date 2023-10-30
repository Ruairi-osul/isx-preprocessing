from isx_preprocessing.path_parcers.output import OutputRootParserAstrocyte
from isx_preprocessing.exporting.update_ids import IDUpdaterMouse
from pathlib import Path
from tqdm import tqdm

DEST_DIR = Path(r"F:\Astrocyte\Export")
ON_EXISTS = "overwrite"


def main():
    mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        DEST_DIR,
    ).mouse_dirs

    id_updater = IDUpdaterMouse(
        session_cell_id="session_cell_id",
        mouse_cell_id="mouse_cell_id",
        on_exists=ON_EXISTS,
    )

    for mouse_dir in tqdm(mouse_dirs):

        sessions = [
            mouse_dir.cond_dir,
            mouse_dir.ret_behavior_dir,
            mouse_dir.ext_behavior_dir,
            mouse_dir.ext_ret_dir,
            mouse_dir.long_ret_dir,
            mouse_dir.renew_dir,
        ]
        session_names = (
            "cond",
            "ret",
            "ext",
            "diff-ret",
            "late-ret",
            "renewal",
        )
        for session_dir, session_name in zip(sessions, session_names):
            if session_dir.traces_tidy.exists():
                id_updater.update_traces(
                    longreg_file=mouse_dir.long_reg_tidy_csv,
                    trace_file=session_dir.traces_tidy,
                    updated_trace_file=session_dir.traces_tidy_mouse_id,
                    session_name=session_name,
                )
            if session_dir.props_tidy.exists():
                id_updater.update_props(
                    longreg_file=mouse_dir.long_reg_tidy_csv,
                    props_file=session_dir.props_tidy,
                    updated_props_file=session_dir.props_tidy_mouse_id,
                    session_name=session_name,
                )


if __name__ == "__main__":
    main()
