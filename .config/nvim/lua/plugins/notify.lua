return {
  "rcarriga/nvim-notify",
  opts = {
    render = "compact",
    timeout = 3000,
    stages = "fade",
    top_down = false,
    config = function()
      require("notify").setup({
        background_colour = "#000000",
      })
    end,
  },
}
