import json
import os
import time


module_dir = os.path.dirname(__file__)
backup_path = os.path.join(module_dir, '../backup_courses.json')
source_path = os.path.join(module_dir, '../UCSD_courses.json')


def reset_json():
    """
    Copies the backup file into source
    """
    with open(backup_path) as backup:
        with open(source_path, 'w') as source:
            source.write(backup.read())


def import_json():
    """
    Reads the json file from source and returns a dictionary of its data
    :return: A dictionary holding the course data
    """
    with open(source_path) as source:
        return json.load(source)


def export_dict(a_dict):
    """
    Takes the dictionary and adds it to the json file.
    :param a_dict: The dictionary to convert to json and export into file
    """
    with open(source_path, 'w') as source:
        json.dump(a_dict, source, indent=4)


def add_courses(prereqs):
    """
    Ask user for courses and appends them into the prerequisites list
    :param prereqs: The list which we want to append user responses to
    """
    course = input()
    while course != 'done':
        if course:
            prereqs.append(course)
        course = input()


def adder_tool():
    """
    The entry point -- Asks user for course they want to add and its
    prerequisite courses.
    """
    print('Welcome to the JSON adder tool.')
    course_json = import_json()
    while True:
        print('Please enter the course you would like to add prerequisites to.'
              ' Or enter "RESET" to reset the json to its original data.\n'
              '(If the course already exists in the JSON, '
              'it will be overwritten)')
        main_course = input()
        if main_course == 'RESET':
            reset_json()
            print('UCSD_courses.json has been reset')
            time.sleep(1)
            print('Thank you for using the JSON adder tool!')
            time.sleep(1)
            return
        elif main_course in ['', 'exit', 'quit']:
            print('Thank you for using the JSON adder tool!')
            time.sleep(1)
            return
        # AND COURSES
        prereqs = []
        print('Now enter your AND prerequisite courses one by one and enter '
              '"done" when you\'re ready to enter OR classes. If the course '
              'can be taken concurrently, add an asterisk (*) to the end of '
              'the course name')
        add_courses(prereqs)

        # Get number of sets of OR classes with input checks
        while True:
            try:
                num_sets = input('Now we\'ll add the OR courses. '
                                 'How many OR sets are there? If there are '
                                 'none, enter "0" or nothing\n')
                if num_sets == '':
                    num_sets = 0
                else:
                    num_sets = int(num_sets)
                break
            except ValueError:
                print('That is not a valid number! Try again')

        for i in range(num_sets):
            print('Enter the OR courses for set ' + str(i + 1) +
                  '. Enter "done" when you\'re done with the set')
            or_sets = []
            add_courses(or_sets)
            prereqs.append(or_sets)

        course_json[main_course] = prereqs
        print('The course, ' + main_course + ', now has ', end='')
        print(prereqs, end='')
        print(' added to it')

        choice = input('Would you like to add more classes? (Y/N)\n')
        while choice not in ['Y', 'N']:
            choice = input('That is not an option. Would you like to add '
                           'more classes? (Y/N)')
        if choice == 'N':
            break

    print('Saving all changes to JSON file...')
    export_dict(course_json)
    print('Thank you for using the JSON adder tool!')
    time.sleep(1)


if __name__ == '__main__':
    adder_tool()
