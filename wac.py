#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uses a url file to check each url against a supplied auth mechanism and
# determines which urls had access to or not so we can determine urls
# that may be unsecured for certain roles

import os
import sys
import re

from argparse import ArgumentParser, FileType
from Queue import Queue
from threading import Thread

import requests

# consts
DEF_THREADS = 10 # worker threads

# HTTP statuses
STATUS_REDIRECT = 302
STATUS_UNAUTHORIZED = 401

# globals
args = ()
urls = Queue()
remaining = 0


def work():
  global remaining

  try:
    while not urls.empty():
      url = urls.get()
      headers = {}
      user = None
      pwd = None

      # keep the user informed of progress
      if remaining % 30 == 0:
        print "[+] remaining requests: %d" % remaining

      if args.cookie:
        headers['Cookie'] = args.cookie

      if args.auth:
        user, pwd = args.auth.split(":")

      try:
        resp = requests.get(url, headers=headers, allow_redirects=False, auth=(user, pwd))

        # check different requirements
        if not args.status is None:
          if args.status == resp.status_code:
            args.output.write("DENIED %s\n" % url)
            continue

        if not args.redirect is None:
          if resp.status_code == STATUS_REDIRECT:
            location = resp.headers['location']
            if re.search(args.redirect, location, re.IGNORECASE):
              args.output.write("DENIED %s\n" % url)
              continue

        if not args.body is None:
          if re.search(args.body, resp.text):
            args.output.write("DENIED %s\n" % url)
            continue

        # if they made it to here then they have access
        args.output.write("GRANTED %s\n" % url)

      except requests.exceptions.RequestException as e:
        args.output.write("FAIL %s:%s\n" % (url, e))
      finally:
        remaining -= 1

  except KeyboardInterrupt:
     print "[!] cancelled by user"
     sys.exit(1)


def main():
  global remaining
  if args.cookie:
    print "[*] cookie: %s" % args.cookie

  if args.auth:
    print "[*] auth: %s" % args.auth

  print "[*] url file: %s" % args.url_file.name
  print "[*] threads: %d" % args.threads

  # read in the urls to be processed
  try:
    for line in args.url_file:
      url = line.rstrip("\n")
      urls.put(url)
      remaining += 1
  finally:
    args.url_file.close()

  print "[*] urls found: %d" % remaining 

  # output header
  args.output.write("STATUS URL DETAILS\n")

  # spin up the threads to do the work
  for i in range(args.threads):
    t = Thread(name="web req thread: %d" % i, target=work)
    t.start()


if __name__ == "__main__":
  parser = ArgumentParser("Web Auth Checker")

  # madatory args
  parser.add_argument("url_file", help="file with urls to check (use - for STDIN)", type=FileType("r"), metavar="URL_FILE", default=sys.stdin)

  # options args
  parser.add_argument("-t", "--threads", help="number of request threads (default %d)" % DEF_THREADS, type=int, default=DEF_THREADS)
  parser.add_argument("-c", "--cookie", help="cookie to use for requests", type=str)
  parser.add_argument("-a", "--auth", help="authorization to use for requests in format user:pwd", type=str)
  parser.add_argument("-o", "--output", help="output file (default STDOUT)", type=FileType("w"), default=sys.stdout)

  # reponse options
  parser.add_argument("-r", "--redirect", help="check for a redirect using status of 302 and Location header", type=str)
  parser.add_argument("-s", "--status", help="check for a specific HTTP status", type=int)
  parser.add_argument("-b", "--body", help="check custom body content returned in response, regex is supported", type=str)

  args = parser.parse_args()
  main()
