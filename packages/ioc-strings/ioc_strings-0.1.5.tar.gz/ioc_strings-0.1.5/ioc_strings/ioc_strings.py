import os
import sys
import subprocess
import argparse
import string
import json
import multiprocessing
import base64
import time

import iocextract
import validators


global CPU_COUNT
global LOCK
CPU_COUNT = multiprocessing.cpu_count()
LOCK = multiprocessing.Lock()


class IOC:

    def __init__(self, ioc="", args={}, filepath=""):
        self.ioc = ioc.strip()
        self.ioc_types = []

        check_functions = [
            self.check_ip,
            self.check_domain,
            self.check_file,
            self.check_hash,
            self.check_url,
            self.check_email,
            self.check_base64
        ]

        for check in check_functions:
            result = check(ioc)
            if result and result not in self.ioc_types:
                self.ioc_types.append(result)

        self.handle_other_type()
        self.handle_domain_type()
        self.data = {"ioc": self.ioc, "ioc_types": self.ioc_types}

        if args["fileinfo"] and len(filepath) > 0:
            self.data["fileinfo"] = {"filepath": filepath}

        if args["filter"]:
            if not args["filter"] in self.ioc_types:
                return

        with LOCK:
            if args["t"] and self.is_ioc():
                print(json.dumps(self.data))
            elif not args["t"] and self.is_ioc():
                print(self.ioc)

    def handle_other_type(self):
        # When "other" is not the only ioc_type, remove "other" from ioc_types
        if "other" in self.ioc_types and len(self.ioc_types) != 1:
            self.ioc_types.remove("other")

    def handle_domain_type(self):
        if "domain" in self.ioc_types and len(self.ioc_types) != 1:
            self.ioc_types.remove("domain")

    def is_ioc(self):
        if len(self.ioc_types) != 0:
            return True
        else:
            return False

    def check_domain(self, ioc):
        result1 = validators.domain(ioc)

        if not result1:
            return False

        return "domain"

    def check_email(self, ioc):
        ioc = ioc.lower()

        result1 = validators.email(ioc)

        if not result1:
            return False

        result2 = list(iocextract.extract_emails(ioc, refang=True))
        if not result2:
            return False

        self.ioc = result2[0]
        return "mail"

    def check_ip(self, ioc):
        ioc = ioc.lower()

        result4_2 = list(iocextract.extract_ipv4s(ioc, refang=True))
        result6_2 = list(iocextract.extract_ipv6s(ioc))

        if not result4_2 and not result6_2:
            return False

        if result4_2:
            self.ioc = result4_2[0]
        elif result6_2:
            self.ioc = result6_2[0]

        return "ip"

    def check_url(self, ioc):
        result1 = list(iocextract.extract_urls(ioc, refang=True))

        if not result1:
            return False

        self.ioc = result1[0]
        return "url"

    def check_file(self, ioc):
        if os.path.isfile(ioc):
            return "file"
        
        return False

    def check_hash(self, ioc):
        result = list(iocextract.extract_hashes(ioc))

        if not result:
            return False

        self.ioc = result[0]
        return "hash"

    def check_base64(self, ioc):
        if len(ioc) < 40:
            return False

        try:
            test_ioc = base64.b64encode(base64.b64decode(bytes(ioc, "utf-8")))
            if not test_ioc == bytes(ioc, "utf-8"):
                raise Exception
            
            return "other"
        except:
            return False
        

def run_strings(args, filepath):
    strings = subprocess.check_output(["strings", "-n", str(args["n"]), filepath])
    strings = str(strings, "utf-8").split("\n")

    strings_by_whitespace = []
    for s in strings:
        for s_by_whitespace in s.split():
            if len(s_by_whitespace) >= args["n"]:
                strings_by_whitespace.append(s_by_whitespace)

    return strings_by_whitespace


def handle_filepath(args, filepath):
    strings = run_strings(args, filepath)
    for s in strings:
        s = s.strip()
        ioc = IOC(s, args, filepath=filepath)


def main():
    parser = argparse.ArgumentParser(description="Get IOC types from file")
    parser.add_argument("filepath", help="Path to file or folder containing files")
    parser.add_argument("-n", help="Locate & print any NUL-terminated sequence of at least [number] characters (default 10)", default=7)
    parser.add_argument("-t", help="Output as JSON with IOC types", action="store_true", default=False)
    parser.add_argument("--filter", help="Filter by type (ip, domain, url, file, hash, email)")
    parser.add_argument("--singleprocess", help="Use single process instead of multiprocessing", action="store_true", default=False)
    parser.add_argument("--fileinfo", help="Display file which contained the IOC", action="store_true", default=False)
    args = vars(parser.parse_args())

    if not os.path.exists(args["filepath"]):
        print("Path {} does not exist.".format(args["filepath"]))
        exit()

    if os.path.isfile(args["filepath"]):
        filepaths = [args["filepath"]]
    else:
        filepaths = []
        for root, subdir, filenames in os.walk(args["filepath"]):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                filepaths.append(filepath)

    if not args["singleprocess"]:
        file_count = 0
        filepaths_amount = len(filepaths)
        while True:
            if file_count == filepaths_amount and len(multiprocessing.active_children()) == 0:
                break

            if len(multiprocessing.active_children()) < CPU_COUNT and file_count != filepaths_amount:
                filepath = filepaths[file_count]
                p = multiprocessing.Process(target=handle_filepath, args=(args, filepath))
                p.daemon = True
                p.start()
                file_count += 1
    else:
        for filepath in filepaths:
            handle_filepath(args, filepath)


if __name__ == "__main__":
    main()