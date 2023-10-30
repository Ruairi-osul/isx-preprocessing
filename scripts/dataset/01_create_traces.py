from isx_preprocessing.path_parcers.output import OutputRootParserAstrocyte
from isx_preprocessing.dataset_create import (
    TraceCreater,
    PropsCreater,
    MasterCellsetCreater,
)
from pathlib import Path
from tqdm import tqdm
from dataclasses import dataclass

SOURCE_DIR = Path(r"F:\Astrocyte\Export")

DEST_DIR = Path(r"F:\Astrocyte\dataset-01")
ON_EXISTS = "overwrite"

COMPRESSION = "snappy"


@dataclass
class SessionAttr:
    session_name: str
    session_attr: str
    sub_dir: str


def main():
    mouse_dirs = OutputRootParserAstrocyte.from_root_dir(
        SOURCE_DIR,
    ).mouse_dirs

    cond = SessionAttr(session_name="cond", session_attr="cond_dir", sub_dir="01-cond")
    ret = SessionAttr(
        session_name="ret", session_attr="ret_behavior_dir", sub_dir="02-ret"
    )
    ext = SessionAttr(
        session_name="ext", session_attr="ext_behavior_dir", sub_dir="03-ext"
    )
    diff_ret = SessionAttr(
        session_name="diff-ret", session_attr="ext_ret_dir", sub_dir="04-diff-ret"
    )
    late_ret = SessionAttr(
        session_name="late-ret", session_attr="long_ret_dir", sub_dir="05-late-ret"
    )
    renewal = SessionAttr(
        session_name="renewal", session_attr="renew_dir", sub_dir="05-renewal"
    )
    sessions = [cond, ret, ext, diff_ret, late_ret, renewal]

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
            if session_dir.traces_tidy_mouse_id.exists():
                trace_files.append(session_dir.traces_tidy_mouse_dataset_id)
            if session_dir.props_tidy_mouse_id.exists():
                props_files.append(session_dir.props_tidy_mouse_dataset_id)

        trace_creator(
            trace_files=trace_files, output_dir=DEST_DIR / session_attr.sub_dir
        )
        props_creator(
            props_files=props_files, output_dir=DEST_DIR / session_attr.sub_dir
        )


if __name__ == "__main__":
    main()
