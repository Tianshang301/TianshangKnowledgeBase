# Neovim 进阶

## 一、Neovim vs Vim

| 特性 | Neovim | Vim |
|------|--------|-----|
| 内置 LSP | ✅ | ❌（需 coc.nvim） |
| Lua API | 原生支持 | 有限 |
| Treesitter | 原生支持 | 需插件 |
| 终端 | 内置终端 | 有限 |
| 异步 | 原生 event loop | 有限 |
| 外部编辑器 | msgpack API | 有限 RPC |
| Python 嵌入 | ✅ | 有限 |
| 配置 | Lua（推荐）或 Vimscript | Vimscript |

---

## 二、Lua 配置 API

### 核心 API

```lua
-- 设置选项
vim.opt.number = true           -- set number
vim.opt.tabstop = 4             -- set tabstop=4
vim.opt.shiftwidth = 4          -- set shiftwidth=4
vim.opt.expandtab = true        -- set expandtab
vim.opt.mouse = 'a'
vim.opt.clipboard = 'unnamedplus'

-- 设置局部选项
vim.opt_local.tabstop = 2
vim.bo.tabstop = 2              -- buffer-local
vim.wo.number = true            -- window-local

-- 全局变量
vim.g.mapleader = ' '

-- 执行 vim 命令
vim.cmd('colorscheme gruvbox')
vim.cmd('source ~/.config/nvim/init.lua')
vim.cmd(augroup my_group
        autocmd!
        autocmd BufWritePre * :%s/\s\+$//e
    augroup END)

-- 定义 autocmd
vim.api.nvim_create_autocmd('BufWritePre', {
    pattern = '*',
    callback = function()
        vim.cmd(%s/\s\+$//e)
    end,
    group = vim.api.nvim_create_augroup('TrimWhitespace', { clear = true }),
})

-- 变量命名
-- vim.g      global variables          (g:)
-- vim.b      buffer variables          (b:)
-- vim.w      window variables          (w:)
-- vim.bo     buffer-local options      (&l:)
-- vim.wo     window-local options      (&w:)
-- vim.env    environment variables     ($)
```

### 按键映射 API

```lua
-- 现代方式
vim.keymap.set('n', '<Leader>w', ':w<CR>', { desc = '保存' })
vim.keymap.set('n', '<Leader>q', ':q<CR>', { desc = '退出' })
vim.keymap.set('i', 'jk', '<Esc>', { desc = '退出插入模式' })

-- 参数说明
-- 模式: 'n' normal, 'i' insert, 'v' visual, 'x' 选择, 't' terminal
-- 'noremap = true' 表示非递归映射
-- 'silent = true' 表示不显示输出
-- 'buffer = true' 表示仅当前缓冲区

-- 旧方式（仍可用）
vim.api.nvim_set_keymap('n', '<Leader>w', ':w<CR>', { noremap = true, silent = true })
```

---

## 三、LSP 设置

### 完整 LSP 配置

```lua
-- 1. lspconfig 管理 LSP 服务器
local lspconfig = require('lspconfig')
local capabilities = require('cmp_nvim_lsp').default_capabilities()

-- LSP 附加时的快捷键
vim.api.nvim_create_autocmd('LspAttach', {
    group = vim.api.nvim_create_augroup('UserLspConfig', {}),
    callback = function(args)
        local buf = args.buf
        local client = vim.lsp.get_client_by_id(args.data.client_id)

        -- 建议：仅支持有补全功能的 LSP 附加
        if client and client.server_capabilities.completionProvider then
            -- 不在此设置补全相关
        end

        -- 快捷键
        local opts = { buffer = buf, silent = true }

        vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)         -- 跳转到定义
        vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)               -- 悬浮文档
        vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, opts)     -- 实现
        vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)         -- 引用
        vim.keymap.set('n', 'gy', vim.lsp.buf.type_definition, opts)    -- 类型定义
        vim.keymap.set('n', '<Leader>rn', vim.lsp.buf.rename, opts)     -- 重命名
        vim.keymap.set('n', '<Leader>ca', vim.lsp.buf.code_action, opts)-- 代码操作
        vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)       -- 上一个诊断
        vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)       -- 下一个诊断
        vim.keymap.set('n', '<Leader>e', vim.diagnostic.open_float, opts) -- 诊断详情
    end,
})

-- 配置语言服务器
local servers = {
    pyright = {},
    tsserver = {},
    gopls = {},
    rust_analyzer = {
        settings = {
            ['rust-analyzer'] = {
                checkOnSave = { command = 'clippy' },
                cargo = { allFeatures = true },
            },
        },
    },
    clangd = {},
    lua_ls = {
        settings = {
            Lua = {
                runtime = { version = 'LuaJIT' },
                diagnostics = { globals = { 'vim' } },
                workspace = {
                    library = vim.api.nvim_get_runtime_file('', true),
                    checkThirdParty = false,
                },
            },
        },
    },
}

for server, config in pairs(servers) do
    config.capabilities = capabilities
    lspconfig[server].setup(config)
end
```

---

## 四、Treesitter

### Treesitter 完整配置

```lua
require('nvim-treesitter.configs').setup({
    ensure_installed = {
        'c', 'cpp', 'go', 'rust', 'python',
        'javascript', 'typescript', 'lua',
        'vim', 'vimdoc', 'bash', 'markdown',
        'markdown_inline', 'json', 'yaml',
        'html', 'css', 'sql',
    },
    auto_install = true,
    highlight = { enable = true },
    indent = { enable = true },
    incremental_selection = {
        enable = true,
        keymaps = {
            init_selection = 'gnn',
            node_incremental = 'grn',
            scope_incremental = 'grc',
            node_decremental = 'grm',
        },
    },
    textobjects = {
        select = {
            enable = true,
            lookahead = true,
            keymaps = {
                ['af'] = '@function.outer',
                ['if'] = '@function.inner',
                ['ac'] = '@class.outer',
                ['ic'] = '@class.inner',
                ['ab'] = '@block.outer',
                ['ib'] = '@block.inner',
            },
        },
        move = {
            enable = true,
            set_jumps = true,
            goto_next_start = {
                [']m'] = '@function.outer',
                [']]'] = '@class.outer',
            },
            goto_previous_start = {
                ['[m'] = '@function.outer',
                ['[['] = '@class.outer',
            },
        },
    },
})

-- 启用 Treesitter 折叠
vim.opt.foldmethod = 'expr'
vim.opt.foldexpr = 'nvim_treesitter#foldexpr()'
vim.opt.foldlevelstart = 99
```

---

## 五、DAP（调试）

### nvim-dap 配置

```lua
local dap = require('dap')

-- Python 调试
dap.adapters.python = {
    type = 'executable',
    command = 'python',
    args = { '-m', 'debugpy.adapter' },
}

dap.configurations.python = {
    {
        type = 'python',
        request = 'launch',
        name = '调试当前文件',
        program = '${file}',
        console = 'integratedTerminal',
        justMyCode = true,
    },
    {
        type = 'python',
        request = 'launch',
        name = '调试 Django',
        program = 'manage.py',
        args = { 'runserver' },
        django = true,
        console = 'integratedTerminal',
    },
}

-- Node.js 调试
dap.adapters.node = {
    type = 'executable',
    command = 'node',
    args = { os.getenv('HOME') .. '/.vscode/extensions/ms-vscode.js-debug/src/out/ui/serverBootstrap.js' },
}

dap.configurations.javascript = {
    {
        type = 'node',
        request = 'launch',
        name = '调试当前文件',
        program = '${file}',
        cwd = '${workspaceFolder}',
        runtimeArgs = { '--inspect-brk' },
    },
}

-- Go 调试
dap.adapters.go = {
    type = 'executable',
    command = 'dlv',
    args = { 'dap', '--listen=127.0.0.1:38697' },
}

dap.configurations.go = {
    {
        type = 'go',
        request = 'launch',
        name = '调试当前文件',
        program = '${file}',
        dlvToolPath = 'dlv',
    },
    {
        type = 'go',
        request = 'launch',
        name = '调试包测试',
        mode = 'test',
        program = '${fileDirname}',
    },
}

-- DAP 快捷键
vim.keymap.set('n', '<Leader>db', dap.toggle_breakpoint)
vim.keymap.set('n', '<Leader>dc', dap.continue)
vim.keymap.set('n', '<Leader>do', dap.step_over)
vim.keymap.set('n', '<Leader>di', dap.step_into)
vim.keymap.set('n', '<Leader>dO', dap.step_out)
vim.keymap.set('n', '<Leader>dr', dap.repl.toggle)
vim.keymap.set('n', '<Leader>du', dap.ui.widgets.hover)
```

---

## 六、Telescope 配置

```lua
local telescope = require('telescope')
local actions = require('telescope.actions')

telescope.setup({
    defaults = {
        prompt_prefix = "> ",
        selection_caret = "> ",
        path_display = { "smart" },
        mappings = {
            i = {
                ["<C-j>"] = actions.move_selection_next,
                ["<C-k>"] = actions.move_selection_previous,
                ["<C-c>"] = actions.close,
                ["<CR>"] = actions.select_default,
                ["<C-u>"] = actions.preview_scrolling_up,
                ["<C-d>"] = actions.preview_scrolling_down,
            },
            n = {
                ["q"] = actions.close,
            },
        },
    },
    pickers = {
        find_files = {
            hidden = true,
            find_command = { "rg", "--files", "--hidden", "--glob", "!.git" },
        },
        live_grep = {
            additional_args = { "--hidden" },
        },
    },
    extensions = {
        fzf = {
            fuzzy = true,
            override_generic_sorter = true,
            override_file_sorter = true,
            case_mode = "smart_case",
        },
    },
})

-- 加载扩展
telescope.load_extension('fzf')

-- 快捷键
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<Leader>ff', builtin.find_files, { desc = '查找文件' })
vim.keymap.set('n', '<Leader>fg', builtin.live_grep, { desc = '全文搜索' })
vim.keymap.set('n', '<Leader>fb', builtin.buffers, { desc = '缓冲区列表' })
vim.keymap.set('n', '<Leader>fh', builtin.help_tags, { desc = '帮助标签' })
vim.keymap.set('n', '<Leader>fk', builtin.keymaps, { desc = '按键映射' })
vim.keymap.set('n', '<Leader>ft', builtin.treesitter, { desc = 'Treesitter 符号' })
vim.keymap.set('n', '<Leader>fd', builtin.diagnostics, { desc = '诊断列表' })
vim.keymap.set('n', '<Leader>fr', builtin.oldfiles, { desc = '最近文件' })
vim.keymap.set('n', '<Leader>fc', builtin.commands, { desc = '命令列表' })
vim.keymap.set('n', '<Leader>fs', builtin.spell_suggest, { desc = '拼写建议' })
```

---

## 七、完整 init.lua 模板

```lua
-- 1. 基础设置
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.mouse = 'a'
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = false
vim.opt.incsearch = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.autoindent = true
vim.opt.hidden = true
vim.opt.clipboard = 'unnamedplus'
vim.opt.termguicolors = true

-- 2. 快捷键
vim.g.mapleader = ' '
local map = vim.keymap.set
local opts = { noremap = true, silent = true }

map('n', '<Leader>w', ':w<CR>', opts)
map('n', '<Leader>q', ':q<CR>', opts)
map('i', 'jk', '<Esc>', opts)

-- 分割窗口导航
map('n', '<C-h>', '<C-w>h', opts)
map('n', '<C-j>', '<C-w>j', opts)
map('n', '<C-k>', '<C-w>k', opts)
map('n', '<C-l>', '<C-w>l', opts)

-- 3. 插件管理
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        'git', 'clone', '--filter=blob:none',
        'https://github.com/folke/lazy.nvim.git',
        '--branch=stable', lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require('lazy').setup({
    -- 主题
    { 'ellisonleao/gruvbox.nvim', priority = 1000 },
    -- LSP
    { 'neovim/nvim-lspconfig' },
    { 'hrsh7th/nvim-cmp' },
    { 'hrsh7th/cmp-nvim-lsp' },
    -- Treesitter
    { 'nvim-treesitter/nvim-treesitter', build = ':TSUpdate' },
    -- Telescope
    { 'nvim-telescope/telescope.nvim', dependencies = { 'nvim-lua/plenary.nvim' } },
    -- Git
    { 'lewis6991/gitsigns.nvim' },
    { 'tpope/vim-fugitive' },
    -- UI
    { 'folke/which-key.nvim' },
    { 'nvim-lualine/lualine.nvim' },
    { 'windwp/nvim-autopairs' },
})

-- 4. 主题
vim.cmd('colorscheme gruvbox')

-- 5. LSP 和补全（调用独立函数）
require('config.lsp')
require('config.completion')
require('config.treesitter')
require('config.telescope')
```

## 八、性能优化

```lua
-- 加速 Neovim 启动

-- 1. 延迟加载
-- 使用 lazy.nvim 的 event 和 cmd 选项
require('lazy').setup({
    {
        'nvim-telescope/telescope.nvim',
        cmd = 'Telescope',            -- 调用命令时才加载
        keys = { '<Leader>ff' },      -- 按快捷键时才加载
    },
    {
        'lewis6991/gitsigns.nvim',
        event = { 'BufReadPre', 'BufNewFile' },  -- 打开文件时加载
    },
})

-- 2. 禁用不需要的插件
vim.g.loaded_netrw = 1      -- 禁用 netrw
vim.g.loaded_netrwPlugin = 1
vim.g.did_load_filetypes = 0

-- 3. 使用 luajit
-- Neovim 使用 LuaJIT，比标准 Lua 快很多
-- 默认已启用

-- 4. 延迟加载 Treesitter
vim.opt.foldmethod = 'manual'  -- 不用 Treesitter 折叠

-- 5. 关闭 swap/backup
vim.opt.swapfile = false
vim.opt.backup = false
```

## 相关条目

- [[Plugins]]
- [[Config]]
- [[Bash]]
- [[Scripting]]
- [[Basics]]
