import os
if os.getcwd().strip('/').endswith('tests'):
    fname = './.isbndbkey'
else:
    fname = 'tests/.isbndbkey'

KEY = open(fname,'r').read().strip()
