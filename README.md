This project is a simple implementation of a Turing machine.  
This is a project for educational purposes in order to understand the operation of a Turing machine.

# Install
```pip install .``` or ```poetry install```

# Using
```
Usage: tmachine [OPTIONS] PROGRAM_PATH

  Run a program with turing machine

Arguments:
  PROGRAM_PATH  [required]

Options:
  -n, --number INTEGER            Numbers to initialize on the machine tape
                                  before program execution
  -s, --tape-size INTEGER         Tape size  [default: 71]
  -o, --origin INTEGER            Tape origin index  [default: 35]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
  ```





# Write programs

## Commands available

| Command | Description |
| --- | --- |
| < and > | Move reading head left or right |
| print | Displays state machine |
| write(0) and write(1) | Write 0 or 1 on the tape |
| loop: | Starts a loop |
endif(0) and endif(1) | Exits the loop or progam if a 0 or 1 is written on the tape

## Write loops
Please respect indentations to write loops, tab or 4 spaces as below:

```
loop:
    ....
    ....
    loop:
        ....
        ....
        endif(0)
        ....
    ....
    endif(1)
....
```

# Example

Example to duplicate a number:

## Program
```
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

```

## Command

```bash
tmachine ./test-programs/duplicates.TSP -n 4
```

## Output
```
                                    ↓                                    
 00000000000000000000000000000000000111110000000000000000000000000000000 
 ┴────┴────┴────┴────┴────┴────┴────┼────┴────┴────┴────┴────┴────┴────┴ 
                                    0                                    

                                          ↓                              
 00000000000000000000000000000000000111110000000000000000000000000000000 
 ┴────┴────┴────┴────┴────┴────┴────┼────┴────┴────┴────┴────┴────┴────┴ 
                                    0                                    

                                   ↓                                     
 00000000000000000000000000000000000100000111110000000000000000000000000 
 ┴────┴────┴────┴────┴────┴────┴────┼────┴────┴────┴────┴────┴────┴────┴ 
                                    0                                    

                                          ↓                              
 00000000000000000000000000000000000111110111110000000000000000000000000 
 ┴────┴────┴────┴────┴────┴────┴────┼────┴────┴────┴────┴────┴────┴────┴ 
                                    0
```
