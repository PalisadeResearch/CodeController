# CodeController

Write software entirely using an Xbox controller and your voice. Maps every control you need for a voice-first, multi-terminal, agentic workflow to your gamepad.

Sit, stand, or walk around while developing software faster than ever.

## Features

- **Face buttons** — Common keys (Return, Escape, Backspace, Tab) with modifier layers

- **D-pad** — Arrow keys, with modifier layers for tab and window switching

- **Two modifier layers** — Hold LT or LB to access extended bindings on every button

- **Left stick** — Moves mouse cursor (fallback for when buttons won't do)

- **Right stick** — Smooth scrolling

- **Universal mouse buttons** — Any button combo without a keyboard binding automatically emits a virtual mouse button (10–23), distinguished across modifier layers by held modifier keys (Option for +LT, Control for +LB). Mappable in utilities like [SuperWhisper](https://superwhisper.com) or [BetterTouchTool](https://folivora.ai)

- **JSON config** — All bindings stored in `~/.config/codecontroller.json`, editable without recompiling

## Requirements

- macOS 10.15+
- Xbox One wireless controller (known supported — other controllers may work via Apple's Game Controller framework)
- **Voice transcription** — CodeController replaces your keyboard, so you need a voice-to-text app to type. [SuperWhisper](https://superwhisper.com) is recommended, but [Whisper Transcription](https://goodsnooze.gumroad.com/l/macwhisper), [Talon](https://talonvoice.com), or macOS Dictation also work

## Setup

Check the [Releases](../../releases) page for pre-built binaries.

### Building from Source

Requires Swift toolchain (Xcode or Command Line Tools).

1. Build: `./build.sh`
2. Copy to Applications: `cp -R CodeController.app /Applications/`
3. Launch: `open /Applications/CodeController.app`
4. Grant **Accessibility** permission when prompted (or manually in System Settings > Privacy & Security > Accessibility)

### Testing the Build Script

Run `python3 -B -m unittest discover -s tests -v` to check packaging success and
failure handling. These tests require Python 3 and Bash, use a stub Swift compiler
in temporary directories, and never launch the app or request Accessibility
permissions. They do not validate Swift compilation or controller behavior;
those checks require macOS and a connected controller.

### SuperWhisper (Voice Input)

[SuperWhisper](https://superwhisper.com) is a macOS voice-to-text app. Bind controller buttons to SuperWhisper for hands-free dictation:

1. Install SuperWhisper
2. Open SuperWhisper Settings
3. Set Mouse Shortcut to **Mouse Button 14** (RT)

### BetterTouchTool (Extended Bindings)

[BetterTouchTool](https://folivora.ai) can map any of the virtual mouse buttons (10–23) to system actions that CodeController can't do natively — switching Spaces, launching apps, window snapping, etc. Modifier layers emit the same button numbers but with held modifier keys (Option for +LT, Control for +LB), so BTT can distinguish them by matching on modifier state.

1. Open BetterTouchTool Settings
2. Enable **Advanced > High Level Mouse Event Recognition**
3. Import the included preset: **Preset > Import Preset**, then select `codecontroller_triggers.bttpreset` from the app bundle (right-click CodeController.app > Show Package Contents > Contents/Resources) or the [Releases](../../releases) page
4. The preset maps LT+D-Left / LT+D-Right to switch Spaces (left/right)

Add your own triggers by assigning a mouse button to any action in BetterTouchTool's preferences.

### Claude Code Keybindings

The default bindings map Y to Tab. Claude Code changed Tab from extended thinking toggle to autocomplete. To restore Tab as the thinking toggle, add this to `~/.claude/keybindings.json`:

```json
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "tab": "chat:thinkingToggle"
      }
    }
  ]
}
```

## Default Bindings

> **Mouse buttons:** Every button has a default mouse button number shown in the **Mouse #** column. All three layers (Base, +LT, +LB) use the same button numbers (10–23) — layers are distinguished by modifier keys held during the event: none for Base, Option for +LT, Control for +LB. The config file contains keyboard overrides — remove an override to expose the underlying mouse button. These virtual mouse buttons can be mapped in apps like SuperWhisper or BetterTouchTool.

### Sticks

| Input | Action | Mouse # |
|-------|--------|---------|
| Left Stick | Mouse cursor | |
| Left Stick Click | Left click | 16 |
| Right Stick | Scroll | |
| Right Stick Click | Right click | 17 |

### Modifiers

| Button | Role |
|--------|------|
| **LT** (Left Trigger) | Hold to activate +LT layer |
| **LB** (Left Bumper) | Hold to activate +LB layer |

### Base

| Button | Key | Action | Mouse # |
|--------|-----|--------|---------|
| **A** | `Return` | Submit | 10 |
| **B** | `Escape` | Cancel | 11 |
| **X** | `Backspace` | Delete | 12 |
| **Y** | `Tab` | Autocomplete / thinking | 13 |
| **RT** | | | 14 |
| **RB** | | | 15 |
| **D-Up** | `Up` | Navigate | 18 |
| **D-Down** | `Down` | Navigate | 19 |
| **D-Left** | `Left` | Navigate | 20 |
| **D-Right** | `Right` | Navigate | 21 |
| **Back** | `Ctrl+O` | Toggle transcript | 22 |
| **Menu** | `/` | Slash commands | 23 |

### +LT (mouse buttons held with Option)

| Button | Key | Action | Mouse # |
|--------|-----|--------|---------|
| **LT+A** | `Space` | Scroll page | 10+Opt |
| **LT+B** | | | 11+Opt |
| **LT+X** | | | 12+Opt |
| **LT+Y** | `Shift+Tab` | Cycle permission mode | 13+Opt |
| **LT+RT** | | | 14+Opt |
| **LT+RB** | | | 15+Opt |
| **LT+LS** | | | 16+Opt |
| **LT+RS** | | | 17+Opt |
| **LT+D-Up** | `<Accessibility>` | Cycle windows | 18+Opt |
| **LT+D-Down** | `<Accessibility>` | Cycle windows | 19+Opt |
| **LT+D-Left** | `Cmd+Shift+[` | Prev tab | 20+Opt |
| **LT+D-Right** | `Cmd+Shift+]` | Next tab | 21+Opt |
| **LT+Back** | `Ctrl+E` | Toggle show all | 22+Opt |
| **LT+Menu** | | | 23+Opt |

### +LB (mouse buttons held with Control)

| Button | Key | Action | Mouse # |
|--------|-----|--------|---------|
| **LB+A** | | | 10+Ctrl |
| **LB+B** | `Cmd+W` | Close tab | 11+Ctrl |
| **LB+X** | | | 12+Ctrl |
| **LB+Y** | `Cmd+T` | New tab | 13+Ctrl |
| **LB+RT** | | | 14+Ctrl |
| **LB+RB** | | | 15+Ctrl |
| **LB+LS** | | | 16+Ctrl |
| **LB+RS** | | | 17+Ctrl |
| **LB+D-Up** | | | 18+Ctrl |
| **LB+D-Down** | | | 19+Ctrl |
| **LB+D-Left** | | | 20+Ctrl |
| **LB+D-Right** | | | 21+Ctrl |
| **LB+Back** | `Ctrl+B` | Background task | 22+Ctrl |
| **LB+Menu** | | | 23+Ctrl |

## Configuration

Bindings are stored in `~/.config/codecontroller.json`. A default config is written on first launch. Edit the file and use **Reload Config** from the menu bar to apply changes.

The config only needs entries for keyboard overrides. Any button combo not in the config automatically emits its mouse button.

### Binding Types

| Type | Description | Fields |
|------|-------------|--------|
| `key` | Hold key (press on button down, release on up) | `key`, `modifiers` |
| `tap` | Fire once on press with explicit modifier key events — use for system shortcuts (e.g. `Cmd+Shift+[`) that don't register with `key` | `key`, `modifiers` |
| `leftClick` | Left mouse click | — |
| `rightClick` | Right mouse click | — |
| `cycleWindows` | Raise next window of frontmost app | — |

### Example Bindings

```json
{ "key": "return",  "type": "key" }
{ "key": "w",       "type": "key",   "modifiers": ["command"] }
{ "key": "[",       "type": "tap",   "modifiers": ["command", "shift"] }
{ "type": "leftClick" }
{ "type": "cycleWindows" }
```

### Key Names

- Letters: `a` through `z`
- Numbers: `0` through `9`
- Editing: `return`, `tab`, `space`, `backspace`, `escape`, `delete`
- Arrows: `up`, `down`, `left`, `right`
- Function: `f1` through `f12`
- Punctuation: `/`, `[`, `]`, `-`, `=`, `;`, `'`, `,`, `.`, `` ` ``
- Navigation: `home`, `end`, `pageup`, `pagedown`

### Modifier Names

- `command` or `cmd`
- `shift`
- `option` or `alt`
- `control` or `ctrl`

### Binding Keys

Base buttons:

`a`, `b`, `x`, `y`, `rt`, `rb`, `ls`, `rs`, `back`, `menu`, `dpad_up`, `dpad_down`, `dpad_left`, `dpad_right`

Prefix with `lt+` or `lb+` for modifier layers (e.g., `lt+a`, `lb+dpad_left`).

## Logs

Output is logged to `~/Library/Logs/CodeController.log`.
