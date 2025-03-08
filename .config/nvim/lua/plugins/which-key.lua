return {
  "folke/which-key.nvim",
  event = "User BaseDefered",

  opts_extend = { "disable.ft", "disable.bt" },
  opts = {
    preset = "modern", -- "classic", "modern", or "helix"
  },
  config = function(_, opts)
    require("which-key").setup(opts)
  end,
}
