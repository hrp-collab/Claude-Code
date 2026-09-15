#!/usr/bin/env python3
"""Render a slow camera move over a still image. Costs nothing — no API, no credits.

For an ink-and-wash motion comic this beats AI image-to-video on the shots that are
just a camera move: a real crop over a fixed painting has zero frame-to-frame texture
drift, so the paper grain and hatching cannot boil.

    python3 scripts/kenburns.py stills/s01.png -o out/s01.mp4 -d 6 -m push-in
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

MOVES = ("push-in", "pull-out", "pan-left", "pan-right", "drift-up", "drift-down", "hold")


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found. Install it, or: pip install imageio-ffmpeg")


def build_filter(move: str, frames: int, w: int, h: int, fps: int, zoom: float) -> str:
    # zoompan samples the source once per output frame; pre-scaling to 4x gives it
    # enough pixels to interpolate smoothly instead of stepping visibly.
    pre = f"scale={w * 4}:{h * 4}:flags=lanczos"
    step = (zoom - 1.0) / frames

    if move == "push-in":
        z, x, y = f"1+{step}*on", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif move == "pull-out":
        z, x, y = f"{zoom}-{step}*on", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif move in ("pan-left", "pan-right"):
        z = f"{zoom}"
        travel = f"(iw-iw/zoom)*on/{frames}"
        x = travel if move == "pan-right" else f"(iw-iw/zoom)-{travel}"
        y = "ih/2-(ih/zoom/2)"
    elif move in ("drift-up", "drift-down"):
        z = f"{zoom}"
        travel = f"(ih-ih/zoom)*on/{frames}"
        x = "iw/2-(iw/zoom/2)"
        y = travel if move == "drift-down" else f"(ih-ih/zoom)-{travel}"
    else:  # hold
        z, x, y = "1.0", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"

    zoompan = f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={w}x{h}:fps={fps}"
    return f"{pre},{zoompan},format=yuv420p"


def main() -> None:
    p = argparse.ArgumentParser(description="Slow camera move over a still image.")
    p.add_argument("image", type=Path)
    p.add_argument("-o", "--out", type=Path, required=True)
    p.add_argument("-d", "--duration", type=float, default=6.0)
    p.add_argument("-m", "--move", choices=MOVES, default="push-in")
    p.add_argument("--zoom", type=float, default=1.12, help="end zoom; keep subtle")
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    args = p.parse_args()

    if not args.image.exists():
        sys.exit(f"no such image: {args.image}")

    frames = max(1, int(args.duration * args.fps))
    args.out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg_bin(), "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-i", str(args.image),
        "-t", str(args.duration),
        "-vf", build_filter(args.move, frames, args.width, args.height, args.fps, args.zoom),
        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-r", str(args.fps), str(args.out),
    ]
    subprocess.run(cmd, check=True)
    print(f"{args.out}  {args.duration}s  {args.move}  {args.width}x{args.height}@{args.fps}")


if __name__ == "__main__":
    main()
