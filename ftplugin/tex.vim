" Insert Overleaf comments.
" Author:      Paul Seyfert
" Version:     0.0.0
" WebPage:     https://github.com/pseyfert/overleaf-commenter
" Description: Generate a comment in a TeX file for rendering on overleaf
" License:     AGPL v3, see LICENSE for more details.

let s:save_cpo = &cpo
set cpo&vim
let g:overleaf_comment_py = expand('<sfile>:p:h:h') . '/overleaf_comment.py'

function! Overleafcomment()
  if has('python3')
    execute ':py3file ' . g:overleaf_comment_py
  elseif has('python')
    execute ':pyfile ' . g:overleaf_comment_py
  endif
endfunction

function! Overleafclosediscussion()
  if has('python3')
    python3 import sys
    python3 sys.argv.append('--close')
    execute ':py3file ' . g:overleaf_comment_py
    python3 sys.argv.pop()
  elseif has('python')
    python import sys
    python sys.argv.append('--close')
    execute ':pyfile ' . g:overleaf_comment_py
    python sys.argv.pop()
  endif
endfunc

command! -nargs=0 -buffer -complete=customlist,Overleafcomment OverleafComment call Overleafcomment()
command! -nargs=0 -buffer -complete=customlist,Overleafclosediscussion OverleafCloseDiscussion call Overleafclosediscussion()

let &cpo = s:save_cpo
unlet s:save_cpo
