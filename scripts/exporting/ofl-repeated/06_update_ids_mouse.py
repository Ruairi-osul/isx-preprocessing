from isx_preprocessing.path_parcers.output import OutputRootParserOFLRepeated
from isx_preprocessing.exporting.update_ids import IDUpdaterMouse
from pathlib import Path
from tqdm import tqdm

DEST_DIR = Path(r"/Volumes/Pdata/OFL/ofl-repeated")
ON_EXISTS = "overwrite"


def main():
    mouse_dirs = OutputRootParserOFLRepeated.from_root_dir(
        DEST_DIR, 
    ).mouse_dirs

    id_updater = IDUpdaterMouse(session_cell_id="session_cell_id", mouse_cell_id="mouse_cell_id", on_exists=ON_EXISTS)

    for mouse_dir in tqdm(mouse_dirs):
        sessions = mouse_dir.day_dirs[1:]
        for session_dir in sessions:
            id_updater.update_traces(
                longreg_file=mouse_dir.long_reg_tidy_csv,
                trace_file=session_dir.traces_tidy,
                updated_trace_file=session_dir.traces_tidy_mouse_id,
                session_name=session_dir.session_dir.name
            )
            id_updater.update_props(
                longreg_file=mouse_dir.long_reg_tidy_csv,
                props_file=session_dir.props_tidy,
                updated_props_file=session_dir.props_tidy_mouse_id,
                session_name=session_dir.session_dir.name
            )


if __name__ == "__main__":
    main()
