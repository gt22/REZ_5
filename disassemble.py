import subprocess
import re
import sys

pattern = re.compile(r'.*\/\/ Method ([^\.]+)\.[^:]+:\(([^)]*)\)(.+)')


def parse_types(s):
    res = []
    while s:
        c = s[0]
        if c != 'L':
            s = s[1:]
            continue
        end = s.find(';')
        if end == -1:
            end = len(s)
        res.append(s[1:end].replace('/', '.'))
        s = s[end:]
    return res


def parse_call(c):
    match = re.match(pattern, c)
    receiver = match.group(1).replace('/', '.')

    args = parse_types(match.group(2))
    return_type = parse_types(match.group(3))
    if return_type:
        return_type = return_type[0]
    else:
        return_type = None
    ret = {receiver, *args}
    if return_type is not None:
        ret.add(return_type)
    return ret


def main():
    if len(sys.argv) < 2:
        print("Usage: disassemble.py ClassName")
        return
    s = subprocess.check_output(["javap", "-c", "-p", sys.argv[1]]).decode('utf8').split('\n')
    calls = [x for x in s if 'invokevirtual' in x]
    res = set().union(*[parse_call(c) for c in calls])
    for t in res:
        print(t)


if __name__ == '__main__':
    main()