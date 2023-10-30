from isx_preprocessing.exporting.dir_copy import DirectoryCopier
from pathlib import Path

SOURCE_DIR = Path(r"D:\raw data")
DEST_DIR = Path(r"F:\Astrocyte\Export")


def main():
    copier = DirectoryCopier(depth=2)
    copier.copy_directories(source=SOURCE_DIR, target=DEST_DIR)


if __name__ == "__main__":
    main()
