import os
import argparse
from pydub import AudioSegment
from tqdm import tqdm

def convert_audio_files(source_folder, input_format, output_format):
    audio_paths = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(f".{input_format}"):
                audio_paths.append(os.path.join(root, file))

    print(f"Total {input_format.upper()} files found: {len(audio_paths)}")

    for full_path in tqdm(audio_paths, desc=f'Converting {input_format.upper()} to {output_format.upper()}'):
        audio = AudioSegment.from_file(full_path, format=input_format)
        audio.export(full_path, format=output_format)
        os.remove(full_path)

def main():
    parser = argparse.ArgumentParser(description="Convert audio files between formats.")
    parser.add_argument("source_folder", type=str, help="The folder containing audio files to convert.")
    parser.add_argument("input_format", type=str, choices=["mp3", "m4a", "ogg", "flac", "wav"], help="The audio file format to convert from.")
    parser.add_argument("output_format", type=str, choices=["wav", "mp3", "ogg", "flac"], help="The audio file format to convert to.")
    
    args = parser.parse_args()

    convert_audio_files(args.source_folder, args.input_format, args.output_format)

if __name__ == "__main__":
    main()
