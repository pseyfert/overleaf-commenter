[![Licence: AGPL v3](https://img.shields.io/github/license/pseyfert/overleaf-commenter.svg)](LICENSE)

# overleaf-commenter

Use Overleaf discussions on a local text editor.

## background

Overleaf is a cloud based collaborative latex editing tool.  (I.e. have a
tex(t) editor in the web browser, automatically re-generate the pdf on the
server and show it in the browser). It's a bit a multi-user compiler-explorer
for TeX.

Discussions on Overleaf are kept in the document (and thus accessible through
the git clone) as tex comments.

![example screenshot](https://i.stack.imgur.com/fV9rJ.png)

The syntax is (simply by looking at what gets generated):

```tex
Some regular $T=e \cdot X$ code.

% * <email@server.tld> 2018-02-05T14:56:52.585Z:
% 
% I would phrase this similar ...
% 
% ^ <other.email@server.tld> 2018-02-12T14:05:57.936Z:
% 
% I agree, I just wanted to make it clear that I think this is a very hard problem.
% 
% ^.
```

I.e. `% *` starts a discussion `% ^.` ends it, and `% ^` is a response.

Overleaf documents can be accessed through git.  One can follow and contribute
to discussions from a local text editor, provided one gets the syntax right -
something your computer should be able to do for you in your local text editor.

## USAGE

### overleaf-commenter can be called from the command line:

```sh
> python vim-overleaf.py

% *^ <email@server.tld> 2018-02-21T07:31:12.752395Z:
%
% WRITEME
%
% ^.
```

You then should pick `^` or `*` and write the comment. `python` may be python2 or python3.

### overleaf-commenter can be called from vim

Add to the `.vimrc` a definition

```viml
function! OverleafComment()
  py3f /path/to/overleaf-commenter/vim-overleaf.py
endfunc
```

or

```viml
map <C-O> py3f /path/to/overleaf-commenter/vim-overleaf.py
```

The vim functionality has a bit of heuristics to determine if a reply is
requested or a new comment will be started. The comment will be inserted
between the current cursor's line and the next line. The distinction is based
on the current line (comparison to `$ ^.`).

## What can/can't go into the comment syntax

Trying around:

 - microseconds (as in ISO8601 formaters) are allowed
 - the time is not checked for "validity" (future postings are okay)
 - the time is UTC
 - time zone information is **not** allowed (the comment will not be picked up as discussion
 - email addresses which do not correspond to overleaf accounts are valid (though no avatar and author information will get rendered)



## Behind the scenes

 - overleaf-commenter obtains the email address through git. (Since the git commit email address and the accouunt on overleaf are independent, this might actually be wrong)
