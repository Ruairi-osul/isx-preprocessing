from isx_preprocessing.exporting import DirectoryCopier
from pathlib import Path

SOURCE_DIR = Path(r"E:\OFL\Raw ISX data")
DEST_DIR = Path(r"F:\Raw OFL")


def main():
    copier = DirectoryCopier(depth=2)
    copier.copy_directories(source=SOURCE_DIR, target=DEST_DIR)


if __name__ == "__main__":
    main()
