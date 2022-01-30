// ######## begin of system include headers ########


#include <iostream>


// ######## end of system include headers ########


// ######## begin of self header files


// begin /Users/syys/PycharmProjects/PyMerge/test/include/hea1.h
//
// Created by syys on 2022/1/29.
//
#ifndef TEST_HEA1_H
#define TEST_HEA1_H
void hea1_f1();
#endif //TEST_HEA1_H

// end of /Users/syys/PycharmProjects/PyMerge/test/include/hea1.h
// begin /Users/syys/PycharmProjects/PyMerge/test/third_lib/include/third_lib.h
#ifndef _THIRD_LIB_INCLUDED_
#define _THIRD_LIB_INCLUDED_ 
void info_print();
#endif 

// end of /Users/syys/PycharmProjects/PyMerge/test/third_lib/include/third_lib.h
// begin /Users/syys/PycharmProjects/PyMerge/test/include/hea2.h
//
// Created by syys on 2022/1/30.
//
#ifndef TEST_MERGE_HEA2_H
#define TEST_MERGE_HEA2_H
void hea2_f1();
#endif //TEST_MERGE_HEA2_H

// end of /Users/syys/PycharmProjects/PyMerge/test/include/hea2.h


// ######## end of self header files ######## 


// ######## begin of source files ######## 


// begin of /Users/syys/PycharmProjects/PyMerge/test/source/main.cpp
//
// Created by syys on 2022/1/29.
//
int main()
{
    hea1_f1();
    hea2_f1();
    return 0;
}
// end of /Users/syys/PycharmProjects/PyMerge/test/source/main.cpp

// begin of /Users/syys/PycharmProjects/PyMerge/test/source/hea1.cpp
//
// Created by syys on 2022/1/29.
//
void hea1_f1() {
    std::cout << "header 1 function 1" << std::endl;
}
// end of /Users/syys/PycharmProjects/PyMerge/test/source/hea1.cpp

// begin of /Users/syys/PycharmProjects/PyMerge/test/source/hea2.cpp
//
// Created by syys on 2022/1/30.
//
void hea2_f1() {
    std::cout << "hea2 f1 referring third lib" << std::endl;
    info_print();
}
// end of /Users/syys/PycharmProjects/PyMerge/test/source/hea2.cpp

// ######## end of source files ######## 


