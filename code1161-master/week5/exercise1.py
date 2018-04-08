# -*- coding: UTF-8 -*-
"""Refactoring.

This exercise contains a complete and working example, but it's very poorly written.

Your job is to go through it and make it as good as you can.

That means making it self-documenting wherever possible, adding comments where
it isn't. Take repeated code and make it into a function. Also use functions
to encapsulate concepts. If something is done many times, maybe a map or a loop
is called for. Etc.

Some functions will have directions as external comments, once you think you
are on top of it, take these comments out. Others won't have comments and
you'll need to figure out for yourself what to do.
"""
import math

# This is a terrible function. The rest of the functions in this file do a
# much better job of what it's trying to do. Once you've has a little look,
# move on, and eventually delete this function. (And this comment!)
def do_bunch_of_bad_things():
    print(countdown("Getting ready to start in",9,1,"Let's go!"))
    base = 3
    height =4
    print("area = " + str(calculate_area(base,height)))
    print("hypotenuse: {}".format( calculate_hypotenuse(base,height)))

    another_hyp = calculate_hypotenuse(5,6)
    print(another_hyp)

    yet_another_hyp = calculate_hypotenuse(40,30)
    print(yet_another_hyp)


# return a list of countdown messages, much like in the bad function above.
# It should say something different in the last message.
def countdown(message, start, stop, completion_message):
    ss = start
    ee = stop
    returnList = []
    if (start>stop):
        ss=stop
        ee=start
    for x in range(ss,ee+1):
        returnList.append(message+" "+str(x))
    print(completion_message)
    return  returnList



# TRIANGLES

# This should be a series of functions that are ultimatly used by
# triangle_master
# It should eventually return a dictionary of triangle facts. It should
# optionally print information as a nicely formatted string. Make printing
# turned off by default but turned on with an optional argument.
# The stub functions are made for you, and each one is tested, so this should
# hand hold quite nicely.
def calculate_hypotenuse(base, height):
    return math.sqrt(base**2+height**2)


def calculate_area(base, height):
    return (base*height)/2


def calculate_perimeter(base, height):
    return(base+height+calculate_hypotenuse(base,height))


def calculate_aspect(base, height):
    if (base < height ):
        return "tall"
    elif(base==height):
        return "equal"
    else:
        return "wide"


# Make sure you reuse the functions you've already got
# Don't reinvent the wheel
def get_triangle_facts(base, height, units="mm"):
    return {"area": calculate_area(base,height),
            "perimeter": calculate_perimeter(base,height),
            "height": height,
            "base": base,
            "hypotenuse": calculate_hypotenuse(base,height),
            "aspect": calculate_aspect(base,height),
            "units": units}


# this should return a multi line string that looks a bit like this:
#
# 15
# |
# |     |\
# |____>| \  17.0
#       |  \
#       |   \
#       ------
#       8
# This triangle is 60.0mm²
# It has a perimeter of 40.0mm
# This is a tall triangle.
#
# but with the values and shape that relate to the specific
# triangle we care about.
def tell_me_about_this_right_triangle(facts_dictionary):
    tall = """
            {height}
            |
            |     |\\
            |____>| \\  {hypotenuse}
                  |  \\
                  |   \\
                  ------
                  {base}"""
    wide = """
            {hypotenuse}
             ↓         ∕ |
                   ∕     | <-{height}
               ∕         |
            ∕------------|
              {base}"""
    equal = """
            {height}
            |
            |     |⋱
            |____>|  ⋱ <-{hypotenuse}
                  |____⋱
                  {base}"""

    pattern = ("This triangle is {area}{units}²\n"
               "It has a perimeter of {perimeter}{units}\n"
               "This is a {aspect} triangle.\n")

    facts = pattern.format(**facts_dictionary)
    print(facts)
    a = facts_dictionary["aspect"]
    if(a=="tall"):
        return tall.format(**facts_dictionary)
    elif(a=="wide"):
        return wide.format(**facts_dictionary)
    else:
        return equal.format(**facts_dictionary)

def triangle_master(base,
                    height,
                    return_diagram=False,
                    return_dictionary=False):
    d = get_triangle_facts( base, height, "mm" )
    diagram = tell_me_about_this_right_triangle( d )
    if return_diagram and return_dictionary:
        d["diagram"]=diagram
        return d
    elif return_diagram:
        return diagram
    elif return_dictionary:
        dict = {"facts":{"units":d["units"],"base":d["base"]}}
        return dict
    else:
        print("You're an odd one, you don't want anything!")


def wordy_pyramid():
    pyramid_list = []
    pyramid_list = list_of_words_with_lengths(range(3, 21, 2))

    pyramid_list += list_of_words_with_lengths(range(20,3,-2))
    return pyramid_list


def get_a_word_of_length_n(length):

    try:
        int(length)
    except:
        return None


    if(length<=0):
        return None
    import requests
    baseURL = "http://api.wordnik.com/v4/words.json/randomWords?api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5&minLength={0}&maxLength={0}&limit=1"
    url = baseURL.format( length )
    r = requests.get( url )
    message = r.json()[0]['word']
    return message



def list_of_words_with_lengths(list_of_lengths):
    returnList = []
    for x in list_of_lengths :
        returnList.append(get_a_word_of_length_n(x))
    return returnList



if __name__ == "__main__":
    #do_bunch_of_bad_things()
    facts = get_triangle_facts(3,4)
    dict1 = {"facts":{}}
    dict1["facts"].update(facts)
    print(dict1)

    dict1["diagram"] = tell_me_about_this_right_triangle(facts)
    print(dict1)