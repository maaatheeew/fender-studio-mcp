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

### Optional MCU setup

Create or choose a virtual MIDI port called `StudioPro-MCU`, then add a
**Mackie Control Universal** external device in Studio Pro / Studio One with
that port as **Receive From**. MCU is used for mixer and transport controls;
the server can still expose non-MCU functions without it.

### Shortcuts and macOS accessibility

Some commands use the DAW's keyboard shortcuts. On macOS, grant Accessibility
permission to the app that launches the MCP server. Exporting your own
`.keyscheme` and running `python -m studio_pro_mcp.keyscheme` makes the server
prefer your actual bindings over its fallback mapping.

Keyboard automation changes the foreground DAW. Review a command before
running it, keep a saved version of valuable sessions, and do not expose an
HTTP instance beyond localhost.

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
