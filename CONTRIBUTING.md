# Contributing

Thanks for improving `fender-studio-mcp`.

## Before opening a pull request

1. Keep changes focused and describe the Studio Pro / Studio One version and
   operating system used for any live verification.
2. Run `pytest`, `ruff check src tests`, and `mypy src`.
3. Add or update tests for behavioral changes. Unit tests must use fixtures,
   never a local DAW profile, plug-in cache, song, or external device.
4. Explain any command that can change a DAW session and how a user can verify
   the result.

## Privacy and licensing

Do not commit recordings, song files, MIDI performances, screenshots with
personal information, `.keyscheme` exports, plug-in inventories, credentials,
or generated model weights. Do not add third-party code or models unless their
licence permits redistribution and the attribution is documented.

By submitting a contribution, you agree that it may be distributed under this
repository's MIT License.
