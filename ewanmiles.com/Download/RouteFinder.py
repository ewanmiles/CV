#####################################################################################################################################################################
# ROUTEFINDER FILE NAVIGATOR
# Ewan Miles - 06/05/2020
# This code is entirely open-source and thus is editable by anyone.
#----------------------------------------------------------------------#
# This program is designed to be used in a terminal, but can be used in an editor with an interactive iPython window.
# To use in the terminal, navigate to the directory where this file is saved and start a python session by typing "python" and pressing Enter.
# Following that, write "from RouteFinder import RouteFinder, filesearch".
# Please note that this program only works for local file systems; it cannot locate directories on an external server for example.
#----------------------------------------------------------------------#
# RouteFinder() is used to return the path from this file's directory to the desired directory as a string.
# Its first argument should be given by ".", e.g. RouteFinder(".",...), which indicates it should start in its current directory.
# All arguments should be given as strings and as such should be surrounded by "quotes".
# It can only explore to subdirectories, not "upwards"; for this reason, saving this file in the highest directory possible is recommended (e.g. Desktop, user)
#----------------------------------------------------------------------#
# filesearch() is used to return the path from one directory to another (both subdirectories from this file's location) as a string.
# The path will go FROM the first argument TO the second argument, e.g. filesearch("filea","fileb") will give the path from filea to fileb.
# Again, all arguments should be surrounded by "quotes".
# This does not give the shortest path. It instead gives a path that goes from the first location, up to this directory, then down to the desired location.
#----------------------------------------------------------------------#
# I hope you enjoy using this rudimentary navigator! It is very simple, but will save time when navigating large file systems!

from pathlib import Path

def RouteFinder(d,file):
    """
    Function that prints the full filepath from current directory to desired file, with inputs:
    - d: Initial directory to start browse
    - file: Name of file that is being searched for
    Prints ONLY the filepath to desired file, but may print alternative filepaths if filename is
    string contained within other filenames in any directories
    ALSO declares global variable "pathup" which is necessary "../" path to d from file
    """
    
    #Global variables necessary for checking condition and for later use
    global pathup
    global path
    
    #Iterate through each subdirectory returning string path
    for i in Path(d).iterdir():
        if file in str(i):
            #Check if desired file location in string as a folder
            if "{0}/".format(file) in str(i):
                pass
            else:
                if "levels" in locals():
                    pass
                else:
                    #Count levels down to file location
                    levels = str(i).count("/") + 1
                    pathup = (levels * "../")
                    #Path to file location
                    path = i
        else:
            try:
                RouteFinder(i,file)
            except NotADirectoryError:
                continue
    #Check if valid path has been found by checking global variables, return valid path
    if "path" in globals():
        return str(path)

def filesearch(filestart,filename):
    """
    Function that returns the route to a file from a separate file, with a shared parent directory, with inputs:
    - filestart: Name of file to start route search from
    - filename: Name of file to find in search
    REQUIRES that the function is saved in the top parent directory (earliest directory that shares the starting
    and desired file)
    Returns full path from start file to desired file
    """
    
    #Path from top directory to start file location
    startpath = RouteFinder(".",filestart)  #This is not used, but is necessary to find dirs variable as pathup variable is global

    #Number of necessary "../" to reach top directory from start location
    dirs = pathup

    #Path from top directory to end file location
    endpath = RouteFinder(".",filename)

    #Full path is startpath "../" attached to endpath
    fullpath = dirs + str(endpath)
    
    return fullpath