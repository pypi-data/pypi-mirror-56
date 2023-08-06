# MIT
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://bitbucket.org/gurpreet-anand/say-greetings/src/master/say-greetings/
# Filename: greetings.py
# Description: Main script for `greetings` app.

import argparse
from random import choice


def main():

    parser = argparse.ArgumentParser(prog='greetings', description='A simple command-line app to greet!')

    parser.add_argument('-t', '--title', required=False, dest='title')
    parser.add_argument('-f', '--first-name', required=False, dest='first_name')
    parser.add_argument('-m', '--middle-name', required=False, dest='middle_name')
    parser.add_argument('-l', '--last-name', required=False, dest='last_name')

    args = parser.parse_args()
    kwargs = vars(args)

    greetings = [ 'Bonjour', 'Hola', 'Guten Tag', 'Ciao', 'Namaste', 'Salaam']

    name = ' '.join([word for word in kwargs.values() if word is not None])
    print('{greeting}! {name}'.format(greeting=choice(greetings), name=name))

