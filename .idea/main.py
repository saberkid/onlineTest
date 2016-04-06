from parse_task import *
from core import *
from test import *

global GRAPHS
global CORES
GRAPHS = []
CORES = []
CORE_NUM = 10
TESTING = None#core instance under test

def build_log():
    task_status_dic = {1:"running", 2:"stalled"}
    test_status_dic = {1:"PRE TEST", 2:"TESTING", 3:"AFTER TEST"}
    print '**********',"cycle:",CYCLE,'************'
    for i in xrange(len(CORES)):
        if  CORES[i].status:
            if CORES[i].test:
                print "core%d:"%(i+1), "(type%d)"%CORES[i].type, CORES[i].status.task_id,' ',task_status_dic[CORES[i].status.status],\
                    " Test is now in %s"%test_status_dic[CORES[i].test.status]
            else:
                 print "core%d:"%(i+1), "(type%d)"%CORES[i].type, CORES[i].status.task_id,' ',task_status_dic[CORES[i].status.status],\
                " Not under test"
        else:
            if CORES[i].test:
                print "core%d:"%(i+1), "(type%d)"%CORES[i].type, "vacant.", " Test is now in %s"%test_status_dic[CORES[i].test.status]
            else:
                print "core%d:"%(i+1), "(type%d)"%CORES[i].type, "vacant.", " Not under test"

def task_dispatch():
    for i in xrange(len(CORES)):
        if not CORES[i].status:#vacant core
            if len(CORES[i].task_list):
                if CORES[i].task_list[0].is_executable():
                    if not CORES[i].test: #not under test
                        CORES[i].status = CORES[i].task_list[0]
                        del CORES[i].task_list[0]
                        CORES[i].status.status = 1
                    else:   #under test
                        if CORES[i].test.status != 1 and CORES[i].test.status != 3:
                            CORES[i].status = CORES[i].task_list[0]
                            del CORES[i].task_list[0]
                            CORES[i].status.status = 1
                            
        else:#core running task
            if not CORES[i].test:#not under test
                CORES[i].status.runtime += 1
                if CORES[i].status.is_finished():
                    CORES[i].status = None
            else:#under test
                if CORES[i].test.status == 1:           #pre test
                    if CORES[i].type:                   #unbreakable
                        CORES[i].status.runtime += 1
                        if CORES[i].status.is_finished():
                            CORES[i].status = None
                    else:                                   #breakable
                        CORES[i].status.status = 2           #task stalled
                elif CORES[i].test.status == 2:             #under test
                    CORES[i].status.status = 1
                    CORES[i].status.runtime += 1
                    if CORES[i].status.is_finished():
                        CORES[i].status = None
                
                else:                                   #after_test
                    pass


def is_test_finished():
    for i in xrange(len(CORES)):
        if not CORES[i].test_status:
            return 0
    return 1
def is_task_finished():
    for i in xrange(len(CORES)):
        if len(CORES[i].task_list):
            return 1
    return 0

def core_for_test():
    for i in xrange(len(CORES)):
        if not CORES[i].test_status:
            if not CORES[i].type:
                CORES[i].test  = test()
                return CORES[i]
    for i in xrange(len(CORES)):
        if not CORES[i].test_status:
            CORES[i].test  = test()
            return CORES[i]

def test_dispatch():
    # if not TESTING.test.status:#initial
    #     if TESTING.type:#unbreakable
    #         if not TESTING.status:
    #             TESTING.test.status = 1
    #     else:#breakable
    #         TESTING.test.status = 1
    global TESTING
    if TESTING.test.status == 1: #pre_test
        if TESTING.type:#unbreakable
            if not TESTING.status:
                TESTING.test.pre_test -= 1
                if TESTING.test.pre_test <= 0:
                    TESTING.test.status = 2
        else:#breakable
            TESTING.test.pre_test -= 1
            if TESTING.test.pre_test <= 0:
                TESTING.test.status = 2

    elif TESTING.test.status == 2: #under test
         if TESTING.type:#unbreakable
            TESTING.test.under_test -= 1
            if TESTING.test.under_test <= 0 and TESTING.status == None:
                TESTING.test.status = 3
         else:#breakable
            TESTING.test.under_test -= 1
            if TESTING.test.under_test <= 0:
                TESTING.test.status = 3
            if TESTING.status:
                TESTING.status.status = 2#task stalled

    else:
        TESTING.test.after_test -= 1
        if TESTING.test.after_test <= 0:
            TESTING.test_status = 1
            if TESTING.status:
                TESTING.status.status = 1
            TESTING.test = None
            TESTING = None

def run_graph(graph):
    global CYCLE
    global TEST_FINISHED
    global TASK_FINISHED
    global TESTING
    CYCLE = 0
    TEST_FINISHED = 0
    TASK_FINISHED = 0
    while not (TASK_FINISHED and TEST_FINISHED):
        CYCLE += 1

        # build_log()
        if not TESTING:
                TESTING = core_for_test()
                test_dispatch()
                task_dispatch()
        else:
            test_dispatch()
            task_dispatch()

        TEST_FINISHED = is_test_finished()
        TASK_FINISHED = is_task_finished()
        build_log()






if __name__ == '__main__':
    # global GRAPHS
    # global CORES


    for i in range(CORE_NUM):
        CORES.append(core(i+1,1))
    filename = raw_input("ENTER YOUR TG FILENAME:\n")
    file_object = open(filename)
    try:
        tgff_file = file_object.read()
    finally:
        file_object.close()
    parse_task(tgff_file, CORES, GRAPHS)

    for graph_num in xrange(len(GRAPHS)):
        run_graph(GRAPHS[graph_num])



