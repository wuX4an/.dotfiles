from libqtile import layout


layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], margin=8),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(
        margin=8,
        border_width=2,
        border_focus="#343f44",
        border_normal="#232a2e",
    ),
    # layout.Matrix(),
    layout.MonadTall(
        margin=8,
        border_width=2,
        border_focus="#343f44",
        border_normal="#232a2e",
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(),
    layout.TreeTab(
        font="Departure Mono",
        fontsize=11,
        border_width=0,
        # bg_color="#0f0f0f",
        # active_bg="#",
        # active_fg="#",
        # inactive_bg="#",
        # inactive_fg="#",
        padding_left=8,
        padding_x=8,
        padding_y=8,
        sections=["ONE", "TWO", "THREE"],
        section_fontsize=10,
        # section_fg="#",
        section_top=15,
        section_bottom=15,
        level_shift=8,
        vspace=3,
        panel_width=240

    ),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Floating(),
]
