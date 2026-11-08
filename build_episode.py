#!/usr/bin/env python3
from __future__ import annotations
"""
Main CLI runner for the Camper Rain YouTube Factory.
Takes a raw 10s Google Flow video clip (`google_flow_raw_10s.mp4`) for a given scene ID
and produces two distinct, anti-duplicate YouTube packages (Account 1: Sleep, Account 2: Cozy Chill)
with custom acoustic/ambient audio mixes, thumbnails, 15s previews, and vidIQ SEO metadata.
"""

import argparse
import json
from pathlib import Path
from src.video_builder import render_dual_youtube_videos
from src.yt_packager import generate_youtube_packages


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dual YouTube packages for a Camper Rain episode.")
    parser.add_argument("--scene-id", default="01_pacific_cliff_storm", help="Scene ID from prompts/camper_scenes.json")
    parser.add_argument(
        "--raw-clip",
        default=None,
        help="Path to the raw 10s Google Flow video clip (defaults to assets/episodes/<scene-id>/google_flow_raw_10s.mp4)",
    )
    parser.add_argument("--sleep-seconds", type=int, default=4500, help="Duration for Account 1 Sleep video (default: 4500s = 1h 15m)")
    parser.add_argument("--chill-seconds", type=int, default=3900, help="Duration for Account 2 Chill video (default: 3900s = 1h 05m)")
    parser.add_argument("--metadata-only", action="store_true", help="Only regenerate YouTube SEO metadata & vidIQ report")
    args = parser.parse_args()

    out_dir = f"output/{args.scene_id}"
    if args.metadata_only:
        res = generate_youtube_packages(args.scene_id, out_dir, args.sleep_seconds, args.chill_seconds)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    raw_clip = args.raw_clip or f"assets/episodes/{args.scene_id}/google_flow_raw_10s.mp4"
    if not Path(raw_clip).exists():
        raise FileNotFoundError(f"Raw Google Flow clip not found: {raw_clip}")

    res = render_dual_youtube_videos(
        raw_clip_path=raw_clip,
        scene_id=args.scene_id,
        duration_sleep_sec=args.sleep_seconds,
        duration_chill_sec=args.chill_seconds,
        out_dir=out_dir,
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
