# system-commander
Programs and scripts that perform useful actions on a system (usually Linux). Some might require admin/root access on the system

For the most efficient usage, add the dir `/path/to/system-commander/run/` to your environment PATH
> The objects in `run` are symbolic links to the running programs in their respective directories. If you want to add it you can do it manually or run the bash script `add_path.sh` in the `run` directory

<br>

<br>

## ArgParse Mandatory Args
If a user requires that an option is selected when running a program, you can have the program print an error message along with the options using the below:

```python
def main():
    """
    Run the program. Accepts no inputs.
    """
    # Build and store user arguments
    parser = user_input()
    input_args = parser.parse_args()

    # Error if the user does not give an argument
    if all(value == False or value == None
           for value in vars(input_args).values()):
        parser.print_help()
        raise argparse.ArgumentError("NO ARGUMENT GIVEN BUT REQUIRED!")
    
    # Continue doing things


# Only run if executing, not import
if __name__ == "__main__":
    main()
```

<br>

<br>

## Global Decorator
This allows you to add a simple decorator to track and debug a program using built-in utilities.

* Import as `import globalDecorator as gd`
* `@log` - Add info and debug log level as an argument to running the program (`--info`, `--debug`)
* `@timer` - Add a timer to the debug message.

<br>

### No Parser
If your program does not contain an argument parser, do the below.

```python


```

<br>

### Parser
If you program contains a parser then do the below

1. Ensure that the parser is constructed as:
```python
def user_input() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="""
Whatever
""", formatter_class=argparse.RawDescriptionHelpFormatter)
    # ARGUMENTS
    gd.add_log_arg(parser) # Add decorator options

    return parser
```

2. For all functions and classes (Except `user_input` and `main`) you can add the below decorators:
  * `@gd.log` - Add info and debug log level as an argument to running the program (`--info`, `--debug`)
  * `@gd.timer` - Add a timer to the debug message.

<br>

### MAIN
Add this to the main part of your program

```python
def main():
    """
    Run the program. Accepts no inputs.
    """
    # Build and store user arguments
    parser = user_input()
    input_args = parser.parse_args()

    # Configure the logging object
    gd.set_logging(input_args)


# Only run if executing, not import
if __name__ == "__main__":
    main()
```

<br>

<br>

## Programs/Scripts
Below are a list of the programs/scripts that are part of this repository.

> All of the programs have a `-h`, `--help` argument to get details on running. Most also do the same if you give no arguments

<br>

### Programs

* `sys-stat`: Get usage stats on your local Linux system, or search for a process and show linked usage and open files.

<br>

### Scripts

* None

<br>