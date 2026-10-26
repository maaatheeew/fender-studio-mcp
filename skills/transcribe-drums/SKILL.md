# Transcribe rehearsal drums to MIDI

Use this workflow when someone wants a usable drum **draft** from a rehearsal
recording, phone video, or an isolated drum stem.

## Input and output

- Input: a user-supplied audio/video file and the target song tempo if known.
- Output: a MIDI draft, an unquantized reference copy, and a short report of
  assumptions and limitations.

Never upload or publish the source recording without explicit permission.

## Workflow

1. Confirm that the user owns or may process the recording. Preserve the
   original file and work on a copy.
2. Extract a WAV, for example:

   ```bash
   ffmpeg -i rehearsal.mov -ar 44100 -ac 2 rehearsal.wav
   ```

3. If guitars and vocals obscure the kit, make an optional drum stem with an
   installed source separator such as Demucs. Keep both the full-mix and stem
   results for comparison.
4. Run a local automatic drum transcriber such as ADTOF-pytorch. Treat its
   onsets as candidates for five broad classes: kick, snare, tom, hi-hat, and
   cymbal.
5. Estimate the beat grid from the full mix and align the candidates to it.
   Remove duplicate hits and very low-confidence stem-only hits.
6. Export two MIDI files: one retaining source timing and one quantized only
   after the intended tempo is confirmed.
7. Listen through every fill and transition. Correct impossible overlaps (for
   example a closed hi-hat remaining under a two-hand fill), verify downbeats,
   and simplify repeated sections into named, reusable clips.

## Deliverable checklist

- State the source duration, assumed tempo, time signature, grid, and model.
- State that velocity is an estimate, not recovered performance data.
- Identify unmodelled details: tom pitch, open/closed hi-hat, cymbal type,
  ghost notes, and articulations.
- Do not report automatic detection as a verified transcription until a person
  has listened and corrected it.
