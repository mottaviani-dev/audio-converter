import argparse
import logging
from pathlib import Path

from pydub import AudioSegment
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_audio_files(
    source_folder_path,
    output_folder_path,
    input_format,
    output_format,
):
    source_root = Path(source_folder_path)
    output_folder = Path(output_folder_path)
    output_folder.mkdir(parents=True, exist_ok=True)

    audio_paths = []

    for root, _dirs, filenames in source_root.walk():
        for filename in filenames:
            if filename.endswith(f".{input_format}"):
                full_path = Path(root) / filename
                relative_path = full_path.relative_to(source_root)
                audio_paths.append((full_path, relative_path))

    logger.info(
        "Total %s files found: %d",
        input_format.upper(),
        len(audio_paths)
    )

    for full_path, relative_path in tqdm(
        audio_paths,
        desc=f"Converting {input_format.upper()} to {output_format.upper()}"
    ):
        audio = AudioSegment.from_file(full_path, format=input_format)
        output_path = output_folder / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_filename = output_path.with_suffix(f".{output_format}")
        audio.export(out_filename, format=output_format)


def main():
    parser = argparse.ArgumentParser(
        description="Convert audio files between formats."
    )
    parser.add_argument(
        "source_folder",
        type=str,
        help="The folder containing audio files to convert."
    )
    parser.add_argument(
        "output_folder",
        type=str,
        help="The folder to save converted audio files.",
        default=None,
    )
    parser.add_argument(
        "input_format",
        type=str,
        choices=["mp3", "m4a", "ogg", "flac", "wav"],
        help="The audio file format to convert from."
    )
    parser.add_argument(
        "output_format",
        type=str,
        choices=["wav", "mp3", "ogg", "flac"],
        help="The audio file format to convert to."
    )

    args = parser.parse_args()
    if not args.output_folder:
        args.output_folder = (
            f"{args.source_folder}/{args.input_format}_to_{args.output_format}"
        )


    convert_audio_files(
        source_folder_path=args.source_folder,
        output_folder_path=args.output_folder,
        input_format=args.input_format,
        output_format=args.output_format
    )


if __name__ == "__main__":
    main()
