set fish_greeting
# autorun
zoxide init fish | source
#tide configure --auto --style=Lean --prompt_colors='16 colors' --show_time=No --lean_prompt_height='One line' --prompt_spacing=Compact --icons='Many icons' --transient=Yes

# Exports:
export SUDO_PROMPT="passwd: "
export EDITOR="nvim"
export TERM="xterm-256color"

# Alias:
alias ls="eza --color --sort=type --icons -1"
alias sl="eza --color --sort=type --icons -1"
alias la="eza --color --sort=type --icons -1 -a"
alias l="eza --color --sort=type --across --header --modified --created --git --icons -1 -a -l"
alias cp="cp -r"
alias cd="z"
alias py="python"
alias clip="xclip -i -selection clipboard"
alias rm="rmtrash"
