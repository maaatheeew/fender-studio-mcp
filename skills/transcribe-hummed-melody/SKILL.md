# Transcribe a hummed melody to MIDI

Use this workflow when someone sings, hums, or whistles a melody and wants a
MIDI sketch for a rehearsal demo.

## Capture guidance

Ask for a short, dry, monophonic recording. A spoken count-in helps alignment.
Avoid a backing track, reverb, tuning effects, and other voices when a separate
guide vocal can be recorded. Keep the original recording private unless the
user explicitly asks to publish it.

## Workflow

1. Convert the take to WAV while preserving a copy of the original.
2. Run a local pitch-to-MIDI model such as Basic Pitch. For its installed CLI,
   the usual pattern is:

   ```bash
   basic-pitch output-directory melody.wav
   ```

3. Open the resulting MIDI beside the audio. Remove breath noise and very
   short false notes; join notes that belong to one sustained pitch.
4. Set the correct tempo and align the first intentional note. Do not
   mechanically quantize all attacks: the melody's phrasing may be deliberate.
5. Compare the pitches to the song's stated key and chords. Correct octave
   jumps, passing tones that were missed, and pitches that are not musically
   intended.
6. Import the reviewed result to an instrument track as a clearly named MIDI
   clip. Retain a separate `raw` version for comparison.

## Report honestly

Mention the model used, tempo assumption, and each musical decision made after
transcription. A pitch model estimates frequency; it does not infer intended
harmony, lyrics, note spelling, articulation, or arrangement.
