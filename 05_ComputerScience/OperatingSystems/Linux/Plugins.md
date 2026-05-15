---
aliases: [Plugins]
tags: ['OperatingSystems', 'Linux', 'Plugins']
---

# Vim 插件生态

## 一、插件管理器

### lazy.nvim (Neovim 推荐)

```lua
-- lazy.nvim 配置
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable",
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    -- 在此添加插件
    "folke/which-key.nvim",
    "nvim-treesitter/nvim-treesitter",
    -- 带配置的插件
    {
        "nvim-telescope/telescope.nvim",
        dependencies = { "nvim-lua/plenary.nvim" },
        config = function()
            require("telescope").setup({})
        end,
    },
}, {
    checker = { enabled = true, notify = false },
    change_detection = { notify = false },
})
```

### vim-plug

```vim
" ~/.vimrc 或 ~/.config/nvim/init.vim
call plug#begin('~/.vim/plugged')

" 插件列表
Plug 'preservim/nerdtree'
Plug 'junegunn/fzf.vim'
Plug 'vim-airline/vim-airline'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'tpope/vim-fugitive'

call plug#end()

" 重启后运行 :PlugInstall 安装插件
```

### packer.nvim (已归档，推荐迁移到 lazy.nvim)

```lua
-- packer.nvim
require('packer').startup(function()
    use 'wbthomason/packer.nvim'
    use 'nvim-treesitter/nvim-treesitter'
    use { 'nvim-telescope/telescope.nvim', requires = { 'nvim-lua/plenary.nvim' } }
end)
```

---

## 二、文件管理器

### NerdTree

```vim
" 安装：Plug 'preservim/nerdtree'
nnoremap <Leader>e :NERDTreeToggle<CR>
nnoremap <Leader>f :NERDTreeFind<CR>

" 设置
let NERDTreeShowHidden = 1
let NERDTreeMinimalUI = 1
let NERDTreeDirArrows = 1
let NERDTreeAutoDeleteBuffer = 1
```

### netrw (内置)

```vim
" Vim 内置文件浏览器
" 打开目录即可使用
:e .
:Explore
:Sexplore          " 水平分屏
:Vexplore          " 垂直分屏
let g:netrw_liststyle = 3    " 树形视图
```

### oil.nvim

```lua
-- Neovim 文件管理器（类似 VSCode 的文件编辑）
require('oil').setup({
    default_file_explorer = true,
    columns = { "icon" },
    view_options = {
        show_hidden = true,
    },
})

vim.keymap.set('n', '-', '<CMD>Oil<CR>')
```

---

## 三、模糊查找

### fzf.vim

```vim
" 安装：Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
"       Plug 'junegunn/fzf.vim'

" 基本命令
:FZF                   " 查找文件
:GFiles                " Git 文件
:GFiles?               " Git 修改的文件
:Buffers               " 缓冲区
:Lines                 " 全文搜索
:Rg                    " ripgrep 搜索
:Marks                 " 标记
:History               " 历史文件
:Commands              " 命令列表

" 映射
nnoremap <Leader>ff :FZF<CR>
nnoremap <Leader>fg :Rg<CR>
nnoremap <Leader>fb :Buffers<CR>
```

### telescope.nvim

```lua
-- Neovim 原生模糊查找器
require('telescope').setup({
    defaults = {
        file_ignore_patterns = { "node_modules", ".git" },
        layout_strategy = "horizontal",
        layout_config = {
            horizontal = { preview_width = 0.5 }
        },
        mappings = {
            i = {
                ["<C-j>"] = "move_selection_next",
                ["<C-k>"] = "move_selection_previous",
            },
        },
    },
    pickers = {
        find_files = { hidden = true },
    },
})

-- 映射
vim.keymap.set('n', '<Leader>ff', require('telescope.builtin').find_files)
vim.keymap.set('n', '<Leader>fg', require('telescope.builtin').live_grep)
vim.keymap.set('n', '<Leader>fb', require('telescope.builtin').buffers)
vim.keymap.set('n', '<Leader>fh', require('telescope.builtin').help_tags)
vim.keymap.set('n', '<Leader>fk', require('telescope.builtin').keymaps)
vim.keymap.set('n', '<Leader>ft', require('telescope.builtin').treesitter)
vim.keymap.set('n', '<Leader>fd', require('telescope.builtin').diagnostics)
```

---

## 四、状态栏

### vim-airline

```vim
" 安装：Plug 'vim-airline/vim-airline'
"       Plug 'vim-airline/vim-airline-themes'

" 设置
let g:airline_theme = 'dracula'
let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail'
let g:airline_section_y = '%{strftime("%H:%M")}'
```

### lualine.nvim

```lua
-- Neovim 轻量状态栏
require('lualine').setup({
    options = {
        theme = 'dracula',
        component_separators = { left = '', right = '' },
        section_separators = { left = '', right = '' },
    },
    sections = {
        lualine_a = { 'mode' },
        lualine_b = { 'branch', 'diff' },
        lualine_c = { 'filename' },
        lualine_x = { 'encoding', 'fileformat', 'filetype' },
        lualine_y = { 'progress' },
        lualine_z = { 'location' },
    },
})
```

---

## 五、LSP 客户端

### coc.nvim (Vim 和 Neovim)

```vim
" 安装：Plug 'neoclide/coc.nvim', {'branch': 'release'}

" 基本设置
" 补全确认
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm() : "\<CR>"

" 导航
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" 重命名
nmap <Leader>rn <Plug>(coc-rename)

" 代码操作
nmap <Leader>ca <Plug>(coc-codeaction)
xmap <Leader>ca <Plug>(coc-codeaction-selected)

" 诊断
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" 浮动文档
nnoremap <silent> K :call CocAction('doHover')<CR>
```

```json
// coc-settings.json
{
  "languageserver": {
    "golang": {
      "command": "gopls",
      "filetypes": ["go"]
    },
    "rust-analyzer": {
      "command": "rust-analyzer",
      "filetypes": ["rust"]
    }
  }
}
```

### nvim-lspconfig (Neovim 内置 LSP)

```lua
-- LSP 设置
local lspconfig = require('lspconfig')

-- 快捷键
vim.api.nvim_create_autocmd('LspAttach', {
    group = vim.api.nvim_create_augroup('UserLspConfig', {}),
    callback = function(ev)
        local opts = { buffer = ev.buf }
        vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
        vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
        vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, opts)
        vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
        vim.keymap.set('n', '<Leader>rn', vim.lsp.buf.rename, opts)
        vim.keymap.set('n', '<Leader>ca', vim.lsp.buf.code_action, opts)
    end,
})

-- 配置各语言服务器
lspconfig.pyright.setup {}
lspconfig.tsserver.setup {}
lspconfig.gopls.setup {}
lspconfig.rust_analyzer.setup {
    settings = {
        ['rust-analyzer'] = { checkOnSave = { command = "clippy" } },
    },
}
lspconfig.clangd.setup {}
```

### nvim-cmp (补全引擎)

```lua
local cmp = require('cmp')

cmp.setup({
    snippet = {
        expand = function(args)
            require('luasnip').lsp_expand(args.body)
        end,
    },
    mapping = cmp.mapping.preset.insert({
        ['<C-b>'] = cmp.mapping.scroll_docs(-4),
        ['<C-f>'] = cmp.mapping.scroll_docs(4),
        ['<C-Space>'] = cmp.mapping.complete(),
        ['<C-e>'] = cmp.mapping.abort(),
        ['<CR>'] = cmp.mapping.confirm({ select = true }),
        ['<Tab>'] = cmp.mapping(function(fallback)
            if cmp.visible() then
                cmp.select_next_item()
            else
                fallback()
            end
        end, { 'i', 's' }),
    }),
    sources = cmp.config.sources({
        { name = 'nvim_lsp' },
        { name = 'luasnip' },
    }, {
        { name = 'buffer' },
        { name = 'path' },
    }),
})
```

---

## 六、语法解析

### nvim-treesitter

```lua
require('nvim-treesitter.configs').setup({
    ensure_installed = {
        "c", "cpp", "go", "rust",
        "python", "javascript", "typescript",
        "lua", "vim", "bash",
        "markdown", "json", "yaml",
        "sql", "html", "css",
    },
    highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
    },
    indent = { enable = true },
    incremental_selection = {
        enable = true,
        keymaps = {
            init_selection = "gnn",
            node_incremental = "grn",
            scope_incremental = "grc",
            node_decremental = "grm",
        },
    },
    textobjects = {
        select = {
            enable = true,
            lookahead = true,
            keymaps = {
                ["af"] = "@function.outer",
                ["if"] = "@function.inner",
                ["ac"] = "@class.outer",
                ["ic"] = "@class.inner",
            },
        },
    },
})
```

---

## 七、Git 集成

### vim-fugitive

```vim
" 安装：Plug 'tpope/vim-fugitive'

:Git              " git 命令
:Gstatus          " git status
:Gdiff            " git diff
:Gcommit          " git commit
:Gblame           " git blame
:Glog             " git log
:Gedit :%         " 显示当前文件的 Git 版本

" 映射
nnoremap <Leader>gs :Gstatus<CR>
nnoremap <Leader>gd :Gdiff<CR>
nnoremap <Leader>gb :Gblame<CR>
nnoremap <Leader>gl :Glog<CR>
```

### gitsigns.nvim

```lua
require('gitsigns').setup({
    signs = {
        add          = { text = '+' },
        change       = { text = '~' },
        delete       = { text = '_' },
        topdelete    = { text = '‾' },
        changedelete = { text = '~' },
    },
    on_attach = function(bufnr)
        local gs = package.loaded.gitsigns
        vim.keymap.set('n', '<Leader>hs', gs.stage_hunk)
        vim.keymap.set('n', '<Leader>hr', gs.reset_hunk)
        vim.keymap.set('n', '<Leader>hp', gs.preview_hunk)
        vim.keymap.set('n', '<Leader>hb', function() gs.blame_line{full=true} end)
        vim.keymap.set('n', '<Leader>hd', gs.diffthis)
        vim.keymap.set('n', ']c', gs.next_hunk)
        vim.keymap.set('n', '[c', gs.prev_hunk)
    end,
})
```

---

## 八、其他实用插件

| 插件 | 功能 |
|------|------|
| tpope/vim-commentary | 注释/取消注释（`gc`） |
| windwp/nvim-autopairs | 自动配对括号 |
| rabob3/commentary.nvim | Neovim 注释插件 |
| numToStr/Comment.nvim | 另一个注释插件 |
| kylechui/nvim-surround | 操作周围字符（引号、括号） |
| folke/which-key.nvim | 显示按键提示 |
| lewis6991/impatient.nvim | 加速 Neovim 启动 |
| stevearc/dressing.nvim | 美化 UI 组件 |
| rcarriga/nvim-notify | 美化通知 |
| nvim-lua/plenary.nvim | 通用工具库 |
| folke/trouble.nvim | 诊断列表 |
| mfussenegger/nvim-dap | 调试适配器 |
| jose-elias-alvarez/null-ls.nvim | 代码格式化/lint |

## 相关条目

- [[Neovim]]
- [[Config]]
- [[Languages]]
- [[Bash]]
- [[Scripting]]
