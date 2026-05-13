# Vim 配置指南

## 一、配置文件位置

| 版本 | 配置文件路径 |
|------|-------------|
| Vim (Unix) | ~/.vimrc |
| Vim (Windows) | ~/_vimrc 或 $HOME/vimfiles/vimrc |
| Neovim | ~/.config/nvim/init.lua 或 ~/.config/nvim/init.vim |

---

## 二、基本设置

### 常用设置项

```vim
" === 基础设置 ===
set nocompatible            " 不与 vi 兼容
filetype plugin indent on   " 文件类型检测

" === 显示设置 ===
set number                  " 显示行号
set relativenumber          " 相对行号
set cursorline              " 高亮当前行
set showcmd                 " 显示命令
set showmode                " 显示模式
set ruler                   " 显示光标位置
set laststatus=2            " 始终显示状态栏
set list                    " 显示不可见字符
set listchars=tab:>-,trail:·,extends:>,precedes:<

" === 搜索设置 ===
set hlsearch                " 高亮搜索结果
set incsearch               " 增量搜索
set ignorecase              " 搜索忽略大小写
set smartcase               " 如果有大写则区分大小写
set wrapscan                " 搜索到文件尾后回到开头

" === 编辑设置 ===
set tabstop=4               " Tab 宽度
set shiftwidth=4            " 缩进宽度
set softtabstop=4           " 按退格删除时一次删除 4 个空格
set expandtab               " 用空格替代 Tab
set autoindent              " 自动缩进
set smartindent             " 智能缩进
set wrap                    " 自动换行
set textwidth=80            " 80 列提醒
set colorcolumn=80          " 80 列标记线
set backspace=indent,eol,start  " 允许退格删除

" === 编码设置 ===
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,gbk,big5,latin1

" === 备份和交换文件 ===
set nobackup                " 不创建备份文件
set nowritebackup
set noswapfile              " 不创建交换文件
" 或者将交换文件集中存放
" set backupdir=~/.vim/backup//
" set directory=~/.vim/swap//

" === 折叠 ===
set foldmethod=indent       " 基于缩进折叠
set foldlevelstart=99       " 默认全部展开
set foldenable

" === 补全 ===
set completeopt=menu,menuone,noselect
set wildmenu                " 命令补全菜单
set wildmode=list:longest,full

" === 鼠标 ===
set mouse=a                 " 启用鼠标支持
set selectmode=mouse,key

" === 其他 ===
set clipboard=unnamedplus   " 使用系统剪贴板
set timeoutlen=500          " 按键超时（毫秒）
set ttimeoutlen=0           " 减少 Esc 延迟
set hidden                  " 允许修改时切换缓冲区
set autoread                " 文件外部修改时自动重读
set confirm                 " 退出时提示保存
set history=1000            " 命令历史
set undofile                " 持久化撤销历史
set undodir=~/.vim/undo//
```

---

## 三、按键映射

### 映射前缀

```vim
" 设置空格为 <LEADER>
let mapleader = " "
let maplocalleader = ","

" 提示按键等待时间（默认 1000ms）
set timeoutlen=500
```

### 常用映射

```vim
" === Normal 模式映射 ===

" 保存和退出
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>x :x<CR>
nnoremap <Leader>wq :wq<CR>

" 清除搜索高亮
nnoremap <Leader>h :nohlsearch<CR>

" 快速编辑和加载配置
nnoremap <Leader>ev :vsplit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>

" 移动（不退出插入模式）
inoremap jk <Esc>
inoremap kj <Esc>

" 分屏导航
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" 分屏操作
nnoremap <Leader>sv :vsplit<CR>
nnoremap <Leader>sh :split<CR>
nnoremap <Leader>sc :close<CR>

" Tab 操作
nnoremap <Leader>tn :tabnew<CR>
nnoremap <Leader>tl :tabnext<CR>
nnoremap <Leader>th :tabprevious<CR>
nnoremap <Leader>tc :tabclose<CR>

" 保持视觉选择
vnoremap > >gv
vnoremap < <gv

" 缓冲区操作
nnoremap <Leader>bn :bnext<CR>
nnoremap <Leader>bp :bprevious<CR>
nnoremap <Leader>bd :bdelete<CR>

" 系统剪贴板
nnoremap <Leader>y "+y
vnoremap <Leader>y "+y
nnoremap <Leader>p "+p
nnoremap <Leader>P "+P

" 快速移动
nnoremap J 5j
nnoremap K 5k

" 行移动（Alt+↑/↓）
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

" 更好的 escape
inoremap <C-c> <Esc>

" 打开终端
nnoremap <Leader>t :terminal<CR>
```

---

## 四、缩写

```vim
" 常用缩写
iabbrev @@ zhangsan@example.com
iabbrev ssig -- \n张三\n高级工程师
iabbrev #i #include <stdio.h>
iabbrev #d #define
iabbrev main() int main(int argc, char *argv[]) {\n    \n    return 0;\n}

" 修正常见拼写错误
iabbrev recieve receive
iabbrev teh the
iabbrev adn and
iabbrev waht what
```

---

## 五、Autocommands

```vim
" 保存时自动删除行尾空白
autocmd BufWritePre * :%s/\s\+$//e

" 恢复光标位置
autocmd BufReadPost *
    \ if line("'\"") > 1 && line("'\"") <= line("$") |
    \   execute "normal! g`\"" |
    \ endif

" 特定文件类型设置
autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4
autocmd FileType javascript setlocal tabstop=2 shiftwidth=2 softtabstop=2
autocmd FileType typescript setlocal tabstop=2 shiftwidth=2 softtabstop=2
autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4
autocmd FileType markdown setlocal textwidth=0 wrap

" 自动创建目录
autocmd BufWritePre *
    \ if !isdirectory(expand("<afile>:p:h")) |
    \   call mkdir(expand("<afile>:p:h"), "p") |
    \ endif

" 离开插入模式自动保存
autocmd InsertLeave * if &modifiable | silent! write | endif
```

---

## 六、完整 init.vim 示例

```vim
" 基础设置
set nocompatible
filetype plugin indent on
syntax on

set number relativenumber
set cursorline
set hlsearch incsearch smartcase ignorecase
set tabstop=4 shiftwidth=4 softtabstop=4 expandtab
set autoindent smartindent
set backspace=indent,eol,start
set hidden autoread
set nobackup noswapfile nowritebackup
set mouse=a
set clipboard=unnamedplus
set timeoutlen=500 ttimeoutlen=0
set laststatus=2 showcmd showmode ruler
set encoding=utf-8
set splitright splitbelow

" 按键映射
let mapleader = " "

nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>x :x<CR>
nnoremap <Leader>h :nohlsearch<CR>
nnoremap <Leader>ev :vsplit $MYVIMRC<CR>
nnoremap <Leader>sv :source $MYVIMRC<CR>

inoremap jk <Esc>
inoremap kj <Esc>

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" 缩写
iabbrev @@ zhangsan@example.com

" Autocommands
autocmd BufWritePre * :%s/\s\+$//e

autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4
autocmd FileType javascript,typescript setlocal tabstop=2 shiftwidth=2 softtabstop=2
```

## 七、完整 init.lua 示例 (Neovim)

```lua
-- 基本设置
vim.opt.nocompatible = true
vim.cmd('filetype plugin indent on')
vim.cmd('syntax on')

vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.hlsearch = true
vim.opt.incsearch = true
vim.opt.smartcase = true
vim.opt.ignorecase = true

vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.softtabstop = 4
vim.opt.expandtab = true
vim.opt.autoindent = true
vim.opt.smartindent = true

vim.opt.hidden = true
vim.opt.autoread = true
vim.opt.mouse = 'a'
vim.opt.clipboard = 'unnamedplus'
vim.opt.timeoutlen = 500
vim.opt.ttimeoutlen = 0
vim.opt.laststatus = 2
vim.opt.showcmd = true
vim.opt.showmode = true
vim.opt.ruler = true
vim.opt.encoding = 'utf-8'
vim.opt.splitright = true
vim.opt.splitbelow = true

-- 按键映射
local map = vim.keymap.set
local opts = { noremap = true, silent = true }

map('n', '<Leader>w', ':w<CR>', opts)
map('n', '<Leader>q', ':q<CR>', opts)
map('n', '<Leader>x', ':x<CR>', opts)
map('n', '<Leader>h', ':nohlsearch<CR>', opts)
map('n', '<Leader>ev', ':vsplit $MYVIMRC<CR>', opts)
map('n', '<Leader>sv', ':source $MYVIMRC<CR>', opts)
map('i', 'jk', '<Esc>', opts)
map('i', 'kj', '<Esc>', opts)

-- 缩写
vim.cmd('iabbrev @@ zhangsan@example.com')

-- Autocommands
vim.api.nvim_create_autocmd('BufWritePre', {
    pattern = '*',
    callback = function()
        vim.cmd(%s/\s\+$//e)
    end
})

vim.api.nvim_create_autocmd('FileType', {
    pattern = 'python',
    callback = function()
        vim.opt_local.tabstop = 4
        vim.opt_local.shiftwidth = 4
        vim.opt_local.softtabstop = 4
    end
})

vim.api.nvim_create_autocmd('FileType', {
    pattern = { 'javascript', 'typescript' },
    callback = function()
        vim.opt_local.tabstop = 2
        vim.opt_local.shiftwidth = 2
        vim.opt_local.softtabstop = 2
    end
})
```

## 相关条目

- [[Neovim]]
- [[Plugins]]
- [[Basics]]
- [[Bash]]
- [[Environment]]
