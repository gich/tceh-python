import sys

first_start = True
print "Welcome to Quizzzes! \n"

if sys.version_info[0] == 2:
    input_function = raw_input
else:
    input_function = input

name = input_function("Please, enter your name: ")
print "\nHi, {}! We have following quizes for you: ".format(name)

test_dict = {}
with open('test_list.txt', 'r') as fh:
    for i, line in enumerate(fh):
        test_name, test_file = line.split(";")
        test_dict[str(i+1)] = {"test_name" : test_name, "test_file" : test_file}
        print "{}. {}.".format(i + 1, test_name)

while True:
    quiz_num = input_function('\nPlease, enter quiz num or type "q" for exit: ')
    if quiz_num == 'q':
        break
    elif quiz_num in test_dict:
        print 'You select "{}".'.format(test_dict[quiz_num]["test_name"])
        # logic here
    else:
        print "Incorrect input. Try again."
