from isx_preprocessing.path_parcers.output import OutputRootParserOFLRepeated
from isx_preprocessing.exporting.update_ids import IDUpdaterDataset
from pathlib import Path
from tqdm import tqdm


SOURCE_DIR = Path(r"D:\Shana ISX Reordered")
DEST_DIR = Path(r"F:\OFL\ofl-repeated")
ON_EXISTS = "overwrite"
MASTER_CELLSET_FILE = DEST_DIR / "master_cellset.csv"


def main():
    mouse_dirs = OutputRootParserOFLRepeated.from_root_dir(
        DEST_DIR, 
    ).mouse_dirs

    id_updater = IDUpdaterDataset(
        dataset_cell_id="cell_id",
        mouse_cell_id="mouse_cell_id",
        on_exists=ON_EXISTS,
    )
    props_files = [mouse_dir.long_reg_tidy_csv for mouse_dir in mouse_dirs]

    master_cellset = id_updater.create_master_cellset(
        props_files=props_files,
        master_cellset_file=MASTER_CELLSET_FILE,
    )

    for mouse_dir in tqdm(mouse_dirs):
        mouse_name = mouse_dir.mouse_name
        sessions = mouse_dir.day_dirs[1:]
        for session_dir in sessions:
            id_updater.update_traces(
                master_cellset=master_cellset,
                mouse_name=mouse_name,
                trace_file=session_dir.traces_tidy_mouse_id,
                updated_trace_file=session_dir.traces_tidy_mouse_dataset_id,
            )
            id_updater.update_props(
                master_cellset=master_cellset,
                mouse_name=mouse_name,
                props_file=session_dir.props_tidy_mouse_id,
                updated_props_file=session_dir.props_tidy_mouse_dataset_id,
            )


if __name__ == "__main__":
    main()
