#!/usr/bin/env python3
import logging
from time import perf_counter
from typing import Any, Callable
import functools
import argparse


def user_input() -> argparse.Namespace:
    """
    Create a new argparse object if the program you want logging does not currently
    have an argparse object.
    """
    parser = argparse. ArgumentParser (description="""
    Debug and info logging enabled on this program
    """)
    parser.add_argument('--debug', action='store_true',
                        help='Run debug logging on the program')
    parser.add_argument('--info', action='store_true',
                        help='Run info logging on the program')
    parser_args = parser.parse_args()

    return parser_args


def add_log_arg(parser: argparse. ArgumentParser) -> argparse. ArgumentParser:
    """
    Simply add log arguments to a pre-made argument parser when imported.

    Args:
        parser (): An argument parser object before arguments are stored.
    Returns:
        parser.add_argument: Additional arguments of --info and --debug
    """
    parser.add_argument('--debug', action='store_true',
                        help='Run debug logging on the program')
    parser.add_argument('--info', action='store_true',
                        help='Run info logging on the program')
    return parser


def set_logging (parser_args: argparse.Namespace):
    """
    Set the logging level based on the user's input
    
    Args:
        parse_args (argparse. Namespace): The object created by the user input
    Returns:
        logging (obj): Logging config object
    """
    if parser_args.debug:
        logging.basicConfig(level=logging.DEBUG,
            format="%(asctime)s | %(levelname)s | PID: %(process)d - %(message)s",
            datefmt="%Y%m%d %H:%M:%S")
        logging.getLogger()
        return logging
    elif parser_args.info:
        logging.basicConfig(level=logging.INFO,
            format="%(levelname)s: % (message)s")
        logging.getLogger()
        return logging
    else:
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger()
        return logging


def timer (func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Get benchmark information every time that a function is called. This will
    calculate the the runtime of all actions in the function and is only to be
    used as a decorator. To view, turn on INFO logging (--info)
    
    Args:
        func: any funtion
    Returns:
        func: same function while calculating benchmark
    """
    @functools.wraps (func) # Fix naming issues when getting function names in decorators
    def wrapper (*args: Any, **kwargs: Any) -> Any: # Take in any args for the wrapper
        start_time = perf_counter()
        process = func(*args, **kwargs) # Take any function from the input
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f"Execution of {func._name_} took {run_time: .4f} Seconds.")
        return process

    return wrapper


def log(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Get the logging information for the functions that are called. This will only be used as a decorator.
    
    Args:
        func: any funtion
    Returns:
        func: same function while storing the logging information
    """
    @functools.wraps (func) # Fix naming issues when getting function names in decorators
    def wrapper (*args: Any, **kwargs: Any) -> Any: # Take in any args for the wrapper
        logging.info(f"Calling function: \'{func._name__}\'")
        process = func(*args, **kwargs) # Take any function from the input
        all_args = locals()
        logging.debug(f" {func._name_} was called with the arguments: \n{all_args}")
        logging.debug(f" {func._name_} defaults are: {func._defaults_}")
        logging.info(f"Finished calling function: \'{func._name_}\'")
        return process # Return the function back

    return wrapper # Return the entire wrapper with function


###### MAIN ####################### 
if __name__ == "__main__": 
    pass 
