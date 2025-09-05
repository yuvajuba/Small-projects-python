import os
import sys
import requests
import hashlib


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check api and try again!')
    return res


def get_password_leaks_counts(hashes, hashes_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_check:
            return count
    return 0


def pwned_api_check(password):
    # hash the password using built-in lib into "sha1" hashing
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_counts(response, tail)


generic_file = "passwords-to-check.txt"
passwords = sys.argv[1:]

if len(passwords) == 0:
    if generic_file in os.listdir("./"):
        with open(generic_file, "r") as f:
            passwords = f.read().splitlines()
        if len(passwords) == 0:
            sys.exit(
                f"{generic_file} is empty! please provide passwords to check")
    else:
        sys.exit(
            f"Please provide passwords to check! either in '{generic_file}' file or inline")


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times ... You should change it!')
        else:
            print(f'{password} is fine ... never been hacked!')
    return '\nDone!'


if __name__ == '__main__':
    sys.exit(main(passwords))
