from isx_preprocessing.path_parcers.output import OutputRootParserOFLRepeated
from isx_preprocessing.dataset_create import (
    TraceCreater,
    PropsCreater,
    MasterCellsetCreater,
)
from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass

SOURCE_DIR = Path(r"/Volumes/Pdata/OFL/ofl-repeated")
DEST_DIR = Path(r"/Volumes/Pdata/OFL/ofl-repeated dataset")

ON_EXISTS = "overwrite"
COMPRESSION = "snappy"


@dataclass
class SessionAttr:
    session_name: str
    session_attr: str
    sub_dir: str


def main():
    mouse_dirs = OutputRootParserOFLRepeated.from_root_dir(
        SOURCE_DIR, 
    ).mouse_dirs


    day1 = SessionAttr(
        session_name="day1", session_attr="day1_dir", sub_dir="01-day1"
    )
    day2 = SessionAttr(
        session_name="day2", session_attr="day2_dir", sub_dir="02-day2"
    )
    day3 = SessionAttr(
        session_name="day3", session_attr="day3_dir", sub_dir="03-day3"
    )
    day4 = SessionAttr(
        session_name="day4", session_attr="day4_dir", sub_dir="04-day4"
    )
    sessions = [day1, day2, day3, day4]

    trace_creator = TraceCreater(trace_fn="traces.parquet", compression=COMPRESSION)
    props_creator = PropsCreater(props_fn="cell_props.parquet", compression=COMPRESSION)
    master_cellset_creator = MasterCellsetCreater(fn="master_cellset.parquet")

    master_cellset_creator(
        source_cellset=SOURCE_DIR / "master_cellset.csv", output_dir=DEST_DIR
    )

    for session_attr in tqdm(sessions):
        trace_files = []
        props_files = []
        for mouse_dir in mouse_dirs:
            session_dir = getattr(mouse_dir, session_attr.session_attr)
            trace_files.append(session_dir.traces_tidy_mouse_dataset_id)
            props_files.append(session_dir.props_tidy_mouse_dataset_id)
        trace_creator(
            trace_files=trace_files, output_dir=DEST_DIR / session_attr.sub_dir
        )
        props_creator(
            props_files=props_files, output_dir=DEST_DIR / session_attr.sub_dir
        )


if __name__ == "__main__":
    main()
