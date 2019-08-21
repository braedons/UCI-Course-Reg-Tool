import requests
from bs4 import BeautifulSoup as bs

majorsDict = {
    "cs": ("http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext", 1),
    "ge": ("http://catalogue.uci.edu/informationforadmittedstudents/requirementsforabachelorsdegree/", 9),
    "gs_minor": ("http://catalogue.uci.edu/interdisciplinarystudies/globalsustainability/", 1)
}

# This function gets the name of the department from the beginning of the class' name ("MATH" from "MATH 6B").
# It's used for when a series of courses is listed like "I&C SCI 31-32-33". This is because the findCourses function will add to the list "I&C SCI 31", "32", and "33" (the latter two lack the department).
def getPrefix(className):
    # During my debugging, I found that the ascii value for the spaces on the UCI page is 160, so I'm including the value for a regular space and for the weird UCI space.
    while className[-1] != ' ' and ord(className[-1]) != 160:
        className = className[:-1]
    return className[:-1]

# This function performs the searching for courses given a url for a major/minor/ge.
def findCourses(tup):
    url = tup[0]
    numTables = tup[1]

    # The soup object takes the block of dense html in page and makes it easier to parse.
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    # The classes array stores the link objects. The classes_names array stores the class names.
    classes_obj = []
    classes_names = []

    # Loop through each table of classes.
    for i in range(numTables):
        # Loop through each link object in each table and add it to the array.
        aObjs = soup.find_all("table")[i].find_all("a")
        for a in aObjs:
            classes_obj.append(a)

    # This loop adds all of the classes to the classes_names array, adding a prefix if it wasn't already present.
    for i in range(len(classes_obj)):
        # The if is checking to see if there exists a prefix on the class yet. All of the classes without prefixes begin with a space because of the webpage's formatting.
        if classes_obj[i].text[0] == ' ':
            # The classes without prefixes already begin with a space, but it has a different ascii value than the spaces on the site, so I'm swapping them out here.
            classes_names.append(getPrefix(classes_names[i-1]) + chr(160) + classes_obj[i].text[1:])
        else:
            classes_names.append(classes_obj[i].text)
    
    return classes_names

# This function returns the classes in common between two arrays of classes.
def findShared(a, b):
    # Using sets allows for a quick comparison that ignores duplicates.
    a_set = set(a) 
    b_set = set(b) 
      
    if len(a_set.intersection(b_set)) > 0: 
        return a_set.intersection(b_set)
    else:
        return "no common elements"


if __name__ == "__main__":
    m1Courses = findCourses(majorsDict["ge"])
    m2Courses = findCourses(majorsDict["gs_minor"])

    shared = findShared(m1Courses, m2Courses)
    if (type(shared) == str):
        print(shared)
    else:
        for a in shared:
            print(a)