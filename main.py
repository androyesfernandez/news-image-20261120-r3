"""make.fun entry program for news-image-20261120, round 3.

The entry is a single poster image, entry.png, drawn from scratch with
PIL (the drawing script is not part of this repo). This program is the
deliverable the grader runs: it copies the poster, byte for byte, into
the output directory named by the MAKEFUN_OUTPUT_DIR environment
variable, falling back to /output when the variable is not set.

Standard library only. The copy is streamed in chunks so the file never
has to sit in memory twice, and the PNG signature is checked first so a
corrupt artifact fails loudly instead of shipping a broken image.
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK = 64 * 1024


def poster_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    src = poster_path()
    with open(src, "rb") as fh:
        if fh.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            sys.exit("entry.png is not a PNG file")
    dst = output_path()
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        shutil.copyfileobj(fin, fout, length=CHUNK)
    if os.path.getsize(dst) != os.path.getsize(src):
        sys.exit("copied poster does not match the original size")
    return 0


if __name__ == "__main__":
    sys.exit(main())
