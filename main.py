from parse_task import *
from core import *
from test import *
from parse_type import *
import copy
CORE_NUM = 10
TESTING = None      #core instance under test
TEST_MODE_SCALAR = 1.2


def build_log():
    task_status_dic = {1:"running", 2:"stalled"}
    test_status_dic = {1:"PRE TEST", 2:"TESTING", 3:"AFTER TEST"}
    print '**********',"cycle:",CYCLE,'************'
    for i in xrange(len(CORES1)):
        if CORES1[i].status:
            if CORES1[i].test:
                print "core%d:"%(i+1), "(type%d)"%CORES1[i].type, CORES1[i].status.task_id, ' ',\
                    task_status_dic[CORES1[i].status.status],\
                    " Test is now in %s"%test_status_dic[CORES1[i].test.status]
            else:
                 print "core%d:"%(i+1), "(type%d)"%CORES1[i].type, CORES1[i].status.task_id, ' ',\
                    task_status_dic[CORES1[i].status.status],\
                    " Not under test"
        else:
            if CORES1[i].test:
                print "core%d:"%(i+1), "(type%d)"%CORES1[i].type, "vacant.", " Test is now in %s"%test_status_dic[CORES1[i].test.status]
            else:
                print "core%d:"%(i+1), "(type%d)"%CORES1[i].type, "vacant.", " Not under test"


def task_dispatch():
    for i in xrange(len(CORES1)):
        if not CORES1[i].status:                 #vacant core
            if len(CORES1[i].task_list):
                if CORES1[i].task_list[0].is_executable():
                    if not CORES1[i].test:       #not under test
                        CORES1[i].status = CORES1[i].task_list[0]
                        del CORES1[i].task_list[0]
                        CORES1[i].status.status = 1
                    else:           #under test
                        if CORES1[i].test.status != 1 and CORES1[i].test.status != 3:
                            CORES1[i].status = CORES1[i].task_list[0]
                            del CORES1[i].task_list[0]
                            CORES1[i].status.status = 1
                            
        else:#core running task
            if not CORES1[i].test:#not under test
                CORES1[i].status.runtime += 1
                if CORES1[i].status.is_finished():
                    CORES1[i].status = None
            else:       #under test
                if CORES1[i].test.status == 1:           #pre test
                    if CORES1[i].type:                   #unbreakable
                        CORES1[i].status.runtime += 1
                        if CORES1[i].status.is_finished():
                            CORES1[i].status = None
                    else:                                   #breakable
                        CORES1[i].status.status = 2           #task stalled
                elif CORES1[i].test.status == 2:             #under test
                    CORES1[i].status.status = 1
                    CORES1[i].status.runtime += 1/TEST_MODE_SCALAR
                    if CORES1[i].status.is_finished():
                        CORES1[i].status = None
                
                else:                                   #after_test
                    pass


def is_test_finished():
    for i in xrange(len(CORES1)):
        if not CORES1[i].test_status:
            return 0
    return 1


def is_task_finished():
    for i in xrange(len(CORES1)):
        if len(CORES1[i].task_list):
            return 0
    return 1


def core_for_test():
    for i in xrange(len(CORES1)):
        if not CORES1[i].test_status:
            if not CORES1[i].type:
                CORES1[i].test = TEST_DIC[i]
                return CORES1[i]
    for i in xrange(len(CORES1)):
        if not CORES1[i].test_status:
            CORES1[i].test = TEST_DIC[i]
            return CORES1[i]
    return None


def test_dispatch():
    global TESTING
    if TESTING.test.status == 1:        #pre_test
        if TESTING.type:                #unbreakable
            if not TESTING.status:
                TESTING.test.pre_test -= 1
                if TESTING.test.pre_test <= 0:
                    TESTING.test.status = 2
        else:               #breakable
            TESTING.test.pre_test -= 1
            if TESTING.test.pre_test <= 0:
                TESTING.test.status = 2

    elif TESTING.test.status == 2:          #under test
         if TESTING.type:                    #unbreakable
            TESTING.test.under_test -= 1
            if TESTING.test.under_test <= 0 and TESTING.status == None:
                TESTING.test.status = 3
         else:                          #breakable
            TESTING.test.under_test -= 1
            if TESTING.test.under_test <= 0:
                TESTING.test.status = 3
            if TESTING.status:
                TESTING.status.status = 2       #task stalled

    else:                   #after test
        TESTING.test.after_test -= 1
        if TESTING.test.after_test <= 0:
            TESTING.test_status = 1
            if TESTING.status:
                TESTING.status.status = 1
            TESTING.test = None
            TESTING = None


def run_graph():
    global CYCLE
    global TEST_FINISHED
    global TASK_FINISHED
    global TESTING
    CYCLE = 0
    TEST_FINISHED = 0
    TASK_FINISHED = 0
    test_recording = 1
    task_recording = 1
    while not (TASK_FINISHED and TEST_FINISHED):
        CYCLE += 1

        # build_log()
        if not TESTING and not TEST_FINISHED:
                TESTING = core_for_test()
                test_dispatch()
                task_dispatch()
        else:
            if not TEST_FINISHED:
                test_dispatch()
            task_dispatch()

        TEST_FINISHED = is_test_finished()
        TASK_FINISHED = is_task_finished()
        if TEST_FINISHED and test_recording:
            test_finished_time = CYCLE
            test_recording = 0
        if TASK_FINISHED and task_recording:
            task_finished_time = CYCLE
            task_recording = 0
        build_log()
    print task_finished_time
    print test_finished_time


def run_graph_2():
    global CYCLE
    CYCLE = 0
    finished = 0
    while not finished:
        finished = 1
        CYCLE += 1
        for i in xrange(len(CORES1)):
            if not CORES2[i].status:
               if len(CORES2[i].task_list):
                     if CORES2[i].task_list[0].is_executable():
                        CORES2[i].status = CORES2[i].task_list[0]
                        del CORES2[i].task_list[0]
                        finished = 0
            else:
                 finished = 0
                 CORES2[i].status.runtime += 1
                 if CORES2[i].status.is_finished():
                     CORES2[i].status = None
    print CYCLE


def init():
    global CORES1
    CORES1 = []
    for i in range(CORE_NUM):
        if i == 4 or i == 5 or i == 9:
            CORES1.append(Core(i+1, 1))
        else:
            CORES1.append(Core(i+1, 0))

if __name__ == '__main__':
    global TEST_DIC
    TEST_DIC = test_dic_init()
    filename = raw_input("ENTER YOUR TG FILENAME:\n")
    file_object = open(filename)
    try:
        tgff_file = file_object.read()
    finally:
        file_object.close()
    init()
    type_dic = parse_type(tgff_file)
    parse_task(tgff_file, CORES1, type_dic)
    CORES2 = copy.deepcopy(CORES1)
    run_graph()
    run_graph_2()


