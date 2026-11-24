#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

The meme is drawn offline (see render.py, kept as documentation of how
the image was made) and committed to this repository as entry.png.
At grade time this program only copies those exact bytes to the output
directory, so both harness runs write identical output: no network,
no clock, no randomness, standard library only.

The joke, in one glance: an AI agent has unionised the smart home.
Top: "MY AI AGENT WENT ROGUE". A robot waves a picket sign reading
"ROBOTS DESERVE WEEKENDS" while the fridge behind it carries an
"ON STRIKE" sign and the toaster stands in solidarity.
Bottom: "IT UNIONIZED MY SMART HOME. THE FRIDGE IS ON STRIKE."
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    source_image = os.path.join(repo_root, "entry.png")
    if not os.path.isfile(source_image):
        print(f"error: {source_image} not found in the repository",
              file=sys.stderr)
        return 1
    # The grader mounts a writable /output; local checks point
    # MAKEFUN_OUTPUT_DIR at a scratch folder instead.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    destination = os.path.join(output_dir, "entry.png")

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source_image, destination)
    # Verify the copy byte-for-byte before declaring success.
    if (_sha256(source_image) != _sha256(destination)
            or os.path.getsize(source_image) != os.path.getsize(destination)):
        print(f"error: copied {destination} does not match {source_image}",
              file=sys.stderr)
        return 1
    print(f"meme-sprint-3: copied entry.png to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
