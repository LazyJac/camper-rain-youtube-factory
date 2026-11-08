import subprocess
import numpy as np
from scipy.ndimage import map_coordinates

W_FULL, H_FULL = 3840, 2160
Y0, Y1 = 680, 1140
X0, X1 = 2240, 2880
H_CROP, W_CROP = Y1 - Y0, X1 - X0
yy, xx = np.mgrid[0:H_CROP, 0:W_CROP].astype(np.float32)

# Target fixed position of the original buoy attached to the boat (in crop coords: cx=56, cy=391 -> 2296, 1071 in 4K)
BX_TARGET, BY_TARGET = 56.0, 391.0

def process_patch(crop_rgb, t_sec, mode="intro"):
    """
    1. Cancels out the slight raw Veo drift of the original buoy between t=4.2s and t=7.8s
       so the original buoy attached to the boat stays 100% locked at (cx=56, cy=391).
    2. Applies a smooth, zero-bend 3D weathervane pivot of the sailboat around that fixed original buoy.
    """
    # Measure/model the smooth raw drift of the buoy in veo_native_4k_upsampled_02.mp4:
    # For t <= 4.0s: buoy is at (56, 391) -> drift = (0, 0)
    # For t from 4.0s to 7.5s: raw buoy drifts smoothly to (71, 383) -> drift = (+15.0, -8.0)
    drift_progress = np.clip((t_sec - 4.0) / 3.4, 0.0, 1.0)
    drift_progress = drift_progress * drift_progress * (3.0 - 2.0 * drift_progress) # smoothstep
    raw_dx_buoy = 15.0 * drift_progress
    raw_dy_buoy = -8.0 * drift_progress

    # Envelope around the buoy + mooring line + bow (cx=20..135, cy=300..430) to lock the buoy at (56, 391)
    # To shift the drifted buoy from (56 + raw_dx, 391 + raw_dy) back to (56, 391), we sample at (xx + raw_dx, yy + raw_dy)!
    env_buoy_lock = np.exp(-((xx - 64.0)**2 / (42.0**2) + (yy - 386.0)**2 / (28.0**2)))

    # Weathervane angle psi(t) around the locked buoy (56, 391):
    if mode == "intro":
        # As the storm wind arrives (t=1.5..7.8s), the boat gently weathervanes with the wind
        wind_prog = np.clip((t_sec - 1.2) / 6.4, 0.0, 1.0)
        psi = 0.52 * np.sin(wind_prog * np.pi * 0.5)
    else:
        # Storm loop clip (t in 3.6..7.8s -> local_t in 0..4.2s): smooth oscillation as wind gusts vary
        local_norm = np.clip((t_sec - 3.6) / 4.2, 0.0, 1.0)
        psi = 0.52 * np.cos(local_norm * 2.0 * np.pi)

    rx = np.maximum(0.0, xx - BX_TARGET) / 515.0
    env_y = (1.0 / (1.0 + np.exp(-(yy - 216.0) / 6.0))) * (1.0 / (1.0 + np.exp((yy - 420.0) / 8.0)))
    env_x = (1.0 / (1.0 + np.exp(-(xx - (BX_TARGET + 12.0)) / 8.0))) * (1.0 / (1.0 + np.exp((xx - 595.0) / 12.0)))
    env_boat = env_y * env_x * (1.0 - 0.85 * env_buoy_lock)

    dy_boat = psi * 9.5 * (rx ** 1.15) * env_boat
    rx_aft = np.maximum(0.0, xx - 305.0) / 270.0
    env_aft = (1.0 / (1.0 + np.exp(-(yy - 245.0) / 6.0))) * env_x * (1.0 / (1.0 + np.exp(-(xx - 315.0) / 10.0)))
    dx_boat = (-abs(psi) * 5.5 * (rx_aft ** 1.2) + psi * 2.0 * rx_aft) * env_aft

    # Combine buoy stabilization + boat weathervane pivot
    sample_x = np.clip(xx + raw_dx_buoy * env_buoy_lock - dx_boat, 0, W_CROP - 1)
    sample_y = np.clip(yy + raw_dy_buoy * env_buoy_lock - dy_boat, 0, H_CROP - 1)

    warped = np.empty_like(crop_rgb)
    for c in range(3):
        warped[:, :, c] = map_coordinates(crop_rgb[:, :, c], [sample_y, sample_x], order=1, mode="nearest")
    return warped

def build_clip(in_path, out_path, ss=0.0, dur=None, mode="intro"):
    cmd_in = ["ffmpeg", "-v", "error"]
    if ss > 0:
        cmd_in += ["-ss", f"{ss:.3f}"]
    cmd_in += ["-i", in_path]
    if dur is not None:
        cmd_in += ["-t", f"{dur:.3f}"]
    cmd_in += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]

    cmd_out = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W_FULL}x{H_FULL}", "-r", "24",
        "-i", "-",
        "-c:v", "h264_videotoolbox", "-b:v", "45M", "-pix_fmt", "yuv420p",
        out_path
    ]

    p_in = subprocess.Popen(cmd_in, stdout=subprocess.PIPE)
    p_out = subprocess.Popen(cmd_out, stdin=subprocess.PIPE)

    frame_bytes = W_FULL * H_FULL * 3
    idx = 0
    while True:
        raw = p_in.stdout.read(frame_bytes)
        if len(raw) < frame_bytes:
            break
        frame = np.frombuffer(raw, dtype=np.uint8).reshape((H_FULL, W_FULL, 3)).copy()
        t_sec = ss + (idx / 24.0)
        crop = frame[Y0:Y1, X0:X1].astype(np.float32)
        warped = process_patch(crop, t_sec, mode=mode)
        frame[Y0:Y1, X0:X1] = np.clip(warped, 0, 255).astype(np.uint8)
        p_out.stdin.write(frame.tobytes())
        idx += 1

    p_in.stdout.close()
    p_out.stdin.close()
    p_in.wait()
    p_out.wait()
    print(f"Built {out_path} ({idx} frames)")

if __name__ == "__main__":
    src = "assets/episodes/02_masurian_lakes_dusk/veo_native_4k_upsampled_02.mp4"
    build_clip(src, "assets/episodes/02_masurian_lakes_dusk/_veo4k_intro_fixed_buoy.mp4", ss=0.0, dur=7.8, mode="intro")
    build_clip(src, "assets/episodes/02_masurian_lakes_dusk/_veo4k_storm_swing_back.mp4", ss=3.6, dur=4.2, mode="storm_loop")
