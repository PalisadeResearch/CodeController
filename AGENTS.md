# CodeController

Single-file Swift macOS app that remaps an Xbox controller to keyboard/mouse for terminal workflows. No Xcode project, no SPM — just `swiftc`.

## Build & Deploy

```bash
# Build
bash build.sh

# Reset permissions, build, deploy, and launch
tccutil reset Accessibility com.local.codecontroller && pkill -x CodeController 2>/dev/null; sleep 0.5; bash build.sh && cp -R CodeController.app /Applications/ && open /Applications/CodeController.app
```

**IMPORTANT:** Always reset Accessibility permissions before deploying. The app's hash changes on every rebuild, so macOS invalidates the old permission grant. Without the reset, the app launches but silently fails to send input events.

Packaging regressions: `python3 -B -m unittest discover -s tests -v`. These use a
stub compiler in temporary directories; app testing remains manual with a
connected controller on macOS.

## Architecture

Everything lives in `CodeController.swift` (~560 lines):

- **Binding config** (top): `Binding` struct (Codable), `defaultConfigJSON`, `keyNameToCode` lookup, `loadBindings()` reads from `~/.config/codecontroller.json`
- **State tracking**: `buttonStates`, `activeBindingObjects`, scroll/mouse velocity, canonical button order and fallback mouse button numbering (10-51)
- **Event simulation**: `pressKey()`, `tapKey()`, `pressMouseButton()`, `mouseClick()`, `rightClick()`, `moveMouse()`, `scroll()` — all use CGEvent with `.privateState` event source
- **Binding dispatch**: `executeBinding()` and `handleButton()` — unified dispatch with activeBindingObjects tracking for correct release behavior. If no config entry exists, falls back to sequential mouse button
- **Polling**: `pollController()` at 60Hz via Timer — reads all buttons through `handleButton()`, left stick for mouse with momentum, right stick for scroll with hybrid decay
- **Menu bar**: `AppActions` class — NSStatusItem with icon, status, Edit Bindings, Reload Config, Show README (marked.js), Quit
- **Main**: NSApplication with `.accessory` policy, `shouldMonitorBackgroundEvents` on controller connect, Accessibility permission prompt

## Key Conventions

- Button names: `a`, `b`, `x`, `y`, `rt`, `rb`, `ls`, `rs`, `dpad_up/down/left/right`, `back`, `menu`
- Modifier layers: prefix with `lt+` or `lb+` (e.g., `lt+a`, `lb+dpad_left`)
- `ls`/`rs` not `l3`/`r3` — migration in `loadBindings()` handles old configs
- Canonical button order: A, B, X, Y, RT, RB, LS, RS, D-pad, Back, Menu
- Mouse button numbering: all layers use 10-23, distinguished by modifier keys (none for base, +Option for LT, +Control for LB). Hard cap at button 31 — higher numbers crash WindowServer

## Gotchas

- **`tapKey()` vs `pressKey()`**: `tapKey` posts explicit modifier key-down/up events around the main key — required for system shortcuts like `Cmd+Shift+[` that won't register from just setting CGEvent flags
- **`shouldMonitorBackgroundEvents`**: Must be set after a controller connects, not before (crashes on some macOS versions). Without it, gamepad input silently stops when app isn't frontmost
- **Accessibility permissions**: Reset with `tccutil reset Accessibility com.local.codecontroller` when the app stops working after rebuilds. The app prompts via `AXIsProcessTrustedWithOptions` on launch
- **CGEvent `.privateState`**: Prevents our synthetic events from contaminating the global modifier state
- **Config loading**: Runs before `freopen` redirects stdout, so load messages don't appear in `~/Library/Logs/CodeController.log`
- **Config validation**: `validateBindings()` checks for unknown button names, unknown types, missing key fields, negative mouse buttons, and unknown modifiers — warns via NSAlert on load and reload
