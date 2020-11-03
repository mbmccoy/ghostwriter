#!/usr/bin/env bash
set -ex

TEMP_DIR=$(mktemp -d)
FILE_NAME=$(basename -- "$1")
DIR_NAME=$(dirname -- "$1")

BASE_FILE_NAME="${FILE_NAME%.*}"

OUTPUT_FILE_NAME="${DIR_NAME}"/"${BASE_FILE_NAME}".gif
STAGING_FILE_NAME="${TEMP_DIR}"/"${BASE_FILE_NAME}".gif


mplayer -ao null "${1}" -vo jpeg:outdir="${TEMP_DIR}"
convert  "${TEMP_DIR}"/* "${STAGING_FILE_NAME}"
convert "${STAGING_FILE_NAME}" -fuzz 10% -layers Optimize "${OUTPUT_FILE_NAME}"

# Clean up temp dir
rm -rf "${TEMP_DIR}"
