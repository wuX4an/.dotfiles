-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

local map = vim.keymap.set

-- Normal Editor
map("n", "<Tab>", "<cmd>BufferLineCycleNext<CR>", { noremap = true })
map("n", "<S-Tab>", "<cmd>BufferLineCyclePrev<CR>", { noremap = true })
map("n", "<S-u>", "<C-r>")

map("n", "<Leader>z", "<cmd>ZenMode<CR>", { desc = "Zen Mode" })
map("n", "<S-space>", "<cmd>Telescope keymap", { desc = "Keymaps" })
map("i", "<C-h>", "<Esc>vbdi", { desc = "Delete word" })
map("i", "<A-h>", "<Esc>vbdi", { desc = "Delete word" })

map("n", "<Leader>m", "", { desc = "Compiler Panel" })
map("n", "<Leader>mc", "<cmd>CompilerOpen<CR>", { desc = "Open Compiler Options" })
map("n", "<Leader>mo", "<cmd>CompilerToggleResults<CR>", { desc = "View Compiler Results" })

-- map("n", "<Leader>e", "<cmd>Neotree right toggle<CR>", { desc = "Explorer NeoTree (Root Dir)" })
-- map("n", "<Leader>E", "<cmd>Neotree right toggle dir=./<CR>", { desc = "Explorer NeoTree (cwd)" })
map("n", "<leader>N", "<cmd>Telekasten panel<CR>")

-- Most used functions
map("n", "<leader>Nf", "<cmd>Telekasten find_notes<CR>")
map("n", "<leader>Ng", "<cmd>Telekasten search_notes<CR>")
map("n", "<leader>Nd", "<cmd>Telekasten goto_today<CR>")
map("n", "<leader>Nz", "<cmd>Telekasten follow_link<CR>")
map("n", "<leader>Nn", "<cmd>Telekasten new_note<CR>")
map("n", "<leader>Nc", "<cmd>Telekasten show_calendar<CR>")
map("n", "<leader>Nb", "<cmd>Telekasten show_backlinks<CR>")
map("n", "<leader>NI", "<cmd>Telekasten insert_img_link<CR>")

-- Call insert link automatically when we start typing a link
-- map("i", "[[", "<cmd>Telekasten insert_link<CR>")
