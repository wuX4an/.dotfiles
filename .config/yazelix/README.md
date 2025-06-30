# Yazelix v6: The power of Yazi plugins and nushell scripting!

## Overview
Yazelix integrates Yazi, Zellij and Helix, hence the name, get it?

- Zellij orchestrates everything, with Yazi as a sidebar and Helix as the editor
- To hide the sidebar, just make your pane fullscreen! (`Ctrl p + f` or `Alt f`)
- Every keybinding from Zellij that conflicts with Helix is remapped [see here](<README#Keybindings>)
- When you hit Enter on a file/folder in the "sidebar," the following happens:
  - If Helix is already open in the topmost pane of the stack (default position in latest zellij version), it opens that file/folder in a new buffer in Helix!
  - If Helix isn’t open, it launches Helix in a new pane for you
- Features include "reveal file in sidebar" and a Yazi plugin that shows when a file was added or changed
- This project holds my config files for Zellij, Yazi, terminal emulators, Nushell scripts, Lua plugins and a lot of love

## Preview
![yazelix_v6_demo](assets/reveal_fullscreen_stacked.gif)
v6 demo

## Improvements of v6 over v5
- **Warning**: After upgrading to Yazelix v6, terminate any running Yazi instances and old terminals to prevent conflicts
- Adds a Yazi plugin to enhance the status bar in the sidebar pane, making it uncluttered, colorful and restores showing file permissions
- Includes a Ghostty config. The author now uses Ghostty as their daily driver, but Yazelix remains compatible with any terminal emulator!
- Thanks to this great [plugin](https://github.com/josephschmitt/auto-layout.yazi), Yazelix’s Yazi now dynamically updates the number of columns (parent, current and preview), making it perfect for sidebar use
- Adds a [Git plugin](https://github.com/yazi-rs/plugins/tree/main/git.yazi) that shows file changes in the Yazi sidebar, incredibly helpful!
- Reveal-in-Yazi command added, pressing `Alt y` in Helix will reveal the file in Yazi, see how to set it up [here](<README#Yazelix Custom Keybindings>). It was implemented using nushell and the `ya emit-to` command
  - LIMITATION (for now): currently it only works for helix instances you opened from yazi (easy adaptation: only open helix from yazi)
  - Requirement: For now, to use this command, you have to [build helix from source](https://docs.helix-editor.com/building-from-source.html), while we wait for the next helix release (with command expansions)
- When opening a file from Yazi, it now always finds a running Helix instance if:
  - It exists
  - It’s in the top pane of the stacked group (Zellij naturally pushes the Helix pane there when opening new panes, but sometimes it moves around when you delete a pane or create a new one)
- Recommendation: Make Yazelix’s Yazi config your default (it’s plugin-enhanced and adjusts layout based on width). For Nushell users, add this to your `env.nu` file (run `config env` to edit):
  ```
  $env.YAZI_CONFIG_HOME = "~/.config/yazelix/yazi"
  ```
- Added detailed logging for nushell scripts, and added logging instructions regarding zellij/yazi to the readme
- Code is way more robust, and the features more polished (open from yazi specially so)
- When you open a file from yazi, it automatically renames the zellij tab to the file's underlying git repo or directory name (game changer)

## Compatibility
- Works with any terminal emulator, though I prefer WezTerm and Ghostty
- Editor: Helix (for now)
- See the version compatibility table [here](<README#Table of Versions>)

## Instructions to Set It Up
1. Ensure the following are installed and in your PATH:
   - [Yazi-fm and Yazi-cli](https://github.com/sxyazi/yazi)
   - [Zellij](https://github.com/zellij-org/zellij)
   - [Helix](https://helix-editor.com)
   - [Nushell](https://www.nushell.sh/book/installation.html)
   - [Zoxide](https://github.com/ajeetdsouza/zoxide): optional, allows you to quickly navigate directories using a smart, interactive command-line tool that learns your habits
   - [cargo-update](https://github.com/nabijaczleweli/cargo-update): optional, enables you to update Rust crates in your project by running a simple command: `cargo install-update -a`
   - [cargo-binstall](https://github.com/cargo-bins/cargo-binstall): optional, provides a WAY faster way to install rust tools, using binaries directly, skipping the compilation step. Will be used by cargo-update if available. Very useful!
  - Example of how to install the deps:
     ```
     cargo install cargo-update cargo-binstall
     cargo install-update -i zellij nu yazi-cli yazi-fm zoxide
     cargo install-update -a # will update everything
     ```
2. Clone this repo into your `~/.config` directory:
   ```
   git clone https://github.com/luccahuguet/yazelix ~/.config/yazelix
   ```
3. Configure your terminal emulator:
   - For WezTerm:
     ```
     cp ~/.config/yazelix/terminal_configs/wez/.wezterm.lua ~/.wezterm.lua
     ```
   - For Ghostty:
     ```
     cp ~/.config/yazelix/terminal_configs/ghostty/config ~/.config/ghostty/config
     ```
   - For other emulators, configure it to run this command on startup (view [ghostty's config](<./terminal_configs/ghostty/config>) for a detailed explanation and alternatives):
     ```
     "nu -c 'zellij --config-dir ~/.config/yazelix/zellij attach --create yazelix_ghostty options --default-layout yazelix'"
     ```

**Notes**:
- Feel free to tweak the configs to make it yours—this is just a starting point
- For extra configuration, see: [WezTerm Docs](https://wezfurlong.org/wezterm/config/files.html) or [Ghostty Docs](https://ghostty.org/docs/config)

That’s it! Open issues or PRs if you’d like 😉

## Why Use This Project?
- Easy to configure and personalize
- I daily-drive Yazelix and will always try to improve it and maintain it
- Zero-conflict keybindings (no need to lock Zellij) and a powerful yazi sidebar
- Cool Yazi plugins included out of the box
- Features like `reaveal in yazi` (from helix) and opening files from yazi in a hx buffer

## Troubleshooting
- If it’s not working properly, you can:
  - Upgrade Yazi and Zellij to the latest versions for bug fixes and compatibility
  - Check Yazelix logs in `~/.config/yazelix/logs/` (`open_helix.log`, `reveal_in_yazi.log`) for script-specific errors
  - View Yazi logs in `~/.local/state/yazi/yazi.log` by running `YAZI_LOG=debug yazi` (or `info`, `warn`, `error` for progressively less verbosity) to enable logging, with `error` being the least verbose
  - View Zellij logs by opening `~/.cache/zellij/zellij-log-<session>.log` or `/tmp/zellij-<uid>/zellij-log/zellij.log` (path varies by system) for session-specific issues
- Check the version compatibility table [here](<README#Table of Versions>)

## Keybindings
| New Zellij Keybinding | Previous Keybinding | Helix Action that conflicted before  | Zellij Action Remapped     |
|-----------------------|---------------------|--------------------------------------|----------------------------|
| Ctrl e                | Ctrl o              | jump_backward                        | SwitchToMode "Session"     |
| Ctrl y                | Ctrl s              | save_selection                       | SwitchToMode "Scroll"      |
| Alt w                 | Alt i               | shrink_selection                     | MoveTab "Left"             |
| Alt q                 | Alt o               | expand_selection                     | MoveTab "Right"            |
| Alt m                 | Alt n               | select_next_sibling                  | NewPane                    |
| Alt 2                 | Ctrl b              | move_page_up                         | SwitchToMode "Tmux"        |

If you find a conflict, please open an issue

## Discoverability of Keybindings
- **Zellij**: Shows all keybindings visually in the status bar—works out of the box
- **Helix**: Similar to Zellij, keybindings are easy to discover
- **Yazi**: Press `~` to see all keybindings and commands (use `Alt f` to fullscreen the pane for a better view)
- **Nushell**:
  - Run `tutor` on a nu shell
  - Read the [Nushell Book](https://www.nushell.sh/book/)
  - Use `help commands | find tables` to search, for example, commands that are related to tables

## Yazelix Custom Keybindings
- **Zellij**: `Alt f` toggles pane fullscreen
- **Helix**: `Alt y` reveals the file from the Helix buffer in Yazi, add this to your Helix config:
  ```toml
  [keys.normal]
  A-y = ":sh nu ~/.config/yazelix/nushell/reveal_in_yazi.nu \"%{buffer_name}\""
  ```

## Keybinding Tips
- **Zellij**: `Ctrl p` then `r` for a split to the right; `Ctrl p` then `d` for a downward split
- **Yazi**: 
  - `Z`: Use Zoxide (fuzzy find known paths)
  - `z`: Use fzf (fuzzy find unknown paths)
  - `SPACE`: Select files
  - `y`: Yank (copy); `Y`: Unyank (cancel copy)
  - `x`: Cut; `X`: Uncut (cancel cut)
  - `a`: Add a file (`filename.ext`) or folder (`foldername/`)
- **Nushell**:
  - `Ctrl r`: interactive history search
  - `Ctrl o`: open a temporary buffer


## Tips
- Add more swap layouts as needed using the KDL files in `layouts`
- I recommend Ghostty or WezTerm, they are extensible and performant

## I’m Lost! Too Much Information
Start by learning Zellij on its own, then optionally Yazi, and re-read this README afterward

## Thanks
- To Yazi, Zellij, Helix and Nushell contributors/maintainers for their amazing projects and guidance
- To Yazi’s author for contributing Lua code to make the sidebar status bar look awesome
- To [Joseph Schmitt](https://github.com/josephschmitt) for his excellent [auto-layout plugin](https://github.com/josephschmitt/auto-layout.yazi)

## Contributing to Yazelix
See [contributing](./contributing.md)

## Table of Versions
- Last tested: April 10th, 2025
- Should work with older versions, but these are tested
- Compatible with other terminal emulators (e.g., Alacritty in the past)

| Component          | Version                  |
| -------------------| ------------------------ |
| OS                 | Pop!_OS 24.04            |
| DE                 | COSMIC                   |
| Zellij             | 0.42.1                   |
| Helix (from source)| helix 25.01.1 (0efa8207) |
| Nushell            | 0.103.0                  |
| Zoxide             | 0.9.7                    |
| Yazi               | 25.4.8                   |
| WezTerm            | 20240203-110809-5046fc22 |
| Ghostty            | 1.1.2                    |
| ya (from yazi-cli) | 25.4.8                   |

## Similar Projects

- If you frequently use other terminal editors besides helix or terminal file managers other than yazi, checkout [zide](https://github.com/josephschmitt/zide)
- If you care about yazi, but dont care much about zellij or having a sidebar, you can integrate yazi and helix with [one line of config](https://github.com/sxyazi/yazi/pull/2461) (experimental, not working for some people as of march 15, 2025)
