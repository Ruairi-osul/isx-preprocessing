from isx_preprocessing.preprocessing import CNMFeDispatcher, ISXCNMFe
from isx_preprocessing.path_parcers.raw import (
    IsxRootParserAstrocyteSet1,
)
from pathlib import Path
from tqdm import tqdm

# GOOD_MICE_NUMS = (5, 8, 9, 13, 15, 22, 27, 30, 31, 6, 7, 12, 18, 24, 25, 28, 32)
ON_EXISTS = "skip"
CNMFE_NUM_THREADS = 10
ROOT_DIR = Path(r"D:\raw data")


def main():
    root_parcer = IsxRootParserAstrocyteSet1.from_root_dir(
        ROOT_DIR,
    )
    mouse_dirs = root_parcer.mouse_dirs
    dispatcher = CNMFeDispatcher(
        on_exists=ON_EXISTS,
        cnmfe=ISXCNMFe(num_threads=CNMFE_NUM_THREADS),
    )
    for mouse_dir in tqdm(mouse_dirs, desc="Mice"):

        # only ret and ext sessions
        for session_dir in tqdm(
            mouse_dir.day_dirs,
            desc=f"{mouse_dir.mouse_name} sessions",
        ):
            dispatcher(isx_video=session_dir.motion_corrected)


if __name__ == "__main__":
    main()
