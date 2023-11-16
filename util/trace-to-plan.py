"""
C:/Users/Henrik/Downloads/verifypn-win64/verifypn-win64.exe : Trace:
At line:1 char:1
+ C:/Users/Henrik/Downloads/verifypn-win64/verifypn-win64.exe --search- ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Trace::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
<trace>
	<transition id="unstack b5 b2" index="88">
		<token place="Atom_clear_b5_" age="0"/>
		<token place="Atom_arm_empty__" age="0"/>
		<token place="Atom_on_b5__b2_" age="0"/>
	</transition>
	<transition id="stack b5 b6" index="98">
		<token place="Atom_clear_b6_" age="0"/>
		<token place="Atom_holding_b5_" age="0"/>
	</transition>
</trace>
"""

# Parse the format above and generate the following format:

"""
(unstack b5 b2)
(stack b5 b6)
"""
import argparse
import re

def parse_trace_file(filename):
    with open(filename, 'r', encoding='utf-16') as f:
        trace = f.read()
    return parse_trace(trace)

def parse_trace(trace):
    pattern = r'<transition id="(.*?)"'
    matches = re.findall(pattern, trace)
    return "\n".join(f"({match})" for match in matches)

def generate_sas_plan(trace):
    with open('tapaal_sas_plan', 'w') as f:
        f.write(trace)

parser = argparse.ArgumentParser(description='Parse TAPAAL trace and generate SAS plan')
parser.add_argument('filename', type=str, help='Path to the trace file')
args = parser.parse_args()
generate_sas_plan(parse_trace_file(args.filename))
    

