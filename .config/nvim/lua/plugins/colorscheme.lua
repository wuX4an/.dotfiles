-- return {
--   "neanias/everforest-nvim",
--   version = false,
--   lazy = false,
--   priority = 1000, -- Asegúrate de cargarlo antes que otros plugins
--   config = function()
--     require("everforest").setup({
--       transparent_background = true, -- Habilitar fondo transparente
--     })

--     -- Además puedes configurar el color de fondo manualmente en tu archivo de configuración de Neovim
--
--     vim.cmd("colorscheme everforest")
--     -- vim.cmd("hi Normal guibg=NONE ctermbg=NONE") -- Establece el fondo como transparente
--     -- vim.cmd("hi NormalNC guibg=NONE ctermbg=NONE") -- Asegúrate de que las ventanas no activas también sean transparentes
--     -- vim.cmd("hi NeoTreeNormal guibg=NONE ctermbg=NONE")
--   end,
-- }
return {
  "wux4an/everforest-nvim",
  version = false,
  lazy = false,
  priority = 1000,
  config = function()
    require("everforest").setup({})
    vim.cmd("colorscheme everforest")
  end,
}
