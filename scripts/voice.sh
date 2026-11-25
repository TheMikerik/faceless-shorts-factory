#!/usr/bin/env bash
# Lokální úprava hlasu: audio/voice_original.mp3 (raw) -> audio/voice.mp3
# 1) odstraní ticho/mezery mezi větami, 2) zrychlí VŽDY alespoň 1.25x, a víc, pokud by výsledek přesáhl MAX sekund (tvrdý strop).
# Použití: scripts/voice.sh [raw.mp3] [out.mp3] [max_sekund=35]
#   max_sekund=0 -> jen odstraní ticho, nezrychluje (long-form)
set -euo pipefail
IN="${1:-audio/voice_original.mp3}"; OUT="${2:-audio/voice.mp3}"; MAX="${3:-35}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
# ticho delší než 0.1 s se zkrátí na 0.06 s (slova se nelepí, ale žádná mezera)
ffmpeg -y -loglevel error -i "$IN" -af "silenceremove=stop_periods=-1:stop_duration=0.1:stop_threshold=-40dB:stop_silence=0.06" "$TMP/trim.wav"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/trim.wav")
# cíl MAX - 0.5 s kvůli rezervě, minimální tempo 1.25x (atempo zachovává výšku hlasu)
RATE=$(python3 -c "d=$DUR;m=${MAX};print(1.0 if m<=0 else round(max(1.25,d/(m-0.5)),4))")
ffmpeg -y -loglevel error -i "$TMP/trim.wav" -filter:a "atempo=$RATE" -b:a 192k "$OUT"
echo "raw: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")s -> bez mezer: ${DUR}s -> tempo x$RATE -> $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s ($OUT)"
