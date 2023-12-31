from pathlib import Path
from .output_session_dir import OutputDir
from dataclasses import dataclass
import datetime
from typing import List, Tuple


@dataclass
class OutputMouseDir:
    """
    A representation of the root directory of a hard drive containing data from a single mouse.

    Subdirectories are expected to be MouseDirs, and will be parsed as such.

    Expected directory structure:

    ├── mouse_1
    |   ├── long_reg.csv
    |   ├── long_reg_tidy.csv
    |   ├── long_reg_tidy_dataset_id.csv
    |   ├── long_reg_crop.csv
    |   ├── long_reg_translation.csv
    │   ├── session_1
    |   │   ├── traces.csv
    |   │   ├── traces_tidy.csv
    |   │   ├── traces_tidy_mouse_id.csv
    |   │   ├── traces_tidy_mouse_dataset_id.csv
    |   │   ├── props.csv
    |   │   ├── props_tidy.csv
    |   │   ├── props_tidy_mouse_id.csv
    |   │   ├── props_tidy_mouse_dataset_id.csv
    |   │   └── tiff
    |   │       ├── cell_0001.tif
    |   │       ├── cell_0002.tif
    |   │       ├── cell_0003.tif
    |   │       ├── cell_0004.tif
    |   |       ...
    │   ├── session_2
    |   │   ├── traces.csv
    |   │   ├── traces_tidy.csv
    |   |  ...

    """

    mouse_name: str
    mouse_dir: Path

    long_reg_csv: Path
    long_reg_tidy_csv: Path
    long_reg_tidy_dataset_id_csv: Path
    long_reg_crop_csv: Path
    long_reg_translation_csv: Path

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        raise NotImplementedError


@dataclass
class OutputMouseDirAstrocyte(OutputMouseDir):
    mouse_name: str
    mouse_dir: Path

    cond_dir: OutputDir
    ret_injection_dir: OutputDir
    ret_behavior_dir: OutputDir
    ext_injection_dir: OutputDir
    ext_behavior_dir: OutputDir
    ext_ret_dir: OutputDir
    long_ret_dir: OutputDir
    renew_dir: OutputDir

    @staticmethod
    def is_hab_dir(session_dir: Path):
        return "hab" in session_dir.name

    @staticmethod
    def sort_lret_ren(
        session_dir1: OutputDir, session_dir2: OutputDir
    ) -> Tuple[OutputDir, OutputDir]:
        if "ren" in session_dir1.session_dir.name.lower():
            return session_dir2, session_dir1
        else:
            return session_dir1, session_dir2

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        # filter sub_dirs to only include those that end in six digits
        sub_dirs = [
            OutputDir.from_session_dir(d)
            for d in mouse_dir.glob("*")
            if d.is_dir() and d.name[-6:].isdigit() and not cls.is_hab_dir(d)
        ]

        # order by date, they are in MMDDYY format
        sub_dirs = sorted(
            sub_dirs,
            key=lambda d: datetime.datetime.strptime(d.session_dir.name[-6:], "%m%d%y"),
        )

        cond_dir = sub_dirs[0]
        ret_behavior_dir, ret_injection_dir = sorted(
            (sub_dirs[1], sub_dirs[2]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_behavior_dir, ext_injection_dir = sorted(
            (sub_dirs[3], sub_dirs[4]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_ret_dir = sub_dirs[5]

        long_ret_dir, renew_dir = cls.sort_lret_ren(sub_dirs[6], sub_dirs[7])

        long_reg_csv = mouse_dir / "long_reg.csv"
        long_reg_tidy_csv = mouse_dir / "long_reg_tidy.csv"
        long_reg_tidy_dataset_id_csv = mouse_dir / "long_reg_tidy_dataset_id.csv"
        long_reg_crop_csv = mouse_dir / "long_reg_crop.csv"
        long_reg_translation_csv = mouse_dir / "long_reg_translation.csv"

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            long_reg_csv=long_reg_csv,
            long_reg_tidy_csv=long_reg_tidy_csv,
            long_reg_tidy_dataset_id_csv=long_reg_tidy_dataset_id_csv,
            long_reg_crop_csv=long_reg_crop_csv,
            long_reg_translation_csv=long_reg_translation_csv,
            cond_dir=cond_dir,
            ret_behavior_dir=ret_behavior_dir,
            ret_injection_dir=ret_injection_dir,
            ext_injection_dir=ext_injection_dir,
            ext_behavior_dir=ext_behavior_dir,
            ext_ret_dir=ext_ret_dir,
            long_ret_dir=long_ret_dir,
            renew_dir=renew_dir,
        )


@dataclass
class OutputMouseDirOFLRepeated(OutputMouseDir):
    mouse_name: str
    mouse_dir: Path

    day0_dir: OutputDir
    day1_dir: OutputDir
    day2_dir: OutputDir
    day3_dir: OutputDir
    day4_dir: OutputDir

    @property
    def day_dirs(self) -> List[OutputDir]:
        return [
            self.day0_dir,
            self.day1_dir,
            self.day2_dir,
            self.day3_dir,
            self.day4_dir,
        ]

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        # filter sub_dirs to only include those that end in six digits

        day0_dir = OutputDir.from_session_dir(mouse_dir / "day0")
        day1_dir = OutputDir.from_session_dir(mouse_dir / "day1")
        day2_dir = OutputDir.from_session_dir(mouse_dir / "day2")
        day3_dir = OutputDir.from_session_dir(mouse_dir / "day3")
        day4_dir = OutputDir.from_session_dir(mouse_dir / "day4")

        long_reg_csv = mouse_dir / "long_reg.csv"
        long_reg_tidy_csv = mouse_dir / "long_reg_tidy.csv"
        long_reg_tidy_dataset_id_csv = mouse_dir / "long_reg_tidy_dataset_id.csv"
        long_reg_crop_csv = mouse_dir / "long_reg_crop.csv"
        long_reg_translation_csv = mouse_dir / "long_reg_translation.csv"

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            day0_dir=day0_dir,
            day1_dir=day1_dir,
            day2_dir=day2_dir,
            day3_dir=day3_dir,
            day4_dir=day4_dir,
            long_reg_csv=long_reg_csv,
            long_reg_tidy_csv=long_reg_tidy_csv,
            long_reg_tidy_dataset_id_csv=long_reg_tidy_dataset_id_csv,
            long_reg_crop_csv=long_reg_crop_csv,
            long_reg_translation_csv=long_reg_translation_csv,
        )


@dataclass
class OutputMouseDirOFLFirst(OutputMouseDir):
    mouse_name: str
    mouse_dir: Path

    day0_dir: OutputDir
    day1_dir: OutputDir
    day2_dir: OutputDir
    day3_dir: OutputDir
    day4_dir: OutputDir

    @property
    def day_dirs(self) -> List[OutputDir]:
        return [
            self.day0_dir,
            self.day1_dir,
            self.day2_dir,
            self.day3_dir,
            self.day4_dir,
        ]

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        # filter sub_dirs to only include those that end in six digits

        day0_dir = OutputDir.from_session_dir(mouse_dir / "day0")
        day1_dir = OutputDir.from_session_dir(mouse_dir / "day1")
        day2_dir = OutputDir.from_session_dir(mouse_dir / "day2")
        day3_dir = OutputDir.from_session_dir(mouse_dir / "day3")
        day4_dir = OutputDir.from_session_dir(mouse_dir / "day4")

        long_reg_csv = mouse_dir / "long_reg.csv"
        long_reg_tidy_csv = mouse_dir / "long_reg_tidy.csv"
        long_reg_tidy_dataset_id_csv = mouse_dir / "long_reg_tidy_dataset_id.csv"
        long_reg_crop_csv = mouse_dir / "long_reg_crop.csv"
        long_reg_translation_csv = mouse_dir / "long_reg_translation.csv"

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            day0_dir=day0_dir,
            day1_dir=day1_dir,
            day2_dir=day2_dir,
            day3_dir=day3_dir,
            day4_dir=day4_dir,
            long_reg_csv=long_reg_csv,
            long_reg_tidy_csv=long_reg_tidy_csv,
            long_reg_tidy_dataset_id_csv=long_reg_tidy_dataset_id_csv,
            long_reg_crop_csv=long_reg_crop_csv,
            long_reg_translation_csv=long_reg_translation_csv,
        )


# def get_paths_on_relative_day(paths, relative_day=0):
#     """
#     Return the paths that occurred on a given day relative to the first path in the sequence.

#     :param paths: List of pathlib.Path objects whose name attribute ends in a date of the format "%m%d%y".
#     :param relative_day: The number of days relative to the first path's date. (e.g., -1 for one day before)
#     :return: List of matched pathlib.Path objects.
#     """
#     if not paths:
#         return []

#     # Extract date from the first path
#     first_path_date_str = paths[0].name[-6:]  # Assuming the last 6 characters have the date
#     first_path_date = datetime.strptime(first_path_date_str, '%m%d%y').date()

#     # Calculate the target date based on the relative_day
#     target_date = first_path_date + timedelta(days=relative_day)
#     target_date_str = target_date.strftime('%m%d%y')

#     # Filter paths that match the target date
#     matching_paths = [path for path in paths if path.name.endswith(target_date_str)]

#     return matching_paths
