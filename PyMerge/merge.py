from pathlib import *
import getopt
import sys
import os
from copy import deepcopy


global_include_dir = []
global_include_visited = []


def search_includes(file_path, not_def_macro):
    global global_include_visited, global_include_dir
    # global_include_visited.append(file_path)
    sys_include_path = []
    self_include_path = []
    with open(file_path, 'r', encoding='utf-8') as f:
        code_lines = f.readlines()
        curr_dir = str(PurePath(file_path).parent)
        look_for_endif = False
        look_for_elseif = False
        for line in code_lines:
            line = line.replace('\n', '')
            if look_for_endif:
                if line == '#endif':
                    look_for_endif = False
                continue
            if look_for_elseif and '#else' == line:
                look_for_endif = True
                look_for_elseif = False
            if '#ifdef' in line:
                def_found = False
                for it in not_def_macro:
                    if ('#ifdef ' + it) in line:
                        def_found = True
                        break
                if def_found:
                    look_for_endif = True
                    continue
            if '#ifndef' in line:
                ndef_found = False
                for it in not_def_macro:
                    if ('#ifndef ' + it) in line:
                        ndef_found = True
                        break
                if ndef_found:
                    look_for_elseif = True
            if line[0:8] == '#include':
                name_inc = line.replace('#include', '').split(' ')[1]
                if name_inc[0] == "<":
                    file_final = name_inc.replace('<', '').replace('>', '')
                    sys_include_path.append(file_final)
                elif name_inc[0] == '"':
                    file_final = name_inc.replace('"', '')
                    curr_include_dir = deepcopy(global_include_dir)
                    curr_include_dir.append(curr_dir)
                    flag_find = False
                    for path_tmp in curr_include_dir:
                        path_inc = path_tmp + '/' + file_final
                        if path_inc in global_include_visited:
                            flag_find = True
                            break
                        if Path(path_inc).is_file():
                            flag_find = True
                            global_include_visited.append(path_inc)
                            (sysm,selfm) = search_includes(path_inc, not_def_macro)
                            sys_include_path.extend(sysm)
                            self_include_path.extend(selfm)
                            break
                    if not flag_find:
                        print("Error! include file not found in all include dirs: ", name_inc)
                        print("exit...")
                        sys.exit()
                else:
                    print("Error, not "" or <> include style not allowed! exit...")
                    sys.exit()
        self_include_path.append(file_path)

    return sys_include_path, self_include_path


def merge(main_file_full_path, inc_dir=[], src_dir=[], save_full_path=None,
          extra_hea_suf=[], extra_src_suf=[], pro_root_dir='', debug=False,
          not_def_macro=[]):
    if not Path(main_file_full_path).is_file():
        print("main file not exist! Exit...")
        sys.exit()
    if pro_root_dir == '':
        pro_root_dir = '.'
    pro_root_dir = os.path.abspath(pro_root_dir)
    extra_hea_suf.append('.h')
    extra_src_suf.append('.cpp')
    main_file = PurePath(main_file_full_path)
    base_path = str(main_file.parent)
    base_name = str(main_file.name).replace('.cpp', '')
    global global_include_visited, global_include_dir
    global_include_visited.clear()
    global_include_dir.clear()
    global_include_dir.append(os.path.abspath(base_path))
    global_include_dir.append(pro_root_dir)
    for inc in inc_dir:
        global_include_dir.append(os.path.abspath(inc))
    if debug:
        for gd in global_include_dir:
            print('gd: ', global_include_dir)
    if save_full_path is None:
        save_full_path = base_path + '/' + base_name + '_merged.cpp'
    sys_inc, self_inc = search_includes(str(main_file), not_def_macro)
    # sys_inc = list(set(sys_inc))
    sys_inc = sorted(set(sys_inc), key=sys_inc.index)
    for i in range(len(self_inc)):
        self_inc[i] = os.path.abspath(self_inc[i])
    self_inc = sorted(set(self_inc), key=self_inc.index)
    abs_main = os.path.abspath(main_file_full_path)
    assert abs_main in self_inc
    self_inc.remove(abs_main)
    if debug:
        for sc in self_inc:
            print(sc)
    self_sour = [abs_main]
    for inc_file in self_inc:
        inc_suf = os.path.splitext(inc_file)[-1]
        assert inc_suf in extra_hea_suf
        for src_suf in extra_src_suf:
            sour_file = inc_file.replace(inc_suf, src_suf)
            if Path(sour_file).is_file():
                self_sour.append(sour_file)
        for src_suf in extra_src_suf:
            for pre_src_path in src_dir:
                src_name = Path(os.path.abspath(pre_src_path) + '/'
                                + str(PurePath(inc_file).name).replace(inc_suf, src_suf))
                if src_name.is_file():
                    self_sour.append(str(src_name))
    self_sour = sorted(set(self_sour), key=self_sour.index)
    if debug:
        for sr in self_sour:
            print(sr)
    for sour_wenjian in self_sour:
        if debug:
            print(sour_wenjian)
        with open(sour_wenjian, 'r', encoding='utf-8') as fwj:
            wenjian_dir = str(PurePath(sour_wenjian).parent)
            wenjian_lines = fwj.readlines()
            for ec_line in wenjian_lines:
                ec_line = ec_line.replace('\n', '')
                if '#include' in ec_line:
                    ret_line = ec_line.replace('#include', '').split(' ')[1]
                    if ret_line[0] == '"':
                        aaa_line = ret_line.replace('"', '')
                        bbb_path = os.path.abspath(wenjian_dir + '/' + aaa_line)
                        if Path(bbb_path).is_file():
                            if debug:
                                print('bbb: ', bbb_path)
                            self_inc.append(bbb_path)
                        bbb_path = os.path.abspath(pro_root_dir + '/' + aaa_line)
                        if Path(bbb_path).is_file():
                            if debug:
                                print('bbb: ', bbb_path)
                            self_inc.append(bbb_path)
                    elif ret_line[0] == '<':
                        aaa_line = ret_line.replace('<', '').replace('>', '')
                        bbb_path = aaa_line
                        sys_inc.append(bbb_path)
                    else:
                        print('error!, illegal grammar! exit...')
                        sys.exit()

    self_inc = sorted(set(self_inc), key=self_inc.index)
    # sys_inc = list(set(sys_inc))
    sys_inc = sorted(set(sys_inc), key=sys_inc.index)
    with open(save_full_path, 'w', encoding='utf-8') as f:
        f.write("// ######## begin of system include headers ########\n\n\n")
        for file_tmp in sys_inc:
            full_tmp = '#include <' + file_tmp + '>\n'
            f.write(full_tmp)
        f.write("\n\n// ######## end of system include headers ########\n\n\n")
        f.write("// ######## begin of self header files\n\n\n")
        for file_tmp in self_inc:
            f.write("// begin " + file_tmp + '\n')
            with open(file_tmp, 'r', encoding='utf-8') as fp_tmp:
                sour_line_tmp = fp_tmp.readlines()
                for line_tmp in sour_line_tmp:
                    if '#include' in line_tmp or line_tmp == '\n':
                        continue
                    if '#pragma once' in line_tmp:
                        continue
                    f.write(line_tmp)
            f.write("\n// end of " + file_tmp + "\n")
        f.write("\n\n// ######## end of self header files ######## \n\n\n")
        f.write("// ######## begin of source files ######## \n\n\n")
        for file_tmp in self_sour:
            f.write("// begin of " + file_tmp + '\n')
            with open(file_tmp, 'r', encoding='utf-8') as fp_tmp:
                sour_line_tmp = fp_tmp.readlines()
                for line_tmp in sour_line_tmp:
                    if '#include' in line_tmp or line_tmp == '\n':
                        continue
                    f.write(line_tmp)
            f.write("\n// end of " + file_tmp + "\n\n")
        f.write("// ######## end of source files ######## \n\n\n")
