import subprocess
import os.path
import os


def command_str(args: list[str]) -> None:
    if len(args) == 0:
        return ""
    elif len(args) == 1:
        return args[0]
    else:
        seperator = "\" \""
        return f'{args[0]} "{seperator.join(args[1:])}"'


def run_process(args: list[str], directory: str) -> str:
    print(f"Running: {command_str(args)}")
    p = subprocess.call(args,
        # stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=directory,
        shell=True
    )
    
    # return p.stdout.decode("utf-8")
    return ""


def run_process_timed(args: list[str], directory: str) -> str:
    # return run_process(["time"] + args + [">>", "out.txt"], directory)
    timed_command_piped_to_file(args, "out.txt", "time.txt", directory)
    return ""


def timed_command_piped_to_file(args: list[str], outfile: str, outfile_time: str, directory: str = None) -> None:
    command = command_str(["time"] + args)

    
    if directory is not None:
        full_command =  f'(cd "{os.path.abspath(directory)}"; ({command} > {outfile}) 2> {outfile_time})'
    else:
        full_command = f'({command} > {outfile}) 2> {outfile_time}'
    
    with open("run.sh", "a") as f:
        print(full_command)
        f.write(f"{full_command}\n")
        # print(full_command, f)

    # p = os.system(full_command)

    # print(p)
