from isx_preprocessing.preprocessing import CNMFeDispatcher, ISXCNMFe
from isx_preprocessing.path_parcers.raw import AstrocyteSet2IsxMouseDir
from typing import List, Iterable, Optional
from pathlib import Path
from tqdm import tqdm

# GOOD_MICE_NUMS = (5, 8, 9, 13, 15, 22, 27, 30, 31, 6, 7, 12, 18, 24, 25, 28, 32)
ROOT_DIR =  Path(r"D:\AS-Gq-GRIN")


def find_mouse_dirs(
    root_dir: Path, numbers: Optional[Iterable[int]] = None
) -> List[AstrocyteSet2IsxMouseDir]:

    mouse_dirs: List[AstrocyteSet2IsxMouseDir] = []
    for d in root_dir.glob("*"):
        if not d.is_dir():
            continue
        if not d.name.startswith("A"):
            continue
        if numbers:
            subdir_number = int(d.name.split("-")[-1])
            if subdir_number not in numbers:
                continue
        try:
            mouse_dirs.append(AstrocyteSet2IsxMouseDir.from_mouse_dir(d))
        except ValueError:
            print(d.name)
            raise
    return mouse_dirs


def main():
    mouse_dirs = find_mouse_dirs(ROOT_DIR)
    dispatcher = CNMFeDispatcher(
        on_exists="skip",
        cnmfe=ISXCNMFe(num_threads=10),
    )
    for mouse_dir in tqdm(mouse_dirs, desc="Mice"):
        for session_dir in tqdm(
            mouse_dir.day_dirs,
            desc=f"{mouse_dir.mouse_name} sessions",
        ):
            dispatcher(isx_video=session_dir.motion_corrected)


if __name__ == "__main__":
    main()
