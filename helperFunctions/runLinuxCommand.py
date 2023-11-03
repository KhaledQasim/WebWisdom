import subprocess


def runCommand(cmd):
    """Runs a command in the linux shell and returns the output

    Args:
        (string): the command to be run and all of its arguments

    Returns:
        (array): the output of the command, including stdout and stderr and return-code
    """
    output = subprocess.run([cmd],shell=True, capture_output=True)
    return output