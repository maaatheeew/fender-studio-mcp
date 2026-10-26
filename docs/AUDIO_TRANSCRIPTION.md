# Audio-to-MIDI workflows

The repository ships **agent instructions**, not transcription models or audio
data. They make an intentional distinction between an automatic estimate and a
part that a musician can actually use in a demo.

## Drums from a rehearsal recording

Recommended external components:

1. `ffmpeg` — extract a WAV from a phone video or rehearsal capture.
2. [Demucs](https://github.com/facebookresearch/demucs) — optionally isolate a
   drum stem before transcription.
3. [ADTOF-pytorch](https://github.com/xavriley/ADTOF-pytorch) — infer onset
   candidates for kick, snare, tom, hi-hat, and cymbal.
4. `pretty_midi` or a DAW — remove duplicates, set the tempo grid, and export
   a normal MIDI file.

Automatic drum output is especially fragile around fills, cymbal articulations,
bleed, and tempo changes. It is a starting point for reconstructing a groove,
not a substitute for listening. Keep source timing until the musical review is
finished; quantize a copy, not the only result.

## Melody from a hum or whistle

[Basic Pitch](https://github.com/spotify/basic-pitch) is a practical external
baseline. A short, dry, monophonic take is much more reliable than a full-band
recording. Record a count-in, leave a little silence at both ends, and avoid
effects, double tracking, and accompaniment where possible.

Pitch detection cannot know the intended scale, rhythmic feel, or note lengths.
Compare the generated MIDI to the key and harmony, then edit the attack times,
durations, and wrong octave jumps before importing it into the DAW.

## Attribution and installation

ADTOF-pytorch, Demucs, and Basic Pitch are separate projects. Install them in
their own environments, read their current licences and model terms, and do
not commit their source, weights, or any audio to this repository unless those
terms explicitly allow it.
