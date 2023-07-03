import os
import sys
import argparse

# NOMERGE exclude

no_merges = []
files_scanned = []

def scan_single_file(fpath) -> bool:
    "return false if NOMERGE detected"
    with open(fpath) as fin:
        files_scanned.append(fpath)
        for i, line in enumerate(fin):
            if "NOMERGE exclude" in line:
                break
            if "NOMERGE" in line:
                item = {
                        "file": fpath, "line_number": i+1, "line": line.strip()
                        }
                no_merges.append(item)



def scan_dir(basedir, excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = []
    for root, dirs, files in os.walk(basedir):
        for f in files:
            if f.endswith(".py"):
                fpath = os.path.join(root, f)
                scan_single_file(fpath)


def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-d", "--basedir", default=".")
    #parser.add_argument("-x", "--exclude-dirs", default=None)


    #args = parser.parse_args()

    #scan_dir(args.basedir)
    for f in sys.argv[1:]:
        scan_single_file(f)
    print(f"NOMERGE scanned {len(files_scanned)} files")
    if len(no_merges) == 0:
        print("OK")
    elif len(no_merges) > 0:
        print(f"NOMERGE found {len(no_merges)} times")
        for item in no_merges:
            print(f"[{item['file']}:{item['line_number']}] {item['line']}")
        exit(1)


if __name__ == "__main__":
    main()
