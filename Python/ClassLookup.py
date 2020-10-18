import requests
from bs4 import BeautifulSoup as bs
import csv


# (URL, number of tables, starting table)
# The starting table will usually be 0, but it might be higher depending on the webpage
majors_dict = {
    "cs": ("http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext", 1, 0),
    "GE": ("http://catalogue.uci.edu/informationforadmittedstudents/requirementsforabachelorsdegree/", "GE"),
    "gs_minor": ("http://catalogue.uci.edu/interdisciplinarystudies/globalsustainability/", 1, 0)
}

def match_areas(study_areas, titles):
    output = []

    for url in study_areas:
        for area in study_areas[url]:
            split = area.split(", ", 1)
            
            for title in titles[url]:
                if len(split) == 1:
                    if title.find(split[0]) != -1:
                        output.append((title, url, area))
                        study_areas[url].remove(area)
                        titles[url].remove(title)
                        break
                elif title.find(split[0]) != -1 and title.find(split[1]) != -1:
                    output.append((title, url, area))
                    study_areas[url].remove(area)
                    titles[url].remove(title)
                    break
        
        for title in titles[url]:
            output.append((title, url, title))

    return output

# This function goes through all of the URLs and gets the title for the table of courses.
def write_studyarea_csv(study_area_links):
    study_areas = {url: [] for url in study_area_links}
    
    # Go to each link in the list and find all of the study areas on that page
    for link in study_area_links:
        page = requests.get(link)
        soup = bs(page.text, "html.parser")

        headers = soup.find_all("h4")
        for header in headers:
            if header.text.find("Requirements for the") != -1:
                study_areas[link].append(header.text)

    # (title, url, study area)
    study_areas_matched = match_areas(study_area_links, study_areas)
    
    # Write to the csv (title, url)
    with open("studyarea_url_info.csv", mode='w') as file:
        writer = csv.writer(file, lineterminator = '\n')

        writer.writerow(["GE", "http://catalogue.uci.edu/informationforadmittedstudents/requirementsforabachelorsdegree/", "GE"])

        for area in study_areas_matched:
            writer.writerow(area)

# Reads the csv and returns the list of tuples as (title, url, area)
def read_studyarea_csv():
    study_areas = []

    with open('studyarea_url_info.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            # find_courses() wants the study area as a tuple, not a list
            study_areas.append(tuple(row))
    
    # {area : (url, title)}
    new_majors_dict = {tup[2] : (tup[1], tup[0]) for tup in study_areas}
    majors_dict = new_majors_dict

    return new_majors_dict

# This function searches the website containing all of the majors/minors and the links to their corresponding web pages.
def find_study_area_urls():
    # Prefix is separated here because it's referenced later since the study area URLs are all relative links.
    prefix = "http://catalogue.uci.edu"
    suffix = '/informationforprospectivestudents/'\
        'undergraduatandgraduatedegrees/#undergraduatemajorsandminorstext'
    page = requests.get(prefix + suffix)
    soup = bs(page.text, "html.parser")

    # All of the majors/minors are in an unordered list in a div
    div = soup.find("div", {"id": "undergraduatemajorsandminorstextcontainer"})
    departments = div.find("ul").find_all("a", href=True)

    # It's a dict storing the links because there are several duplicates. This prevents redundant requests.
    # The keys are the URLs, the values are the study areas. This allows for matching with the headers on each web page later.
    study_areas_links = {}

    for department in departments:
        # The [1:] gets rid of the '#' in front of the id name
        major_ul = soup.find("a", {"id": department["href"][1:]}).parent.find_next_sibling("ul")
        major_a_tags = major_ul.find_all("a", href=True)
        for major in major_a_tags:
            key = prefix + major["href"]

            if key in study_areas_links:
                study_areas_links[key].append(major.text)
            else:
                study_areas_links[key] = [major.text]

        minor_a_tags = major_ul.find_next_sibling("ul").find_all('a', href=True)
        for minor in minor_a_tags:
            key = prefix + minor["href"]

            if key in study_areas_links:
                study_areas_links[key].append(minor.text)
            else:
                study_areas_links[key] = [minor.text]
    
    write_studyarea_csv(study_areas_links)

# This function gets the name of the department from the beginning of the class' name ("MATH" from "MATH 6B").
# It's used for when a series of courses is listed like "I&C SCI 31-32-33". This is because the find_courses function will add to the list "I&C SCI 31", "32", and "33" (the latter two lack the department).
def get_prefix(class_name):
    # During my debugging, I found that the ascii value for the spaces on the UCI page is 160, so I'm including the value for a regular space and for the weird UCI space.
    while class_name[-1] != ' ' and ord(class_name[-1]) != 160:
        class_name = class_name[:-1]
    return class_name[:-1]

def swap_space_32_to_160(str):
    out = ""
    for letter in str:
        if ord(letter) == 32:
            out += chr(160)
        else:
            out += letter
    return out

# This function performs the searching for courses given a url for a major/minor/ge.
# tup = (url, header title)
def find_courses(tup):
    url = tup[0]
    header_title = tup[1]

    # The soup object takes the block of dense html in page and makes it easier to parse.
    page = requests.get(url)
    soup = bs(page.text, "html.parser")

    # The classes array stores the link objects. The classes_names array stores the class names.
    classes_obj = []
    classes_names = []
    aObjs = []

    if header_title == "GE":
        # Loop through each table of classes.
        for i in range(9):
            # Loop through each link object in each table and add it to the array.
            objs = soup.find_all("table")[i].find_all("a")
            aObjs += objs
    else:
        headers = soup.find_all("h4")
        for h4 in headers:
            if h4.text == header_title:
                aObjs = h4.find_next_sibling("div").find("table").find_all('a')

    for a in aObjs:
        classes_obj.append(a)

    # This loop adds all of the classes to the classes_names array, adding a prefix if it wasn't already present.
    for i in range(len(classes_obj)):
        # The if is checking to see if there exists a prefix on the class yet. All of the classes without prefixes begin with a space because of the webpage's formatting.
        if classes_obj[i].text[0] == ' ':
            # The classes without prefixes already begin with a space, but it has a different ascii value than the spaces on the site, so I'm swapping them out here.
            classes_names.append(get_prefix(classes_names[i-1]) + chr(160) + classes_obj[i].text[1:])
        else:
            classes_names.append(classes_obj[i].text)
    
    return classes_names

# This function returns the classes in common between two arrays of classes.
def find_shared(a, b):
    # Using sets allows for a quick comparison that ignores duplicates.
    a_set = set(a) 
    b_set = set(b) 
      
    if len(a_set.intersection(b_set)) > 0:
        out = list(a_set.intersection(b_set))
        out.sort()
        return out
    else:
        return ["no common elements"]

def translate_to_ge_category(nums):
    category_titles = {
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
        out.append(category_titles[str(n)][0])
    
    return out

# def find_ge_dupes():
#     courses_ge_cat_dict = gen_cat_dict()

#     for key, val in courses_ge_cat_dict.items():
#         if (len(val) > 1) and (3 in val and 7 in val):#any(item in val for item in [4, 5, 7, 8]):

# This function creates a list of all GE classes and their corresponding GE categories
def gen_cat_dict():
    course_list = find_courses(majors_dict["GE"])
    # Create a dictionary with an empty list for each course
    courses_ge_cat_dict = {a: [] for a in course_list}
    
    url = majors_dict["GE"][0]
    header_title = majors_dict["GE"][1]

    # The soup object takes the block of dense html in page and makes it easier to parse.
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    objs = soup.find_all("table")

    # Loop through each table of classes.
    for i in range(9):
        for course in objs[i].find_all("a"):
            courses_ge_cat_dict[course.text].append(i)

    return courses_ge_cat_dict

# This is the function called by Gui.py that combines all of the above functions
def full_lookup(course_a_str, course_b_str, dict):
    area1_courses = find_courses(dict[course_a_str])
    area2_courses = find_courses(dict[course_b_str])

    shared = find_shared(area1_courses, area2_courses)

    if (shared[0] != "no common elements"):
        # This if statement adds the GE categories to the end of the string if relevant
        if (course_a_str == "GE" or course_b_str == "GE"):
            courses_ge_cat_dict = gen_cat_dict()
            print(courses_ge_cat_dict)
            
            for i in range(len(shared)):
                a = str(translate_to_ge_category(courses_ge_cat_dict[shared[i]]))
                print(a)
                shared[i] += ": " + a
    return shared

if __name__ == "__main__":
    # full_lookup("ge", "cs")
    find_courses(('http://catalogue.uci.edu/thepaulmerageschoolofbusiness/undergraduateprograms/#minorstext', 'Requirements for the Undergraduate Minor in Accounting'))





"*************************old****************"
# def find_courses(tup):
#     url = tup[0]
#     num_tables = tup[1]
#     start_table = tup[2] # Starts at 0

#     # The soup object takes the block of dense html in page and makes it easier to parse.
#     page = requests.get(url)
#     soup = bs(page.text, "html.parser")

    # # The classes array stores the link objects. The classes_names array stores the class names.
    # classes_obj = []
    # classes_names = []

    # # Loop through each table of classes.
    # for i in range(start_table, start_table + num_tables):
    #     # Loop through each link object in each table and add it to the array.
    #     aObjs = soup.find_all("table")[i].find_all("a")
    #     for a in aObjs:
    #         classes_obj.append(a)

    # # This loop adds all of the classes to the classes_names array, adding a prefix if it wasn't already present.
    # for i in range(len(classes_obj)):
    #     # The if is checking to see if there exists a prefix on the class yet. All of the classes without prefixes begin with a space because of the webpage's formatting.
    #     if classes_obj[i].text[0] == ' ':
    #         # The classes without prefixes already begin with a space, but it has a different ascii value than the spaces on the site, so I'm swapping them out here.
    #         classes_names.append(get_prefix(classes_names[i-1]) + chr(160) + classes_obj[i].text[1:])
    #     else:
    #         classes_names.append(classes_obj[i].text)
    
#     return classes_names