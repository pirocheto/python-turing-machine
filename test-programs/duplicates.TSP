print
endif(0)

loop:
    endif(0)
    >
>
print
loop:
    write(1)
    loop:
        <
        endif(0)
    loop:
        <
        endif(1)
    <
    endif(0)
    >
    write(0)
    loop:
        >
        endif(1)
    loop:
        >
        endif(0)
print
>

loop:
    >
    endif(1)
    write(1)
<
write(0)
>
print

