set smartindent
set tabstop=4
set shiftwidth=4
set expandtab

if exists('+colorcolumn')
    set colorcolumn=80
else
    au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
endif

filetype plugin indent on

autocmd BufWritePre *.py :%s/\s\+$//e
autocmd Filetype html,php setlocal ts=2 sts=2 sw=2
autocmd Filetype javascript setlocal ts=2 sts=2 sw=2
