# Shell Notes (revisited)
- $PATH : the variable of all env vars
- \> redirect to >> append to
- the tee command : echo while write to the file at the same time (similar to echo ,input coms from stdin)
- The args in .sh is denoted by \$1 \$2
- touch can be used to create a new file, but we have to change the state of it before we run it (chmod +x)
- to compare if two string is equal `if [ "$1" = "Hello" ]; then`
- to concatenate strings juest put them together `"Hello ""World!"`