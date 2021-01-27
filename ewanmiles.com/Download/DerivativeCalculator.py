#####################################################################################################################################################################
# DERIVATIVE CALCULATOR
# Ewan Miles - 25/09/2020
# This code is entirely open-source and thus is editable by anyone.
#----------------------------------------------------------------------#
# This program is essentially a library of functions, with "diff" incorporating all others at one point or another.
# As there is no GUI and the file is not an executable, it will need to be run in a script editor capable of running a python session.
# This means it can be run in the terminal; I personally call it in Visual Studio Code.
#----------------------------------------------------------------------#
# The code is split up below into various sections:
# > BASE handles any input processing, e.g. separating terms, finding coefficients or subject variables, etc;
# > MULTIPLICATIVE handles all the functions used in multiplications of expressions;
# > DIVISIVE handles all the functions used in division of expressions;
# > DIFFERENTIATION handles all of the different types of differentiation included in this script.
#----------------------------------------------------------------------#
# The function "diff()" at the end of DIFFERENTIATION is the final product of all the work in the script.
# It can handle differentiation for simple variables, trig functions, products, e, ln, and various combinations of each.
# To help you understand, I have left in my TESTING section at the bottom, which will print all of the differentation results of over 200 expressions.
# To see the results, run the whole TESTING section at once; it will print each expression alongside its first derivative.
#----------------------------------------------------------------------#
# I've tried to prepare the script for as many false inputs as possible - which is the main reason the function "brackets()" exists.
# This is meant to allow you to include as many brackets as you like in the expression, while helping the script run regardless.
# There are a few exceptions, where I have included my own raised errors.
# These include putting brackets around powers of e, or brackets around the content of ln.
#----------------------------------------------------------------------#
# The logic in the script isn't perfect - if what you're looking for doesn't work the first time, play around with it!
# Play around with the code and add to it/see what stuff does/use it for any means.
# Thanks for using my script! I hope you get all you want from it.
#####################################################################################################################################################################

### DICTIONARIES #############################
trigrecip = {
    # Reciprocates trig functions for division/multiplication
    "sin": "csc",
    "cos": "sec",
    "tan": "cot",
    "csc": "sin",
    "sec": "cos",
    "cot": "tan"
}

trigmult = {
    # Certain simplified multiplications of trig functions
    "tancos": "sin",
    "costan": "sin",
    "csccos": "cot",
    "coscsc": "cot",
    "csctan": "sec",
    "tancsc": "sec",
    "sinsec": "tan",
    "secsin": "tan",
    "cotsin": "cos",
    "sincot": "cos",
    "cotsec": "csc",
    "seccot": "csc",
    "sincsc": "",
    "cossec": "",
    "tancot": "",
    "cscsin": "",
    "seccos": "",
    "cottan": ""
}

trigdiff = {
    # The first derivatives of each trig function used in diff functions
    "sin": "cos",
    "cos": "-sin",
    "tan": "sec^2",
    "csc": ("-cot","csc"),
    "sec": ("tan","sec"),
    "cot": "-csc^2"
}
##############################################

### BASE #####################################
def brackets(x):
    """
    Removes all brackets (parentheses, "(",")" ) from an input string, with input

    - x: Expression possibly containing brackets (str)

    Returns string with all brackets removed
    """
    while "(" in x:
        x = x.replace("(","") #Replace opening paren with nothing while present in expression
    while ")" in x:
        x = x.replace(")","") #Replace closing paren with nothing while present in expression
    return x

def rotate(x):
    """
    Rotates a list's elements so that the first moves to the last position, with input

    - x: list of any variable types (arr)

    Returns the list with x[0] in x[-1] position, each other element moved to front end of list one place, e.g.
    [1, 2, 3, 4] -> [2, 3, 4, 1]
    """
    xnew = [i for i in x[1:]] #New array of elements from excluding first element of input
    xnew.extend([x[0]])       #Extend new array with first element from input
    return xnew

def func(x):
    """
    Finds function string, or list of functions, found within an expression, with input

    - x: Expression possibly containing a function (str)

    Returns either single function (str) or list of functions (arr);
    If it is a list of functions, they will be ordered by occurrence within expression, e.g.
    func("tanxsinx") -> ["tan", "sin"]
    """
    functions = ["sin","cos","tan","arccos","arcsin","arctan","ln","sin^-1","cos^-1","tan^-1","csc","sec","cot"] #List of functions to search for, add any here
    f_array = [] #Empty array for functions found in expression
    for f in functions:
        loc = x.find(f) #Attempt to find each function within expression
        xtrimmed = x #Necessary to create xtrimmed to iterate through at end of while loop

        while loc != -1:
            if f == "sin^-1":
                f_array.append(["arcsin",loc]) #Correct inverse sin given by -1 power
            elif f == "cos^-1":
                f_array.append(["arccos",loc]) #Correct inverse cos given by -1 power
            elif f == "tan^-1":
                f_array.append(["arctan",loc]) #Correct inverse tan given by -1 power
            elif (loc+len(f) < len(xtrimmed)) and (xtrimmed[loc+len(f)] == "^"):
                f_array.append([xtrimmed[loc:loc+len(f)+2],loc]) #Append functions with power to f_array if present, e.g. sin^2, cos^3
            else:
                f_array.append([f,loc]) #Append found function to f_array along with its position in string
            
            
            xtrimmed = xtrimmed.replace(f,len(f)*"_",1) #xtrimmed now gets rid of all occurrences of current function so loop doesn't go infinitely
            loc = xtrimmed.find(f)

    f_array.sort(key=lambda x: x[1]) #Locs added so that array can be ordered by position in expression string here
    f_array = [i[0] for i in f_array] #Get rid of all indexes from list, leaving only functions
    
    if len(f_array) == 1:
        f_array = f_array[0] #Return only function string if only one function
    elif f_array == []:
        f_array = "" #Return empty string if no functions

    return f_array 

def separate(x):
    """
    Separates functions that are to a power within a list, e.g. separate(["sin^3x"]) -> ["sinx","sinx","sinx"]
    Works with lists that include expressions without functions, with input

    - x: List of terms in an expression, or just general list of strings (arr)

    Returns the same array with any powered function terms separated
    """
    #New array for separated terms
    xnew = []

    for i in x:
        #Append e terms in case function in e power
        if "e^" in i:
            xnew.append(i)
            continue

        f = func(i)
        if f != "":
            if pwr(f) != "1": #Case of power of function not equal to 1, e.g. sin^2(x)
                inew = i
                c = ""

                #Check for coefficient, remove
                if co(i) != "1":
                    c = co(i)
                    inew = i[len(c):]
                fn = inew[:inew.index("^")]  #Take function
                cont = inew[inew.index(pwr(f))+1:]  #Take content

                #Add power number of functions to funcs array
                funcs = []
                k = 0
                while k < int(pwr(f)): #Iterate until k reaches power of function, e.g. until 3 for cos^3(x)
                    funcs.append(fn+cont) #Append single power function to list each time
                    k += 1

                #Check for coefficient, add to first if exists
                funcs[0] = c+funcs[0]

                xnew.extend(funcs) #Add funcs to xnew
            else:
                xnew.append(i) #Case of function being to power of 1, e.g. sinx, just append as is
        else:
            xnew.append(i) #Case of no function present in string, append as is
    return xnew

def co(x):
    """
    Finds coefficient of an expression, with input

    -x: Expression containing a coefficient (str)

    Returns the (NUMERICAL ONLY) coefficient of the expression (str)
    Does not return variable coefficients, just numbers, e.g. 2x^2e^(5x) -> 2, not 2x^2
    Will return numeric inputs as themselves, e.g. co("4") -> "4"
    """
    x = brackets(x) #Remove brackets

    #Check if input is already a number using float(), return input if numeric
    try:
        x = int(x)
        x = str(x)
        return x
    except ValueError:
        pass

    #Remove negative if present so it doesn't break following logic
    if x.find("-") == 0:
        negative = True
        x = x[1:]

    f = func(x) #Find function if present
    if f != "": 
        if type(f) == str: #Single function, f is string
            cl = x.find(f)
        elif type(f) == list: #Multiple functions, f is array
            cl = x.find(f[0])
        if x[cl-1] == "(": #Account for possible opening paren before function
            x = x[:cl-1]
        x = x[:cl] #Slice to the opening of the function, leaving only what comes before it
    
    else:
        i = 0
        while i < len(x): #Iterate through each index in string
            char = x[i]   #Current char given by index slice
            if char == ".": #Skip "." in case of decimal coefficient
                i += 1
                continue
            elif char.isnumeric() == True: #Continue if character is numeric
                i += 1
            else:
                x = x[:i] #Stop when character no longer numeric, i.e. coefficient is finished
    
    #Attempt to append negative again if present before
    try:
        if negative == True:
            x = "-" + x
    except UnboundLocalError: #No negative present
        pass

    if x == "": #Case of coefficient being 1, i.e. no number at beginning of expression
        return "1"
    else:
        return x

def vari(x):
    """
    Finds the subject variable of an expression, with input

    - x: Expression containing a variable (str)

    Returns the variable letter (str) or list of variable letters (arr)
    This function has means to pass over functions, but any random letters within an expression will be treated as variables
    """
    f = func(x) #Find function in expression
    for i in ["(",")","^","-","."]:
        x = x.replace(i,"")  #Remove non-numeric chars that are not variables, i.e. not letters
    
    v = [] #Empty array to fill with variables
    for i in x:
        if i not in f: #If character not in function
            if (i not in v) and (i.isnumeric()==False):
                if i == "e": #Skip e as not variable
                    pass
                else:
                    v.append(i) #Append any letters to variables list

    if len(v) == 1:
        v = v[0] #Return string if only one var
    elif len(v) == 0:
        v = None #Case of no variables present

    return v

def pwr(x):
    """
    Finds the power of an expression, with input

    - x: Expression containing a power (str)

    Returns the power of the expression - this is not limited to variables with power, e.g. x^5
    For example, pwr("e^(5x)") -> "5x"
    Breaks down with an expression of multiple terms with powers, e.g. pwr("x^2e^(5x)") -> "2e^(5x"
    """
    #Ok I won't lie I can't remember why I included this bit, too scared to remove it
    #Most comments were written synchronously but I didn't comment this bit
    #I'm only human
    try:
        float(x)
        return ""
    except (ValueError,TypeError) as e:
        pass

    i = 0
    while i < len(x):
        char = x[i]
        if char.isnumeric() == True:
            break
        if (i == len(x) - 1) and (char.isnumeric() == False):
            return "1"
        i += 1

    c = co(x)
    v = vari(x)
    if c == None:
        c = ""
    if x.find("(") == 0:
        if x.find(")") == len(x)-1:
            x = x[len(c)+1:-1]
        else:
            x = x[len(c)+2:]
    else:
        x = x[len(c):]
    loc = x.find("^")
    if loc != -1:
        if x.find(")") == len(x)-1:
            x = x[loc+1:-1]
        else:
            x = x[loc+1:]
    else:
        if v != None:
            x = "1"
    return x

def terms(x):
    """
    Separates an expression into distinct terms, for example
    terms("xe^(x)sinx") -> ["e^x","x","sinx"] with input

    - x: Expression containing any number of distinct terms (str)

    Returns the separate constituent string terms of the expression (arr)
    Single term inputs, e.g. sinx, will simply be returned (arr)
    """
    #Check negative
    negative = x.find("-")
    if negative == 0 or negative == 1:
        x = x[:negative] + x[negative+1:]
        negative = True

    #Remove coefficient
    c = x
    while c.isnumeric() == False:
        try:
            c = str(float(c)) #Break the loop if float, isnumeric doesn't accept floats
            break
        except:
            pass
        c = co(c)
    if c != "1":
        x = x[x.index(c)+len(c):]

    #Split by exponents
    t_array = []
    loc = x.rfind("e^")
    if loc == -1:
        pass
    else:
        if x[loc+2] != "(": #Brackets not used on e power
            raise SyntaxError("Please use brackets around powers of e")
        else:
            while "e^" in x:
                current = x[loc:]
                close = current.find(")")
                e = current[:close+1]
                x = x.replace(e,"")
                t_array.append(brackets(e))
                loc = x.rfind("e^")

    #Split by logs
    loc = x.rfind("ln")
    if loc == -1:
        pass
    else:
        if x[loc+2] != "(": #Brackets not used on ln content
            raise SyntaxError("Please use brackets around the content of ln")
        else:
            while "ln" in x:
                current = x[loc:]
                close = current.find(")")
                log = current[:close+1]
                x = x.replace(log,"")
                t_array.append(brackets(log))
                loc = x.rfind("ln")

    #Remove rest of brackets
    x = brackets(x)

    #Split by function
    f = func(x)
    funcs = []
    if type(f) == list:
        for i in reversed(f): #Easier to slice when iterating backward
            loc = x.rfind(i)
            funcs.append(x[loc:])
            x = x[:loc]
        funcs.append(x) #Append rest of x when all functions accounted for
        t_array.extend(reversed(funcs)) #Keep functions in order
    else:
        t_array.append(x[:x.index(f)])
        t_array.append(x[x.index(f):])

    #Remove empty strings
    while "" in t_array:
        t_array.remove("")

    #Split by variable
    t_final = []
    for t in t_array:
        if "e^" in t or "ln" in t:
            t_final.append(t) #Append and skip e, ln terms
            continue
        while len(t) > 0: #Iterate through terms in list so far
            term = t
            count = 0 #Count of variables in expression
            index = 0
            for i in term:
                if type(func(term)) == list: #Check for function
                    f = func(term)[0] #Take first function if multiple
                else:
                    f = func(term)
                if (i in f) or (i=="^") or (i=="-") or (i.isnumeric() == True): #Skip over letters in functions, or non-letter digits
                    index += 1
                    continue
                else:
                    count += 1 #Condition that variable is found
                if count == 2:
                    term = term[:index]
                    break
                index += 1
            t_final.append(term) #Essentially splits off multiple different variables adjacent in expressions.
            t = t[len(term):]

    #NOTE: the above section causes terms such as "sinxy" to go to "sinx","y".
    #THIS PROGRAM IS NOT DESIGNED FOR PARTIAL DERIVATIVES.

    #Add coefficient to first term
    if c != "1":
        if len(t_final) == 0: #Case of terms(single number), e.g. terms("2")
            return [c]
        else:
            t_final[0] = c + t_final[0]

    #Check negative
    if negative == True:
        t_final[0] = "-" + t_final[0]

    return t_final
##############################################

### MULTIPLICATIVE ###########################
#The Multiplicative functions essentially separate the jobs by coefficient/variable/function/log/e.
#This means that the same expression list can be used in any of them to return the multiplied variables,
#or the multiplied log terms, or the multiplied coefficient, etc.
#This simplistic form allows all to be simply concatenated after the fact, leading to the function "multiply".
##############################################
def varimult(x):
    """
    Multiplies together ONLY the lone variable terms (e.g. x^3,y,g^7) 
    in a list of expressions to multiply together, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Returns the multiplied variable terms only (str)
    Note, this means the function can be used on, for example, varimult(["sinx","xcosx","x^2e^(5x)"])
    and will still work, only outputting "x^3".
    """
    #Remove brackets
    xnew = []
    for i in x:
        if "e^" in i:
            if "ln" in i:
                try:
                    p = int(i[i.index("ln") - 1]) #Case of ln power, e.g. 2lnsinx -> sin^2x
                    xnew.extend(p*[brackets(i[i.index("ln")+2:])]) #Append e^ln content without brackets
                except:
                    xnew.append(brackets(i[i.index("ln")+2:])) #Append e^ln content without brackets
                continue
            else:
                t = terms(i) #Split expressions into terms
                xnew.extend([j for j in t if "e^" not in j]) #Append new terms to xnew, excluding e^ terms
                continue
        
        elif "ln" in i and "e^" not in i: #Case of ln but not e^
            xnew.append(i)
            continue
        new = brackets(i)
        xnew.append(new)
    x = xnew 
    #This piece of code was added after the original function, making x=xnew easier than
    #running through the code to change and possibly breaking it

    #Returning variable if only one in list
    if len(x) == 1:
        if func(x[0]) != "":
            return "" #Only term has function in it, return nothing
        else:
            if pwr(x[0]) == "1":
                return vari(x[0])
            elif x[0].isnumeric() == True:  #Return nothing if just a number
                return ""
            else:
                return "{0}^{1}".format(vari(x[0]),pwr(x[0]))

    #Creating new list for only variables and powers
    variables = []
    xt = []
    for i in x:
        xt.extend(terms(i)) #List of terms left in x
    for i in xt:
        if func(i) == "": #No function present in term
            if pwr(i) == "1": #No power on variable
                variables.append(vari(i)) #Append variable alone
            else:
                variables.append("{0}^{1}".format(vari(i),pwr(i))) #Append variable with power
    variables.sort(key=lambda x: x[0]) #Sort variables by order of occurrence

    #Removing "None" variables
    if set(variables) == {"None^"}:
        return "" #All variables are "None^", return nothing
    for i in variables:
        if "None^" in i:
            variables.remove(i)

    #Return list contents if at this point only one variable
    if len(variables) == 1:
        return variables[0]

    m = "" #Final string of multiplied terms
    i = 1
    npwr = 0
    while i < len(variables):
        char = variables[i] #Current character in iteration
        prevchar =(variables[i-1]) #Character previous
        npwr += int(pwr(prevchar)) #Power of previous variable

        #If variables not the same (by this point they are ordered, so the same variables will be next to each other)
        #Append the new power of the previous variable to multiplied output string
        if vari(char) != vari(prevchar):
            m += "({0}^{1})".format(vari(prevchar),npwr)
            npwr = 0 #Reset new power to 0

        #If on the final variable in list
        if i == len(variables)-1:
            if vari(char) == vari(prevchar):
                npwr += int(pwr(char))
                
                m += "({0}^{1})".format(vari(char),npwr) #Multiply same variables together
            else:
                m += "({0})".format(char) #Add this one to list

        #If the variable is the same as the previous, the iteration automatically accounts for it        
        i += 1

    while m.find("^1)") != -1:
        m = m.replace("^1)",")") #Remove powers of 1
    while m.find("^0") != -1:
        m = m[:m.find("^0")-2] + m[m.find("^0")+3:] #Remove powers of 0
    m = m.replace(" ","")
    return m

def comult(x):
    """
    Multiplies together ONLY the coefficients
    in a list of expressions to multiply together, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Returns the multiplied coefficients only (str)
    Note, this means the function can be used on, for example, comult(["6sinx","xcosx","x^2e^(5x)"])
    and will still work, only outputting "6".
    """
    #Remove brackets
    xnew = []
    for i in x:
        new = brackets(i)
        xnew.append(new)
    x = xnew

    coeffs = [] #Empty list for coefficients
    for i in x:
        coeffs.append(co(i)) #Append coefficient of each term to list

    #Iterate through coefficients of each list looking for only number terms
    finals = []
    i = 0
    while i < len(coeffs):
        char = coeffs[i]
        try:
            float(char)
            str(char) #If character cannot be turned into float, not numeric, not coefficient
        except ValueError:
            char = co(char)
        finals.append(char)
        i += 1

    #Change "-" to "-1" if present
    while "-" in finals:
        finals.remove("-")
        finals.append("-1")

    #Iterate through coeffs to make product
    product = 1
    for i in finals:
        product *= float(i)

    #Attempt to turn float coefficients that are integers, e.g. 3.0, 5.0, to int
    product = str(product)
    intcheck = product[product.find(".")+1:]
    if int(intcheck) == 0:
        product = str(int(float(product)))
    
    if product == "1":
        return "" #Return nothing if coeff = 1
    elif product == "-1":
        return "-" #Return - if coeff = -1

    return product

def funcmult(x):
    """
    Multiplies together ONLY the function terms
    in a list of expressions to multiply together, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Returns the multiplied function terms only (str)
    Note, this means the function can be used on, for example, funcmult(["6sinx","xcosx","x^2e^(5x)"])
    and will still work, only outputting "sin(x)cos(x)".
    """
    #Remove brackets
    xnew = []
    for i in x:
        if "e^" in i:
            if "ln" in i:
                try:
                    p = int(i[i.index("ln") - 1]) #Case of ln power, e.g. 2lnsinx -> sin^2x
                    xnew.extend(p*[brackets(i[i.index("ln")+2:])]) #Append e^ln content without brackets
                except:
                    xnew.append(brackets(i[i.index("ln")+2:])) #Append e^ln content without brackets
                continue
            else:
                for j in terms(i):
                    if (func(j) != "") and ("e^" not in j):
                        xnew.append(j)
                continue

        elif "ln" in i and "e^" not in i: #Case of ln terms not e^
            xnew.append(i)
            continue
        new = brackets(i)
        xnew.append(new)
    x = xnew

    #Slice for functions only
    t = []
    for i in x:
        for j in terms(i):
            if "ln" in j: #Ignore ln as function
                continue
            t.append(j)
    t = [i for i in t if func(i) != ""]

    #Create array of lists containing [func, content]
    #Where content is what is contained in the subject of the function, e.g. x for sin(x)
    t_final = []
    for i in t:
        t_final.append([func(i),i[i.index(func(i))+len(func(i)):]])

    #Concatenation stage
    cont = list(set([i[1] for i in t_final]))
    t = []
    for i in cont:
        term = ""
        for j in t_final:
            if j[1] == i:
                if pwr(j[0]) != "1":
                    term += int(pwr(j[0]))*j[0][:-2]
                else:
                    term += j[0]
        t.append([term,i])

    #Dictionary simplifying stage
    for i in t:
        while any(j in i[0] for j in set(trigmult)) == True: #If any combinations of functions that are in dictionary to be simplified
            for k in set(trigmult):
                if k in i[0]:
                    i[0] = i[0].replace(k,trigmult[k]) #Replace combinations with simplified terms, e.g. sinxsecx -> tanx

        #Taking repeated functions to power, e.g. secsec -> sec^2
        for j in set(trigrecip):
            if i[0].count(j) > 1: #Remember, still iterating through terms list, hence i and j
                npwr = i[0].count(j)
                i[0] = i[0].replace(j,"") #Replace multiple occurrences of function with empty string
                i[0] += "{0}^{1}".format(j,npwr)

        #Separating concatenated functions
        i[0] = func(i[0])

    #Final formatting
    f = ""
    for i in t:
        if i[0] == "":
            f += ""
        elif type(i[0]) == list:
            for j in i[0]:
                f += "{0}({1})".format(j,i[1])
        else:
            f += "{0}({1})".format(i[0],i[1])

    return f

def emult(x):
    """
    Multiplies together ONLY the e^ terms
    in a list of expressions to multiply together, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Returns the multiplied e^ terms only (str)
    Note, this means the function can be used on, for example, emult(["6sinx","xcosx","x^2e^(5x)"])
    and will still work, only outputting "e^5x".
    """
    #Remove any terms without e
    x = [i for i in x if "e^" in i]

    #Remove any terms with e^ln, remove brackets
    xnew = []
    for i in x:
        if "ln" not in i:
            xnew.append(i)
    x = [brackets(i) for i in xnew]

    if len(x) == 0:
        return "" #No e^ terms, return nothing
    elif len(x) == 1:
        x = x[0][x[0].index("e^"):] #Only one e^ term
        return x

    #Grab only powers
    x = [i[i.index("e^")+2:] for i in x]

    #New power
    npwr = ""
    i = 0
    while i < len(x)-1:
        p = x[i]
        npwr += p
        if x[i+1][0] == "-": #Check negative on next term
            npwr += " - " #Subtract next term
            x[i+1] = x[i+1][1:]
        else:
            npwr += " + " #No negative, add next term
        i += 1
    npwr += x[-1]

    return "e^({0})".format(npwr)

def logmult(x):
    """
    Multiplies together ONLY the log terms
    in a list of expressions to multiply together, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Returns the multiplied log terms only (str)
    Note, this means the function can be used on, for example, emult(["6sinx","xcosx","x^2e^(5x)","ln(2x)"])
    and will still work, only outputting "ln2x".
    """
    #Remove any terms without ln, also remove e^ln
    xnew = []
    for i in x:
        if "ln" in i:
            xnew.extend(terms(i))
    for i in xnew:
        if "e^" in i or "ln" not in i:
            xnew.remove(i)

    #Slice ln terms for only ln parts of expression
    xfinal = []
    for i in xnew:
        loc = i.find("ln")
        xfinal.append(i[loc:])

    #Return concatenated terms, no special rule for log multiplication
    m = ""
    for i in xfinal:
        m += "(" + i + ")"

    return m

def multiply(x):
    """
    Uses all other multiplication functions to create one simple function 
    that can handle any terms, with input

    - x: Multiple str expressions (as complex as necessary) (arr)

    Concatenates all other multiplication methods. If they are applied to no relevant
    terms, e.g. funcmult(["e^(5x)","x^2","yln(2x")]) -> "", they always return empty strings
    meaning the concatenation doesn't fail;
    Returns the (mostly) simplified expression resulting from multiplying all terms together (str)
    """
    multiterms = []
    for i in x:
        if ("+" in i) or (" - " in i): #Case of expressions with more than one term, e.g. "sinx + cosx"
            multiterms.append(i)
            x.remove(i)

    if "0" in x:
        return "0" #If 0 multiplies anything, it's always 0!

    if len(x) == 1 and len(multiterms) == 0:
        return x[0] #Return only term if only one term

    #Use methods to multiply
    c = comult(x)
    v = varimult(x)
    f = funcmult(x)
    e = emult(x)
    l = logmult(x)

    #Concatenate for expression
    exp = "{0}{1}{2}{3}{4}".format(c,v,f,e,l)

    if exp == "":
        return "1" #Return 1 if expression completely cancels out

    else:
        if len(multiterms) != 0:
            m = ""
            for i in multiterms:
                m += "({0})".format(i) #Concatenate multiterm expressions on the end
            exp += m
        return exp
##############################################

### DIVISIVE #################################
#The Divisive functions work the same as Multiplicative, separating the jobs by coefficient/variable/function/log/e.
#The same expression list can again be used in any of them to return the divided variables.
#However, it should be noted that all functions now take to inputs, the numerator (x) and the denominator (y).
#Again, "divide" is simply a concatenation function for the most part.
##############################################
def varidiv(x,y):
    """
    Divides ONLY the lone variable terms (e.g. x^3,y,g^7) 
    from two lists of expressions to divide, with inputs

    - x: Numerator expression, e.g. "sinxcosx" (str)
    - y: Denominator expression (or divisor), e.g. "e^(x)" (str)

    Returns x/y variable terms, simplified for the most part (str);
    Again, works with any complicated expressions, e.g. varidiv("xsin^2x","e^(x)") -> "x";
    Beware a lot of time is saved with divide by using the multiply functions
    """
    #Retrieve variables only from x,y
    xt = terms(x)
    x = [i for i in xt if (func(i) == "") and ("e^" not in i) and (co(i) == "1")]
    #Remove coefficients from other terms
    x.extend([i[len(co(i)):] for i in xt if (func(i) == "") and ("e^" not in i) and (co(i) != "1")])

    #Trim for separated terms with no function and no e^ term
    yt = terms(y)
    y = [i for i in yt if (func(i) == "") and ("e^" not in i) and (co(i) == "1")]
    #Trim any other terms and append where coefficient is not 1, i.e. not ""
    y.extend([i[len(co(i)):] for i in yt if (func(i) == "") and ("e^" not in i) and (co(i) != "1")])

    #Change y powers to negative
    ydiv = []
    for i in y:
        ydiv.append("{0}^{1}".format(vari(i),"-"+pwr(i)))

    #Add divisor terms to x array and multiply (thus dividing)
    x.extend(ydiv)
    d = multiply(x)
    if d == "1":
        d = ""
    return d

def codiv(x,y):
    """
    Divides ONLY the coefficients (e.g. "7","4") 
    from two lists of expressions to divide, with inputs

    - x: Numerator expression, e.g. "4sinxcosx" (str)
    - y: Denominator expression (or divisor), e.g. "2e^(x)" (str)

    Returns x/y coefficient, simplified for the most part (str);
    Again, works with any complicated expressions, e.g. codiv("2sin^2x","4e^(x)") -> "0.5";
    Beware a lot of time is saved with divide by using the multiply functions
    """
    #Check for negatives
    neg = False
    if x[0] == "-": #Only numerator negative
        neg = True
        x = x[1:]

    if y[0] == "-" and neg == True: #Num & denom negative, thus double negative cancels
        neg = False
        y = y[1:]

    elif y[0] == "-" and neg == False: #Only denominator negative
        neg = True
        y = y[1:]

    #Take coefficients of x,y until both numbers
    cox = co(x)
    coy = co(y)
    while cox.isnumeric() == False or coy.isnumeric() == False:
        cox = co(cox) #Not numeric, take coefficient again and repeat
        coy = co(coy)

    #Divide coefficients as floats
    nco = str(float(cox)/float(coy))
    if nco == "1.0":
        nco = ""

    #Return integer if ".0" only on end of float
    if nco[nco.find(".")+1:] == "0":
        nco = nco[:nco.find(".")]

    #Round to three decimal places if float is longer
    elif len(nco[nco.find(".")+1:])>3:
        nco = "{0:0.3f}".format(float(nco))

    #Add on negative if correct
    if neg == True:
        nco = "-" + nco

    return nco

def funcdiv(x,y):
    """
    Divides ONLY the functions (e.g. "sinxcosx","tanx") 
    from two lists of expressions to divide, with inputs

    - x: Numerator expression, e.g. "4sinxcosx" (str)
    - y: Denominator expression (or divisor), e.g. "2tanx" (str)

    Returns x/y function terms, simplified for the most part (str);
    Again, works with any complicated expressions, e.g. codiv("2sin^2x","4cosx") -> "sin(x)tan(x)";
    This function works simply by concatenating reciprocated y functions to x functions and simplifying using dict
    """
    #Retrieve function terms only from x,y
    xt = separate(terms(x))
    x = [i for i in xt if (func(i) != "") and ("e^" not in i) and (co(i) == "1")]
    #Remove coefficients from other terms
    x.extend([i[len(co(i)):] for i in xt if (func(i) != "") and ("e^" not in i) and (co(i) != "1")])

    #Trim for separated terms with function and no e^ term
    yt = separate(terms(y))
    y = [i for i in yt if (func(i) != "") and ("e^" not in i) and (co(i) == "1")]
    #Trim any other terms and append where coefficient is not 1, i.e. not ""
    y.extend([i[len(co(i)):] for i in yt if (func(i) != "") and ("e^" not in i) and (co(i) != "1")])

    #Reciprocate functions for y using trigrecip dict
    ydiv = []
    for i in y:
        cont = i[len(func(i)):]
        ydiv.append("{0}{1}".format(trigrecip[func(i)],cont))
    
    #Add divisor terms to x array and multiply (thus dividing)
    x.extend(ydiv)
    d = multiply(x)
    if d == "1":
        d = ""
    return d

def ediv(x,y):
    """
    Divides ONLY the e^ terms (e.g. "e^(x)","4e^(2x)") 
    from two lists of expressions to divide, with inputs

    - x: Numerator expression, e.g. "4e^(2x)cosx" (str)
    - y: Denominator expression (or divisor), e.g. "e^(ln(x))" (str)

    Returns x/y e^ terms, simplified for the most part (str);
    Again, works with any complicated expressions, e.g. codiv("2sinxe^(2x)","e^(2y)") -> "e^(2x-2y)";
    This function hasn't really been ironed out much and the output isn't always simplified, but it isn't used often;
    Note this is also capable of taking care of e^ln terms, which is why it is so long
    """
    #Remove any negatives
    if x[0] == "-":
        x = x[1:]
    if y[0] == "-":
        y = y[1:]

    #Remove coefficients
    c = x
    while c.isnumeric() == False:
        try:
            c = str(float(c)) #Break the loop if float, isnumeric doesn't accept floats
            break
        except:
            pass
        c = co(c)
    if c != "1":
        x = x[x.index(c)+len(c):]

    c = y
    while c.isnumeric() == False:
        try:
            c = str(float(c))
            break
        except:
            pass
        c = co(c)
    if c != "1":
        y = y[y.index(c)+len(c):]

    #Retrieve e terms only from x,y
    xt = terms(x)
    x = [i for i in xt if ("e^" in i) and ("ln" not in i)]

    yt = terms(y)
    y = [i for i in yt if ("e^" in i) and ("ln" not in i)]

    #Bracket x powers
    xdiv = []
    for i in x:
        xdiv.append("e^{0}".format("("+pwr(i)+")"))

    #Append e^ln terms if present
    logs = [i for i in xt if ("e^" in i) and ("ln" in i)]
    logsdiv = [i for i in yt if ("e^" in i and "ln" in i)]

    #Massive cheat, but multiplying e^ln cases by 1 sorts out the e^ln
    logsdnew = []
    for i in logsdiv:
        term = i[:i.index("^")] + "^(" + i[i.index("^")+1:] + ")" #Add brackets to power
        term = multiply(["1",term])
        logsdnew.append(term)

    #Then, funcdiv with numerator as 1 flips the fraction. I'm embarrassed but it's such an easy way
    logsdfinal = []
    for i in logsdnew:
        term = codiv("1",i) + varidiv("1",i) + funcdiv("1",i)
        logsdfinal.append(term)

    #Change y powers to negative
    ydiv = []
    for i in y:
        ydiv.append("e^{0}".format("(-"+pwr(i)+")"))

    #Add divisor terms to x array and multiply (thus dividing)
    xdiv.extend(ydiv)
    xdiv.extend(logs)        #Numerator e^ln terms
    xdiv.extend(logsdfinal)  #Denominator e^ln terms
    d = multiply(xdiv)
    if d == "1":
        d = ""
    return d

def divide(x,y):
    """
    Uses all other division functions to create one simple function 
    that can handle any terms, with inputs

    - x: Numerator expression, e.g. "4e^(2x)cosx" (str)
    - y: Denominator expression (or divisor), e.g. "e^(ln(x))" (str)

    Concatenates all other division methods. If they are applied to no relevant
    terms, e.g. funcdiv("e^(5x)","x^2") -> "", they always return empty strings meaning the concatenation doesn't fail;
    Returns the (mostly) simplified expression resulting from dividing x/y (str)
    """
    #Return fraction if multiple terms on top/bottom
    if (" + " in x == True) or (" - " in x == True) or (" + " in y == True) or (" - " in y == True):
        return "({0})/({1})".format(x,y)

    #All methods of division
    c = codiv(x,y)
    v = varidiv(x,y)
    f = funcdiv(x,y)
    e = ediv(x,y)

    #Return concatenation
    return "{0}{1}{2}{3}".format(c,v,f,e)
##############################################

### DIFFERENTIATION ##########################
#The Differentiation functions again work similarly as they separate the jobs by coefficient/variable/function/log/e.
#The issue is that it is not as simple as concatenation after the fact, meaning they basically comprise of simple methods
#followed by loads of checks to see which method should be used at each point.
#"diff" is all-encompassing; the idea of this script is that the user can easily use "divide", "multiply" and "diff" and
#not worry about the computation underneath.
##############################################
def varidiff(x):
    """
    Diffentiates any given lone variable term, e.g. x^2,y^7,etc.
    The function does not work in the same way as multiplication and division and
    will only return a result if the correct expression is entered, for example
    varidiff("sinx") -> ""; input

    - x: Lone variable expression, e.g. "x" (str)

    Returns a differentiated expression by the rule f'(v) = (pwr)(variable)^(pwr-1) (str)
    Returns "" for any incorrect expressions input
    """
    #Return empty string if e^, ln present or it is a number
    if "e^" in x or "ln" in x:
        return ""
    try:
        int(x)
        return ""
    except ValueError:
        pass

    #Take terms with no function
    t = terms(x)
    t = [i for i in t if func(i) == ""]

    dt = []
    for i in t:
        #Take power, coefficient, variable of each term
        p = pwr(i)
        c = co(i)
        if c == "-":
            c = "-1"
        v = vari(i)

        #If power is 1, differentiation returns just coefficient
        if p == "1":
            return c

        #Apply diff rules
        newco = int(c)*int(p) #Bring power down and multiply by coeff
        npwr = int(p) - 1 #Calc new power

        #Correct syntax
        if newco == -1:
            newco = "-"
        elif newco == 1:
            newco = ""

        if npwr == 1:
            d = "{0}{1}".format(newco,v) #Case of new power = 1
        else:
            d = "{0}{1}^{2}".format(newco,v,npwr) #Other cases

        dt.append(d) #Append to list of differentiated variables

    return ("{0}{1}".format(comult(dt),varimult(dt)))

def funcdiff(x):
    """
    Diffentiates any given function term, e.g. sinx,cos^2x,etc.
    The function will only return a result if the correct expression is entered, for example
    funcdiff("e^(x)") -> ""; input

    - x: Function expression, e.g. "secx" (str)

    Returns a differentiated expression by the rule e.g. dcos(f(x))/dx = -f'(x)sin(f(x))
    Returns "" for any incorrect expressions input
    """
    #Return empty string if e^, ln present
    if "e^" in x or "ln" in x:
        return ""

    #Take coefficient and find function
    c = co(x)
    if c == "-":
        c = "-1"
    f = func(x)
    if f == "":
        return "" #No function, return empty string
    
    cont = x[x.index(f)+len(f):] #"cont" is subject of function, e.g. x^2 for sin(x^2)
    nco = multiply([c,varidiff(cont)]) #New coefficient
    if nco == "-":
        nco = "-1"

    #Case where the differentiated function returns multiple functions, e.g. dsecx -> secxtanx
    if type(trigdiff[f]) == tuple:
        newf = trigdiff[f][0]+cont+trigdiff[f][1]+cont
    else:
        newf = trigdiff[f]+cont #Case where trigdiff dict returns single function

    #Multiply differentiated expression by new coefficient
    dx = multiply([nco,newf])
    return dx

def vfprod(x):
    """
    Essentially a product differentiation mechanism capable of differentiating
    functions and variables ONLY, e.g. vfprod(["x",sinx"]) -> "sin(x) + xcos(x)";
    Note from the above the separate terms must be input as a list, input

    - x: Terms of function expression, e.g. ["x","cosx"] (arr)

    Returns a differentiated expression by the rule dx = f'(x)g(x) + f(x)g'(x)
    """
    #Create variable for differentiated material
    dx = ""
    i = 0
    while i < len(x):

        #Differentiate the first item, concatenate the rest
        di = []
        di.append(funcdiff(x[0]) + varidiff(x[0]))
        for j in x[1:]:
            di.append(j)
        di = multiply(di)

        dx += di
        dx += " + " #Add terms to final diff string

        x = rotate(x)  #Rotate the list for the next term
        i += 1  #Counter allows loop to continue over all terms in list

    dx = dx[:-3] #Remove final " + "
    dx = dx.replace("+ -","- ")
    return dx

def ediff(x):
    """
    Diffentiates any given e^ term, e.g. e^(2x),4e^(-7y),etc.
    The function does not work in the same way as multiplication and division and
    will only return a result if the correct expression is entered, for example
    ediff("sinx") -> ""; input

    - x: e^ expression, e.g. "e^(x)" (str)

    Returns a differentiated expression by the rule de^f(x) = f'(x)e^f(x)
    Note that this function can handle e^ln terms
    """
    #Return empty string if e not present
    if "e^" not in x:
        return ""

    #Take coefficient
    c = co(x)
    if c == "-":
        c = "-1"
    elif c == "e^":
        c = "1"
    else:
        while c.isnumeric() == False:
            c = co(c)

    #Take power
    p = x[x.index("e^")+2:]
    p = brackets(p)
    if vari(p) == None:
        return ""

    #Check for case of power being ln
    if "ln" in p:
        loc = p.index("ln")
        cont = p[loc+2:] #Grab content of ln
        if loc != 0:
            pco = brackets(p[:loc]) #Grab coefficient if not 1

        #Case of function
        if func(p[loc+2:]) != "":
            function = True
            floc = p.index(func(p[loc+2:])) #If ln(func) grab loc of func
            try:
                if function == True:
                    x = p[loc+2:floc+3] + "^" + pco + p[floc+3:] #Power to function, not variable, i.e. sin^2x instead of sinx^2
            except:
                x = p[loc+2:]

        #Case of variable
        else:
            cp = pwr(cont)
            cc = co(cont)
            try:
                newp = str(int(cp)*int(pco))
                if newp != "1":
                    if cc == "1":
                        x = vari(cont) + "^" + newp #Expression now variable with correct power, no num coefficient
                    else:
                        x = cc + vari(cont) + "^" + newp #Variable with corrent power and coefficient
                else:
                    if cc == "1":
                        x = vari(cont) #If power & coefficient are 1
                    else:
                        x = cc + vari(cont)
            except:
                x = cont

    #Case where e^ln, differentiate new x
    if "e^" not in x:
        f = func(x)
        if f != "":
            x = separate(terms(x))
            if len(x) == 1:
                x = x[0]
            if type(x) == list:  #Product diff for each element in list of terms
                dx = vfprod(x)
            else:
                dx = funcdiff(x)
            if c != "1" and c != "":
                dx = multiply([c,dx])
        else:
            dx = multiply([c,varidiff(x)])
        return dx

    #If e^ still present, diff according to f'(x)e^f(x)
    else:
        if func(p) != "":
            sep = separate(terms(p))
            if len(sep) == 1:
                p = sep[0]
            if type(sep) == list:
                dp = vfprod(sep)
            else:
                dp = funcdiff(p)
        else:
            dp = varidiff(p)

    #Multiply by coefficient
    if "+" not in dp and " - " not in dp:
        dp = multiply([dp,c]) #multiply function can't handle multiple separate terms
    else:
        if c == "1":
            pass
        else:
            dp = c + ")(" + dp #No need to bracket as this is achieved in last line

    if dp == "-1" or dp == "-":
        dp = "-"
    elif dp == "1":
        dp = ""
    else:
        dp = "(" + dp + ")"
    
    return "{0}e^({1})".format(dp,p)

def logdiff(x):
    """
    Diffentiates any given log term, e.g. ln(secx),2ln(x^2),etc.
    The function does not work in the same way as multiplication and division and
    will only return a result if the correct expression is entered, for example
    logdiff("x^2") -> ""; input

    - x: Log expression, e.g. "ln(x)" (str)

    Returns a differentiated expression by the rule dln(f(x)) = f'(x)/f(x)
    """
    #Check for negative
    negative = False
    if x.find("-") == 0:
        negative = True

    #Take coefficient
    c = co(x)
    if c == "-":
        c = "-1"
    else:
        while c.isnumeric() == False:
            c = co(c)

    #Return nothing if e present, or if ln not present
    if ("e^" in x) or ("ln" not in func(x)):
        return ""

    #Get content of ln
    try:
        cont = x[x.index("(")+1:x.rfind(")")]
    except:
        raise SyntaxError("Please use brackets around the content of ln")

    #Take terms, product diff content
    t = separate(terms(cont))
    dt = vfprod(t)
    if negative == True:
        dt = "-" + dt

    #dln(f(x)) = f'(x)/f(x)
    dx = divide(dt,cont)
    dx = multiply([c,dx])

    return dx

def diff(x):
    """
    The culmination of all the work!
    Diffentiates any term. Can be entered in any fashion, e.g. "xsinx", "e^(ln(sinx))", etc.
    Remember always to surround powers of e and content of ln with (brackets), input

    - x: Differentiable expression, e.g. "x^2e^(ln(sinx))" (str)

    Returns a the first derivative of the expression
    Currently NOT able to handle multiterm expressions, e.g. sinx + cosx
    """
    #Check for negative
    if x.find("-") == 0:
        x = x[1:]
        negative = True

    t = terms(x)
    t = separate(t)  #Separate functions to powers e.g. sin^2x -> sinx, sinx

    #Add brackets around ln powers if missing to diff correctly
    for i in t:
        if "ln" in i:
            cont = i[i.index("ln")+2:]
            inew = i[:i.index("ln")+2] + "(" + cont + ")"
            t[t.index(i)] = inew #Replace string in terms

    try:
        if negative == True:
            t[0] = "-" + t[0]
    except UnboundLocalError:
        pass

    dt = ""
    i = 0
    while i < len(t):
        #Differentiate first expression in all ways, append rest of exps to form first product term
        di = [funcdiff(t[0]) + varidiff(t[0]) + logdiff(t[0]) + ediff(t[0])] #Add new diff functions here
        di.extend(t[1:])
        #Add brackets around e powers if missing to multiply correctly
        for j in di:
            if "e^" in j:
                if j[j.index("e^")+2] != "(":
                    cont = j[j.index("e^")+2:]
                    jnew = j[:j.index("e^")+2] + "(" + cont + ")"
                    di[di.index(j)] = jnew #Replace string in di terms
        if len(di) > 1:
            di = multiply(di)
        else:
            di = di[0]
        t = rotate(t)
        if dt == "":
            dt += di
        else:
            if di.find("-") == 0:
                dt += " - {0}".format(di[1:])
            else:
                dt += " + {0}".format(di)
        i += 1
    if dt.find(")") == len(dt)-1 and dt.find("(") == 0:
        return dt[1:-1]
    else:
        return dt
##############################################

### TESTING ##################################
res = []

thelist = ["1","x","2x","x^2","2x^2","10x^2","10x^10","x^-2","sinx","cosx","tanx","cscx","secx","cotx",
"2sinx","2cosx","2tanx","2cscx","2secx","2cotx","sin2x","2sin2x","cos2x","2cos2x","tan2x","2tan2x","csc2x",
"2csc2x","sec2x","2sec2x","cot2x","2cot2x","sinx^2","cosx^2","tanx^2","cscx^2","secx^2","cotx^2","2sinx^2",
"2cosx^2","2tanx^2","2cscx^2","2secx^2","2cotx^2","2xsin2x","2xcos2x","2xtan2x","2xcsc2x","2xsec2x","2xcot2x",
"xsinx","xcosx","xtanx","xcscx","xsecx","xcotx","x^2sinx","x^2cosx","x^2tanx","x^2cscx","x^2secx","x^2cotx",
"sin^2x","cos^2x","tan^2x","csc^2x","sec^2x","cot^2x","sinxcosx","sinxtanx","sinxcscx","sinxsecx","sinxcotx",
"e^(x)","e^(2x)","e^(x^2)","e^(2x^2)","2e^(x)","2e^(2x)","2e^(x^2)","2e^(2x^2)","e^(lnx)","e^(0)","e^(5)",
"e^(lnx^2)","e^(2lnx)","e^(ln2x)","e^(2ln2x)","e^(2lnx^2)","e^(ln2x)","e^(sinx)","e^(cosx)","e^(tanx)",
"e^(cscx)","e^(secx)","e^(cotx)","2e^(lnx)","2e^(2lnx)","2e^(ln2x)","2e^(2ln2x)","2e^(lnx^2)","2e^(2lnx^2)",
"e^(lnsinx)","e^(lncosx)","e^(lntanx)","e^(lncscx)","e^(lnsecx)","e^(lncotx)","2e^(lnsinx)","2e^(lncosx)",
"2e^(lntanx)","2e^(lncscx)","2e^(lnsecx)","2e^(lncotx)","2e^(2lnsinx)","2e^(2lncosx)","2e^(2lntanx)","2e^(lncscx)",
"2e^(2lnsecx)","2e^(2lncotx)","e^(2sinx)","e^(2cosx)","e^(2tanx)","e^(2cscx)","e^(2secx)","e^(2cotx)","2e^(sinx)",
"2e^(cosx)","2e^(tanx)","2e^(cscx)","2e^(secx)","2e^(cotx)","xe^(x)","x^2e^(x)","2xe^(x)","xe^(x^2)","2xe^(sinx)",
"2xe^(cosx)","2xe^(tanx)","2xe^(cscx)","2xe^(secx)","2xe^(cotx)","e^(sin^2x)","e^(cos^2x)","e^(tan^2x)",
"e^(csc^2x)","e^(sec^2x)","e^(cot^2x)","x^2e^(sin^2x)","x^2e^(cos^2x)","x^2e^(tan^2x)","x^2e^(csc^2x)",
"x^2e^(sec^2x)","x^2e^(cot^2x)","2x^2e^(sin^2x)","2x^2e^(cos^2x)","2x^2e^(tan^2x)","2x^2e^(csc^2x)","2x^2e^(sec^2x)",
"2x^2e^(cot^2x)","e^(lnsin^2x)","e^(lncos^2x)","e^(lntan^2x)","e^(lncsc^2x)","e^(lnsec^2x)","e^(lncot^2x)",
"2e^(lnsin^2x)","2e^(lncos^2x)","2e^(lntan^2x)","2e^(lncsc^2x)","2e^(lnsec^2x)","2e^(lncot^2x)","ln(x)","ln(2x)",
"ln(x^2)","ln(2x^2)","2ln(x)","2ln(2x)","2ln(x^2)","2ln(2x^2)","xln(x)","xln(2x)","xln(x^2)","xln(2x^2)","2xln(x)",
"2xln(2x)","2xln(x^2)","2xln(2x^2)","x^2ln(x)","x^2ln(2x)","x^2ln(x^2)","x^2ln(2x^2)","2x^2ln(x)","2x^2ln(2x)",
"2x^2ln(x^2)","2x^2ln(2x^2)","ln(sinx)","ln(cosx)","ln(tanx)","ln(cscx)","ln(secx)","ln(cotx)","2ln(sinx)",
"2ln(cosx)","2ln(tanx)","2ln(cscx)","2ln(secx)","2ln(cotx)"]

for i in thelist:
    try:
        res.append("{0} -> {1}".format(i,diff(i)))
    except:
        res.append("Error for: {0}".format(i))

for i in res:
    print(i)
##############################################