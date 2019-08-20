import requests
from bs4 import BeautifulSoup as bs

# This function gets the name of the department from the beginning of the class' name ("MATH" from "MATH 6B").
# It's used for when a series of courses is listed like "I&C SCI 31-32-33". This is because the findCourses function will add to the list "I&C SCI 31", "32", and "33" (the latter two lack the department).
def getPrefix(className):
    # During my debugging, I found that the ascii value for the spaces on the UCI page is 160, so I'm including the value for a regular space and for the weird UCI space.
    while className[-1] != ' ' and ord(className[-1]) != 160:
        className = className[:-1]
    return className[:-1]

# This function performs the searching for courses given a url for a major/minor/ge.
def findCourses(url, attrs, numTables):
    # The soup object takes the block of dense html in page and makes it easier to parse.
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    # The classes array stores the link objects. The classes_names array stores the class names.
    classes_obj = []
    classes_names = []

    # Loop through each table of classes.
    for i in range(numTables):
        # Loop through each link object in each table and add it to the array.
        tables = soup.find_all("table")[i]
        tableBodies = tables
        aObjs = tableBodies.find_all("a")
        for a in aObjs:
            classes_obj.append(a)

    # This loop adds all of the classes to the classes_names array, adding a prefix if it wasn't already present.
    for i in range(len(classes_obj)):
        # The if is checking to see if there exists a prefix on the class yet. All of the classes without prefixes begin with a space because of the webpage's formatting.
        if classes_obj[i].text[0] == ' ':
            classes_names.append(getPrefix(classes_names[i-1]) + classes_obj[i].text)
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
    csUrl = "http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext"
    csCourses = findCourses(csUrl, {"class" : "sc_courselist"}, 1)

    geUrl = "http://catalogue.uci.edu/informationforadmittedstudents/requirementsforabachelorsdegree/"
    geCourses = findCourses(geUrl, {}, 9)

    shared = findShared(csCourses, geCourses)
    for a in shared:
        print(a)

    # clean up findCourses loop
    # ICS 32 didn't show as common