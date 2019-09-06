import requests
from bs4 import BeautifulSoup as bs

majorsDict = {
    "cs": ("http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext", 1, 0),
    "ge": ("http://catalogue.uci.edu/informationforadmittedstudents/requirementsforabachelorsdegree/", 9, 0),
    "gs_minor": ("http://catalogue.uci.edu/interdisciplinarystudies/globalsustainability/", 1, 0)
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
    startTable = tup[2] # Starts at 0

    # The soup object takes the block of dense html in page and makes it easier to parse.
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    # The classes array stores the link objects. The classes_names array stores the class names.
    classes_obj = []
    classes_names = []

    # Loop through each table of classes.
    for i in range(startTable, startTable + numTables):
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

def translateToGeCategory(nums):
    categoryTitles = {
        '0': ("Ib", "Upper-Division Writing", 1),
        '1': ("II", "Science and Technology", 3),
        '2': ("III", "Social and Behavioral Sciences", 3),
        '3': ("IV", "Arts and Humanities", 3),
        '4': ("Va", "Quantitative Literacy", 1),
        '5': ("Vb", "Formal Reasoning", 1),
        '6': ("VI", "Language Other Than English", 1),
        '7': ("VII", "Multicultural Studies", 1),
        '8': ("VIII", "International/Global Issues", 1),
    }
    out = []
    
    for n in nums:
        out.append(categoryTitles[str(n)][0])
    
    return out

def findGeDupes():
    coursesGeCatDict = {a: [] for a in findCourses(majorsDict["ge"])}
    
    for i in range(majorsDict["ge"][1]):
        for course in findCourses((majorsDict["ge"][0], 1, i)):
            coursesGeCatDict[course].append(i)

    for key, val in coursesGeCatDict.items():
        if (len(val) > 1) and (3 in val and 7 in val):#any(item in val for item in [4, 5, 7, 8]):
            print(key + ":", translateToGeCategory(val))

def full_lookup(course_a_str, course_b_str):
    m1Courses = findCourses(majorsDict[course_a_str])
    m2Courses = findCourses(majorsDict[course_b_str])

    shared = findShared(m1Courses, m2Courses)
    if (type(shared) == str):
        print(shared)
    else:
        for a in shared:
            print(a)

    return shared