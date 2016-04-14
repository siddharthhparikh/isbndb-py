ISBNDb.py is a wrapper for ISBNDb.com written in Python.  The goals of this project are:
1. allow serches on ISBNDb from a python script
2. abstract all http and XML out of a users code
3. do the above in a way that feels natural to python users.

To accomplish these goals ISBNDb.py has implemented the following:
1. all searches can be done from a function.
2. keys for ISBNDb.com are managed by the program, including access counting to avoid limits.
3. Error are raised
4. Search results are returned to act like lists.
5. individual books can be accessed as raw XML, ElementTrees, or a native python object.
