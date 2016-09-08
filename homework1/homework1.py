import sys
import os


def run_test(file_name):
    result = 0
    total = 0
    with open(file_name, 'r') as fh:
        while True:
            line = fh.readline().strip()
            if not line:
                break
            total += 1
            print "\n{}. {}".format(total, line)
            correct_answer = 0
            for i in range(4):
                variant, is_correct = fh.readline().strip().split(";")
                if is_correct == '1':
                    correct_answer = i+1
                print '   {}) {}'.format(i+1, variant)
            user_answer = input_function('Your answer is: ')
            if correct_answer == int(user_answer):
                result += 1
                print 'You have {} correct answer(s)'.format(result)
            else:
                print 'Incorrect answer.'
    return result, total


def log_result(user, quiz, result, total):
    if not os.path.isfile('results.txt'):
        open('results.txt', 'w').close()
    with open('results.txt', 'a') as fh:
        fh.write('{};{};{};{}\n'.format(user, quiz, result, total))

first_run = True
print "Welcome to Quizzes! \n"

if sys.version_info[0] == 2:
    input_function = raw_input
else:
    input_function = input

name = input_function("Please, enter your name: ")

while True:
    if first_run:
        print "\nHi, {}! We have following quizzes for you: ".format(name)
    else:
        print "\nAvailable quizzes: "
    test_dict = {}
    with open('test_list.txt', 'r') as fh:
        for i, line in enumerate(fh):
            test_name, test_file = line.strip().split(';')
            test_dict[str(i + 1)] = {'test_name': test_name,
                                     'test_file': test_file}
            print "{}. {}.".format(i + 1, test_name)

    quiz_num = input_function('\nEnter quiz number or type "q" for exit: ')
    if quiz_num == 'q':
        break
    elif quiz_num in test_dict:
        print 'You select "{}".'.format(test_dict[quiz_num]['test_name'])
        res, tot = run_test(test_dict[quiz_num]['test_file'])
        if res == tot:
            print "Excellent! You have no mistakes!"
        else:
            print 'You have {} correct answer(s)' \
                  ' for {} questions in total'.format(res, tot)

        log_result(name, test_dict[quiz_num]['test_name'], res, tot)
        first_run = False
    else:
        print 'Incorrect input. Try again.'
