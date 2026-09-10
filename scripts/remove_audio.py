import os
import subprocess


def remove_audio_to_folder() -> None:
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "output_silent")

    os.makedirs(output_dir, exist_ok=True)

    files = [name for name in os.listdir(current_dir) if name.lower().endswith(".mov")]
    if not files:
        print("No .mov files found in this directory.")
        return

    print(f"Found {len(files)} files. Starting FFmpeg audio removal...")

    for filename in files:
        input_path = os.path.join(current_dir, filename)
        output_path = os.path.join(output_dir, filename)
        command = [
            "ffmpeg",
            "-i",
            input_path,
            "-an",
            "-vcodec",
            "copy",
            output_path,
            "-y",
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"Processed: {filename}")
        except Exception as exc:
            print(f"Error processing {filename}: {exc}")

    print(f"Done. Silent videos are in: {output_dir}")


if __name__ == "__main__":
    remove_audio_to_folder()
