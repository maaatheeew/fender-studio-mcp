from studio_pro_mcp.keyscheme import translate_combo
from studio_pro_mcp.keystrokes import _combo_to_applescript
from studio_pro_mcp.plugin_db import _parse_plugins_en


def test_mac_modifiers_and_numpad() -> None:
    combo, _, problem = translate_combo("Command+Shift+Control+M")
    assert problem is None
    assert combo == "cmd+shift+ctrl+m"
    assert _combo_to_applescript("numdivide") == "key code 75"
    assert _combo_to_applescript("numdecimal") == "key code 65"


def test_studio_pro_class_cache(tmp_path) -> None:
    path = tmp_path / "Plugins-en.settings"
    path.write_text(
        "<Settings><Section><Attributes><Version vendor=\"Fender\"/>"
        "<List><ClassDescription classID=\"{test}\" name=\"Pro EQ\" "
        "category=\"AudioEffect\"/><ClassDescription classID=\"{browser}\" "
        "name=\"Browser\" category=\"BrowserExtension\"/></List>"
        "</Attributes></Section></Settings>"
    )
    result = _parse_plugins_en(path)
    assert [(p.name, p.vendor, p.category) for p in result] == [
        ("Pro EQ", "Fender", "AudioEffect")
    ]
