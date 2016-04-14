**Overview**

**Description**

**Installing isbndb-py**

**Using the ISBDdb.Com Service**

**Example Usage**


# ........ #



## Overview ##
isbndb-py is a Python wrapper for seaching the ISBNdb.com database for bibliographic data on books

## Description ##
The goals of this project are to:

1. allow serches on ISBNdb.com from a python script

2. abstract all http and XML out of a users code

3. do the above in a way that feels natural to python users


To accomplish these goals ISBNDb.py has implemented the following:

1. all searches can be done from a function

2. keys for ISBNDb.com are managed by the program, including access counting to avoid limits

3. Error are raised

4. Search results are returned to act like lists

5. individual books can be accessed as raw XML, ElementTrees, or a native python object.


## Installing isbndb-py ##
isbndb-py is currently available by Subversion repository access (thanks Google Code!). You can checkout the latest version for our repository using:

```
svn checkout http://isbndb-py.googlecode.com/svn/trunk/ isbndb-py-read-only
```

This is a read-only version of the repository. If you would like to commit changes and fixes feel welcome to send an email to join the project.

Updating your working copy is done in the usual way with ` svn update `


## Using the ISBNdb.com Services ##
isbndb-py is a wrapper for searching the ISBNdb.com database. Access to that database requires each developer to have one or more "keys". To register for yours, please visit https://isbndb.com/account/create.html to create an account and follow the instructions to obtain your key(s). I would recommend that you read their remote data access introduction as well: https://isbndb.com/data-intro.html

#### Using your ISBNdb.com Key with isbndb-py ####
Once you have your key:

_This section is yet to be completed_


isbndb-py will now use this key to access ISBNdb.com


## Example Usage ##