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


def timed_command_piped_to_file(args: list[str], outfile: str, outfile_time: str, directory: str = None) -> str:
    command = command_str(["time"] + args)

    
    if directory is not None:
        full_path = os.path.abspath(directory)
        rel_path = os.path.relpath(full_path)
        rel_out_path = os.path.relpath(outfile, full_path)
        rel_time_path = os.path.relpath(outfile_time, full_path)
        full_command =  f'(cd "{rel_path}"; ({command} > "{rel_out_path}") 2> "{rel_time_path}")'
    else:
        full_command = f'({command} > {outfile}) 2> {outfile_time}'

    return full_command
    
    # with open("run.sh", "a") as f:
    #     print(full_command)
    #     f.write(f"{full_command}\n")
        # print(full_command, f)

    # p = os.system(full_command)

    # print(p)
