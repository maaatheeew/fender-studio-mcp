# fender-studio-mcp

An unofficial [Model Context Protocol](https://modelcontextprotocol.io/) server
and a small set of audio-to-MIDI workflows for turning rehearsal recordings into
the first draft of a demo in **Fender Studio Pro / PreSonus Studio One**.

> **Unofficial project.** This project is not affiliated with, endorsed by, or
> supported by Fender, PreSonus, or their affiliates. Fender Studio Pro and
> Studio One are trademarks of their respective owners.

The MCP server provides transport, Mackie Control Universal (MCU) mixer
control, command discovery, shortcuts, and macro-file generation. The included
agent skills document a practical workflow for extracting a drum sketch or a
hummed melody to MIDI before arranging it in the DAW.

## What this repository includes

- `src/studio_pro_mcp/` — the Python MCP server.
- `studio-one-devices/` — an optional Studio One control-surface definition.
- `skills/transcribe-drums/` — an agent workflow for rehearsal drums to MIDI.
- `skills/transcribe-hummed-melody/` — an agent workflow for hummed melody to
  MIDI.
- `docs/AUDIO_TRANSCRIPTION.md` — dependency choices, limitations, and a
  repeatable review process.

No songs, recordings, MIDI performances, plug-in databases, key-scheme
exports, credentials, or model weights are included.

## MCP functions and commands

The default server exposes **49 MCP tools**: 9 transport tools, 11 mixer
tools, 23 shortcut-based editing tools, 2 plug-in/macro tools, and 4 command
catalog tools. The tables below list the tools implemented in this repository.
Availability in the catalog does not mean every action has been verified on
every DAW version.

### Transport — 9 tools

These send MCU MIDI commands. All take an empty argument object: `{}`.

| Tool | Action |
| --- | --- |
| `transport_play` | Start playback. |
| `transport_stop` | Stop playback. |
| `transport_record` | Send the Record command; recording depends on the DAW's track arming and input setup. |
| `transport_rewind` | Rewind the transport. |
| `transport_fast_forward` | Fast-forward the transport. |
| `transport_toggle_loop` | Toggle loop/cycle playback. |
| `transport_save` | Send the Save command. |
| `transport_undo` | Send Undo. |
| `transport_redo` | Send Redo. |

### Mixer — 11 tools

`channel` is a zero-based MCU strip index (`0–7`) in the current bank, not a
track name or a persistent song-track ID. `mixer_set_fader` also accepts
`"master"`. Fader `level` is a `0–100` position, not a dB value.

| Tool | Arguments | Action |
| --- | --- | --- |
| `mixer_set_fader` | `channel`, `level` | Set a channel or master fader position. |
| `mixer_toggle_mute` | `channel` | Toggle channel mute. |
| `mixer_toggle_solo` | `channel` | Toggle channel solo. |
| `mixer_toggle_rec_arm` | `channel` | Toggle record arming. |
| `mixer_select_channel` | `channel` | Select a channel strip. |
| `mixer_set_pan` | `channel`, `pan` (`-63–63`) | Send relative pan encoder ticks: negative moves left, positive moves right. This does not set an absolute pan position. |
| `mixer_get_state` | `{}` | Read the server's cached mixer state. |
| `mixer_bank_left` | `{}` | Request the previous bank of eight strips. |
| `mixer_bank_right` | `{}` | Request the next bank of eight strips. |
| `mixer_goto_bank` | `bank` (`0–7`) | Request a specific bank. |
| `mixer_get_bank` | `{}` | Read the server's bank counter and corresponding channel range. |

Mixer readback has limits: faders use DAW feedback when available, otherwise
the last value sent. Mute, solo, and record-arm values are assumed from sent
commands. The bank counter does not establish which tracks the DAW is actually
showing. Verify the target bank and the result in the DAW before relying on
these values. A zero pan tick is not a verified reset-to-center operation.

### Track, event, and session editing — 23 tools

These tools send keyboard shortcuts and act on the current DAW selection and
focus. All take `{}`. Their outcome depends on the active view, shortcut
bindings, and dialogs; an `OK` response confirms dispatch, not the final edit.

| Tool | Action |
| --- | --- |
| `auto_add_audio_track` | Invoke Add Audio Track and confirm its dialog using the configured mapping. |
| `auto_add_audio_track_mono` | Invoke Add Audio Track (mono), using an assigned shortcut. |
| `auto_add_instrument_track` | Invoke Add Instrument Track, using an assigned shortcut. |
| `auto_add_bus_track` | Invoke Add Bus Channel, using an assigned shortcut. |
| `auto_duplicate_track` | Send the configured duplicate shortcut for the selected context. |
| `auto_delete_selected` | Delete the current selection. |
| `auto_undo` | Undo the last action. |
| `auto_redo` | Redo the last undone action. |
| `auto_save` | Save the current song. |
| `auto_save_as` | Open Save As; completing the dialog is a separate step. |
| `auto_new_song` | Open New Song; completing the dialog is a separate step. |
| `auto_toggle_mixer` | Show or hide the mixer. |
| `auto_toggle_browser` | Show or hide the browser. |
| `auto_toggle_editor` | Show or hide the MIDI/audio editor. |
| `auto_select_all` | Select all in the active context. |
| `auto_zoom_in` | Zoom in. |
| `auto_zoom_out` | Zoom out. |
| `auto_zoom_to_fit` | Fit the arrangement in the view. |
| `auto_toggle_loop` | Toggle loop playback through its shortcut. |
| `auto_go_to_start` | Invoke navigation to the song start. |
| `auto_go_to_end` | Invoke navigation to the song end. |
| `auto_split_at_playhead` | Split selected events at the playhead. |
| `auto_quantize` | Quantize selected MIDI notes with the DAW's current grid. |

Track duplication, Save As, and Go to End did not perform their intended
actions in the local Studio Pro 8.2 check with the then-current mappings.
Check your bindings before using them. The mono, instrument, and bus creation
actions need assigned shortcuts if none exist in your exported scheme.

### Plug-ins and macro files — 2 tools

| Tool | Arguments | Action |
| --- | --- | --- |
| `auto_list_plugins` | Optional `category`: `AudioSynth`, `AudioEffect`, or `MusicEffect` | List plug-ins discovered from the local DAW settings/database. |
| `auto_generate_insert_macro` | Required `name`; optional `preset` (default `"default"`) and `mode` (default `1`) | Find a plug-in and write a `.studioonemacro` file for inserting it on selected channels and opening the channel editor. |

Generating an insert macro only writes the file. Reload macros in the DAW,
select the intended channel, and run the generated macro from the MCP group
in the macro toolbar or through an assigned shortcut. This server does not
provide direct editing of an instrument's internal drum kit or plug-in parameters.

### DAW command discovery and execution — 4 tools

| Tool | Arguments | Action |
| --- | --- | --- |
| `studio_one_generate_command_catalog` | Optional `path` and `output` | Parse an exported `.keyscheme` into a local catalog of command names, macros, and shortcuts. Without `path`, try auto-discovery. |
| `studio_one_list_commands` | Optional `filter` | List catalog entries, optionally matching a substring. |
| `studio_one_run_command` | Required `name` | Resolve a command or macro by its label and dispatch it through its shortcut, with a Windows-only command-palette fallback. |
| `studio_one_save_new_version` | `{}` | Resolve Save New Version in the catalog and dispatch it with a dialog confirmation attempt; verify the saved result. |

The catalog is generated per installation, so its command count depends on
your DAW and installed macros. Exact case-insensitive names and unique partial
matches are supported; ambiguous partial matches return candidates. On macOS,
assign a shortcut to commands that do not have one. Windows command-palette
search can select an unintended result, so prefer explicit shortcut bindings.

### Example MCP calls

These are tool names and argument objects to pass through an MCP client,
not shell commands. First export a `.keyscheme` from the DAW's keyboard
shortcut preferences, then generate and inspect its catalog:

```json
{"name": "studio_one_generate_command_catalog", "arguments": {"path": "/absolute/path/to/MyShortcuts.keyscheme"}}
{"name": "studio_one_list_commands", "arguments": {"filter": "Quantize"}}
{"name": "auto_list_plugins", "arguments": {"category": "AudioEffect"}}
```

With the intended song, selection, and MCU bank confirmed, examples of actions
are:

```json
{"name": "transport_play", "arguments": {}}
{"name": "transport_stop", "arguments": {}}
{"name": "mixer_set_fader", "arguments": {"channel": 0, "level": 60}}
{"name": "auto_quantize", "arguments": {}}
```

The current public server has no dedicated tools for reading all MIDI notes,
writing note-by-note arrangements, or importing a MIDI file. Importing a
transcription uses the DAW's normal import workflow or a separately installed
integration.

## Quick start

Requirements: Python 3.10+, Fender Studio Pro or PreSonus Studio One, and a
local MCP client.

```bash
git clone https://github.com/maaatheeew/fender-studio-mcp.git
cd fender-studio-mcp
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

Register the server with an MCP client:

```json
{
  "mcpServers": {
    "fender-studio": {
      "command": "/absolute/path/to/fender-studio-mcp/.venv/bin/fender-studio-mcp"
    }
  }
}
```

On Windows, use `.venv\\Scripts\\fender-studio-mcp.exe` instead.

### MCU setup

On macOS/Linux the server creates virtual MIDI ports called `StudioPro-MCU`.
On Windows, create matching loopback ports before starting the server. The
server opens MIDI ports at startup, even when you only intend to use shortcuts.
Add a **Mackie Control Universal** external device in Studio Pro / Studio One
with the server's output as **Receive From** and its input as **Send To** for
feedback. This connection is needed for the transport and mixer tools.

### Shortcuts and macOS accessibility

Some commands use the DAW's keyboard shortcuts. On macOS, grant Accessibility
permission to the app that launches the MCP server. Exporting your own
`.keyscheme` and running `python -m studio_pro_mcp.keyscheme` makes the server
prefer your actual bindings over its fallback mapping.

Keyboard automation changes the foreground DAW. Review a command before
running it, keep a saved version of valuable sessions, and do not expose an
HTTP instance beyond localhost.

### Server CLI commands

Run these from an activated virtual environment, or use the full path to the
installed executable:

```bash
fender-studio-mcp --help
fender-studio-mcp --version
fender-studio-mcp --list-ports
fender-studio-mcp --transport stdio --port-name StudioPro-MCU
fender-studio-mcp --transport http --http-host 127.0.0.1 --http-port 8765
```

`stdio` is the default transport; HTTP serves `/mcp`. Additional options are
`--message-delay SECONDS` (default `0.02`), `--debug`, and `--no-automation`.
The last option removes the 23 shortcut-based editing tools from the catalog;
command execution and Save New Version remain available and can still send
keystrokes. It is not a global switch disabling keyboard access.

## Music skills: audio recognition and transcription

The two included skills are Markdown workflows for an assistant. They explain
how to use separately installed audio tools, review their output, and prepare
MIDI for a demo. They do not add audio-recognition tools to the MCP server,
install models, or execute transcription on their own.

| Skill | Input | Recognition workflow | Intended output |
| --- | --- | --- | --- |
| [transcribe-drums](skills/transcribe-drums/SKILL.md) | Rehearsal audio, phone video, or an isolated drum stem | Extract WAV with FFmpeg; optionally separate drums with Demucs; detect hits with ADTOF-pytorch; review the beat grid and hits. | A drum MIDI draft, a copy preserving source timing, and a report of tempo/grid assumptions. |
| [transcribe-hummed-melody](skills/transcribe-hummed-melody/SKILL.md) | A short solo vocal, hum, or whistle | Convert to WAV; estimate notes with Basic Pitch; remove false notes and correct timing, durations, and octave errors. | Reviewed melody MIDI plus the raw transcription for comparison. |

### Drum recognition

The drum workflow covers five broad classes: **kick, snare, tom, hi-hat, and
cymbal**. It includes comparing stem and full-mix results, removing duplicate
hits, confirming the song tempo before quantization, and turning repeated
grooves into named clips. Velocity is estimated; specific tom pitches,
hi-hat openness, cymbal types, ghost notes, and articulations need review.

Example request to an assistant:

> Read `skills/transcribe-drums/SKILL.md` and use it to make a drum MIDI draft
> from my rehearsal video. Keep a source-timing version, then prepare a
> separate 120 BPM version with the main grooves in named clips.

### Notes from singing, humming, or whistling

The melody workflow works toward a usable note sketch from a clean solo take.
It includes removing breath/noise detections, joining fragmented sustained
notes, aligning the phrase, and reviewing pitches against the supplied key and
chords. Note detection still needs musical review for intended pitch, rhythm,
phrasing, and octave.

Example request to an assistant:

> Read `skills/transcribe-hummed-melody/SKILL.md` and turn my hummed recording
> into a MIDI melody. Preserve the raw result, check octave jumps, and keep
> the original phrasing before quantizing anything.

To use either workflow, ask your assistant to read the linked `SKILL.md` and
provide the source recording and tempo/key when known. Install the external
tools separately according to their own documentation. The recognition steps
run locally when configured that way; they are separate from DAW control.
See [audio transcription notes](docs/AUDIO_TRANSCRIPTION.md) for dependencies
and review guidance.

## From rehearsal to demo

The transcription skills deliberately produce a **draft**, not a claimed
ground-truth performance. A useful sequence is:

1. Export a WAV from the rehearsal recording.
2. Isolate drums (when needed), transcribe them to a five-class MIDI sketch,
   then correct tempo, bar alignment, and impossible hits.
3. Record a clean hum or whistle, convert its pitch contour to MIDI, and check
   it against the song's key and chords.
4. Import reviewed MIDI into Studio Pro / Studio One and arrange named clips.

See [audio transcription notes](docs/AUDIO_TRANSCRIPTION.md) and the two
skills in [`skills/`](skills/).

## Development

```bash
pytest
ruff check src tests
mypy src
```

The test suite is self-contained: it must not read an installed DAW profile,
plug-in cache, or a real song.

## Credits and related projects

This project builds on and is grateful to:

- [tiwadara/StudioOneMcp](https://github.com/tiwadara/StudioOneMcp), the
  original MIT-licensed Studio One MCP foundation.
- [pajdarova/FenderStudioProMCP](https://github.com/pajdarova/FenderStudioProMCP),
  the MIT-licensed Fender Studio Pro fork that this codebase derives from.
- [xavriley/ADTOF-pytorch](https://github.com/xavriley/ADTOF-pytorch) and the
  ADTOF research project, suggested as an external drum-transcription engine.
- [facebookresearch/demucs](https://github.com/facebookresearch/demucs),
  suggested for optional source separation.
- [spotify/basic-pitch](https://github.com/spotify/basic-pitch), suggested for
  hummed-melody transcription.

The external projects above are not bundled here. Their licences, model terms,
and installation instructions apply independently.

## Contributing

Contributions are welcome: bug reports, platform testing, safer command
dispatch, documentation, and better transcription-review workflows are all
useful. Please read [CONTRIBUTING.md](CONTRIBUTING.md), add tests for code
changes, and avoid committing recordings, exported DAW settings, credentials,
or copyrighted reference material.

## License

MIT — see [LICENSE](LICENSE). Upstream copyright notices are retained.
