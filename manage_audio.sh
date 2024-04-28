#!/bin/bash

# Prompt user
run_conversion_script() {
    echo "Running conversion script..."
    read -p "Enter source folder path: " src_folder

    echo "Select the input audio format:"
    select format_option in "mp3" "m4a" "ogg" "flac" "wav"; do
        case $format_option in
            mp3|m4a|ogg|flac|wav) break;;
            *) echo "Please select a valid input format.";;
        esac
    done

    echo "Select the output audio format:"
    select output_format in "wav" "mp3" "ogg" "flac"; do
        case $output_format in
            wav|mp3|ogg|flac) break;;
            *) echo "Please select a valid output format.";;
        esac
    done

    python3 convert.py "$src_folder" "$format_option" "$output_format"
}

run_conversion_script