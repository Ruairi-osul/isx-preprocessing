from isx_preprocessing.path_parcers.output import OutputRootParserAstrocyte
from isx_preprocessing.dataset_create import (
    TraceCreater,
    PropsCreater,
    MasterCellsetCreater,
)
from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass

GOOD_MICE_NUMS = (5, 8, 9, 13, 15, 22, 27, 30, 31, 6, 7, 12, 18, 24, 25, 28, 32)
SOURCE_DIR = Path(r"/Volumes/Pdata/astrocyte/export1")
DEST_DIR = Path(r"/Volumes/Pdata/astrocyte/dataset_1")
ON_EXISTS = "overwrite"
COMPRESSION = "snappy"


@dataclass
class SessionAttr:
    session_name: str
    session_attr: str
    sub_dir: str


def main():
    mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        SOURCE_DIR, numbers=GOOD_MICE_NUMS
    ).mouse_dirs

    ret = SessionAttr(
        session_name="ret", session_attr="ret_behavior_dir", sub_dir="03-ret"
    )
    ext = SessionAttr(
        session_name="ext", session_attr="ext_behavior_dir", sub_dir="04-ext"
    )

    trace_creator = TraceCreater(trace_fn="traces.parquet", compression=COMPRESSION)
    props_creator = PropsCreater(props_fn="cell_props.parquet", compression=COMPRESSION)
    master_cellset_creator = MasterCellsetCreater(fn="master_cellset.parquet")

    master_cellset_creator(
        source_cellset=SOURCE_DIR / "master_cellset.csv", output_dir=DEST_DIR
    )

    for session_attr in tqdm((ret, ext)):
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
