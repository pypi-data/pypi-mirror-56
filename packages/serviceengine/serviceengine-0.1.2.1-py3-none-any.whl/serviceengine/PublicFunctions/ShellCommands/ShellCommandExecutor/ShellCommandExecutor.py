#!/usr/bin/python3
import subprocess


def RunSubProcess(commandLineInput, logger):
    try:
        logger.DEBUG(f"Running shell command: {commandLineInput}")
        result = subprocess.run(commandLineInput, shell=True, check=True, stdout=subprocess.PIPE)
        logger.INFO(result.stdout.decode('utf-8'))
    except Exception as ex:
        logger.Error(f"Failed execute bash command '{commandLineInput}', exception encountered:\n{ex}")