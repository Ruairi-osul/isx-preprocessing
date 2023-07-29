import pandas as pd
from pathlib import Path
from typing import Sequence, Optional


class Creater:
    def __init__(self, compression: Optional[str] = "snappy"):
        self.compression = compression

    def make_dir(self, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)


class TraceCreater(Creater):
    """
    Create a single parquet file containing all traces from a list of trace files.

    Args:
        trace_fn: Name of the output trace file.
        compression: Compression algorithm to use for the output trace file. Default is "snappy". {'snappy', 'gzip', 'brotli', None}
    """

    def __init__(
        self,
        trace_fn: str = "traces.parquet",
        compression: str = "snappy",
        pivot: bool = True,
        pivot_agg: str = "mean",
    ):
        self.trace_fn = trace_fn
        self.compression = compression
        self.pivot = pivot
        self.pivot_agg = pivot_agg

    def pivot_traces(self, df: pd.DataFrame) -> pd.DataFrame:
        df["cell_id"] = df["cell_id"].astype(str)
        df = df.pivot_table(
            index="time", columns="cell_id", values="value", aggfunc=self.pivot_agg
        )
        df.columns.name = None
        df.reset_index(inplace=True)
        return df

    def __call__(self, trace_files: Sequence[Path], output_dir: Path):
        self.make_dir(output_dir)
        df = pd.concat([pd.read_csv(trace_file) for trace_file in trace_files])
        if self.pivot:
            df = self.pivot_traces(df)
        df.to_parquet(output_dir / self.trace_fn, compression=self.compression)


class PropsCreater(Creater):
    """
    Create a single parquet file containing all props from a list of props files.

    Args:
        props_fn: Name of the output props file.
        compression: Compression algorithm to use for the output props file. Default is "snappy". {'snappy', 'gzip', 'brotli', None}
    """

    def __init__(
        self, props_fn: str = "cell_props.parquet", compression: str = "snappy"
    ):
        self.props_fn = props_fn
        self.compression = compression

    def __call__(self, props_files: Sequence[Path], output_dir: Path):
        self.make_dir(output_dir)
        df = pd.concat([pd.read_csv(props_file) for props_file in props_files])
        df.to_parquet(output_dir / self.props_fn, compression=self.compression)


class MasterCellsetCreater(Creater):
    """
    Convert the master cellset to a parquet file.
    Args:
    """

    def __init__(
        self, fn: str = "master_cellset.parquet", compression: Optional[str] = None
    ):
        self.fn = fn
        self.compression = compression

    def __call__(self, source_cellset: Path, output_dir: Path):
        self.make_dir(output_dir)
        df = pd.read_csv(source_cellset)
        df.to_parquet(output_dir / self.fn, compression=self.compression)
