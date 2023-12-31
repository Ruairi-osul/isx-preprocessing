from pathlib import Path
from dataclasses import dataclass
import datetime
from .isx_session_dir import ISXDir

from typing import Union, Any, Optional, List, Tuple


@dataclass
class IsxMouseDir:
    """
    A representation of a directory containing subdirectories for each session of a mouse.

    Subdirectories are expected to be ISXDirs, and will be parsed as such.

    Expected directory structure:
    ├── .
    │   ├── session_1
    │   │   ├── some_video.isxd
    │   │   ├── some_video_downsample.isxd
            ...
    │   ├── session_2
    │   │   ├── some_video.isxd
    │   │   ├── some_video_downsample.isxd
            ...
    │   ├── session_3
    │   │   ├── some_video.isxd
    │   │   ├── some_video_downsample.isxd
            ...

    """

    mouse_name: str
    mouse_dir: Path

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        raise NotImplementedError


@dataclass
class AstrocyteSet1IsxMouseDir(IsxMouseDir):
    mouse_name: str
    mouse_dir: Path

    hab_cage_dir: ISXDir
    hab_cs_dir: ISXDir
    cond_dir: ISXDir
    ret_injection_dir: ISXDir
    ret_behavior_dir: ISXDir
    ext_injection_dir: ISXDir
    ext_behavior_dir: ISXDir
    ext_ret_dir: ISXDir
    long_ret_dir: ISXDir
    renew_dir: ISXDir

    @property
    def day_dirs(self) -> List[ISXDir]:
        return [
            self.hab_cs_dir,
            self.cond_dir,
            self.ret_behavior_dir,
            self.ext_behavior_dir,
            self.ext_ret_dir,
            self.long_ret_dir,
            self.renew_dir,
        ]

    # @staticmethod
    # def sort_lret_ren(session_dir1: Path, session_dir2: Path) -> Tuple[Path, Path]:
    #     if "ren" in session_dir1.name.lower():
    #         return session_dir2, session_dir1
    #     else:
    #         return session_dir1, session_dir2

    @staticmethod
    def sort_lret_ren(
        session_dir1: ISXDir, session_dir2: ISXDir
    ) -> Tuple[ISXDir, ISXDir]:
        if "ren" in session_dir1.session_dir.name.lower():
            return session_dir2, session_dir1
        else:
            return session_dir1, session_dir2

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        # filter sub_dirs to only include those that end in six digits
        sub_dirs = [
            ISXDir.from_session_dir(d)
            for d in mouse_dir.glob("*")
            if d.is_dir() and d.name[-6:].isdigit()
        ]

        if len(sub_dirs) != 10:
            raise ValueError("Incorrect number of directories in mouse directory.")

        # order by date, they are in MMDDYY format
        sub_dirs = sorted(
            sub_dirs,
            key=lambda d: datetime.datetime.strptime(d.session_dir.name[-6:], "%m%d%y"),
        )

        hab_cage_dir = sub_dirs[0]
        hab_cs_dir = sub_dirs[1]
        cond_dir = sub_dirs[2]
        ret_behavior_dir, ret_injection_dir = sorted(
            (sub_dirs[3], sub_dirs[4]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_behavior_dir, ext_injection_dir = sorted(
            (sub_dirs[5], sub_dirs[6]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_ret_dir = sub_dirs[7]

        long_ret_dir, renew_dir = cls.sort_lret_ren(sub_dirs[7], sub_dirs[8])

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            hab_cage_dir=hab_cage_dir,
            hab_cs_dir=hab_cs_dir,
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
class AstrocyteSet2IsxMouseDir(IsxMouseDir):
    mouse_name: str
    mouse_dir: Path

    hab_cage_dir: ISXDir
    hab_cs_dir: ISXDir
    cond_dir: ISXDir
    ret_injection_dir: ISXDir
    ret_behavior_dir: ISXDir
    ext_injection_dir: ISXDir
    ext_behavior_dir: ISXDir
    ext_ret_dir: ISXDir
    long_ret_dir: ISXDir
    renew_dir: ISXDir

    @property
    def day_dirs(self) -> List[ISXDir]:
        return [
            self.hab_dir,
            self.cond_dir,
            self.ret_behavior_dir,
            self.ext_behavior_dir,
            self.ext_ret_dir,
            self.long_ret_dir,
            self.renew_dir,
        ]

    @staticmethod
    def sort_lret_ren(
        session_dir1: ISXDir, session_dir2: ISXDir
    ) -> Tuple[ISXDir, ISXDir]:
        if "ren" in session_dir1.session_dir.name.lower():
            return session_dir2, session_dir1
        else:
            return session_dir1, session_dir2
    
    
    @staticmethod
    def sort_hab_cage_tone(session_dir1: ISXDir, session_dir2: ISXDir) -> Tuple[ISXDir, ISXDir]:
        if "tone" not in session_dir1.session_dir.name.lower():
            return session_dir1, session_dir2
        else:
            return session_dir2, session_dir2

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        # filter sub_dirs to only include those that end in six digits
        sub_dirs = [
            ISXDir.from_session_dir(d)
            for d in mouse_dir.glob("*")
            if d.is_dir() and d.name[-6:].isdigit()
        ]

        if len(sub_dirs) != 10:
            print(len(sub_dirs))
            sub_dirs = sorted(
                sub_dirs,
                key=lambda d: datetime.datetime.strptime(
                    d.session_dir.name[-6:], "%m%d%y"
                ),
            )
            print([sub_dirs.session_dir.name for sub_dirs in sub_dirs])
            raise ValueError("Incorrect number of directories in mouse directory.")

        # order by date, they are in MMDDYY format
        sub_dirs = sorted(
            sub_dirs,
            key=lambda d: datetime.datetime.strptime(d.session_dir.name[-6:], "%m%d%y"),
        )

        hab_cage_dir, hab_cs_dir = cls.sort_hab_cage_tone(sub_dirs[0], sub_dirs[1])
        cond_dir = sub_dirs[2]
        ret_behavior_dir, ret_injection_dir = sorted(
            (sub_dirs[3], sub_dirs[4]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_behavior_dir, ext_injection_dir = sorted(
            (sub_dirs[5], sub_dirs[6]),
            key=lambda x: len(x.session_dir.name),
            reverse=True,
        )
        ext_ret_dir = sub_dirs[7]
        long_ret_dir, renew_dir = cls.sort_lret_ren(sub_dirs[8], sub_dirs[9])

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            hab_cage_dir=hab_cage_dir,
            hab_cs_dir=hab_cs_dir,
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
class OFLRepeatedIsxMouseDir(IsxMouseDir):
    mouse_name: str
    mouse_dir: Path

    day0_dir: ISXDir
    day1_dir: ISXDir
    day2_dir: ISXDir
    day3_dir: ISXDir
    day4_dir: ISXDir

    @property
    def day_dirs(self) -> List[ISXDir]:
        return [
            self.day0_dir,
            self.day1_dir,
            self.day2_dir,
            self.day3_dir,
            self.day4_dir,
        ]

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        day0_dir = ISXDir.from_session_dir(mouse_dir / "day0")
        day1_dir = ISXDir.from_session_dir(mouse_dir / "day1")
        day2_dir = ISXDir.from_session_dir(mouse_dir / "day2")
        day3_dir = ISXDir.from_session_dir(mouse_dir / "day3")
        day4_dir = ISXDir.from_session_dir(mouse_dir / "day4")

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            day0_dir=day0_dir,
            day1_dir=day1_dir,
            day2_dir=day2_dir,
            day3_dir=day3_dir,
            day4_dir=day4_dir,
        )


@dataclass
class OFLFirstIsxMouseDir(IsxMouseDir):
    mouse_name: str
    mouse_dir: Path

    day0_dir: ISXDir
    day1_dir: ISXDir
    day2_dir: ISXDir
    day3_dir: ISXDir
    day4_dir: ISXDir

    @property
    def day_dirs(self) -> List[ISXDir]:
        return [
            self.day0_dir,
            self.day1_dir,
            self.day2_dir,
            self.day3_dir,
            self.day4_dir,
        ]

    @classmethod
    def from_mouse_dir(cls, mouse_dir: Path):
        day0_dir = ISXDir.from_session_dir(mouse_dir / "day0")
        day1_dir = ISXDir.from_session_dir(mouse_dir / "day1")
        day2_dir = ISXDir.from_session_dir(mouse_dir / "day2")
        day3_dir = ISXDir.from_session_dir(mouse_dir / "day3")
        day4_dir = ISXDir.from_session_dir(mouse_dir / "day4")

        return cls(
            mouse_name=mouse_dir.name,
            mouse_dir=mouse_dir,
            day0_dir=day0_dir,
            day1_dir=day1_dir,
            day2_dir=day2_dir,
            day3_dir=day3_dir,
            day4_dir=day4_dir,
        )
