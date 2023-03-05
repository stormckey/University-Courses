define printlist
    set $list = *(unsigned int **) $arg0
    while $list
        print /x $list
        set $list = *($list+1)
    end
end
alias pl = printlist