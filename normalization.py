# coding=utf-8
import os
import re
import shutil
import argparse
from clean_gadget import clean_gadget

def parse_options():
    parser = argparse.ArgumentParser(description='Normalization.')
    parser.add_argument('-i', '--input', help='The dir path of input dataset', type=str, required=True)
    args = parser.parse_args()
    return args

def normalize(path):
    setfolderlist = os.listdir(path)
    for setfolder in setfolderlist:
        catefolderlist = os.listdir(path + "//" + setfolder)
        #print(catefolderlist)
        for catefolder in catefolderlist:
            filepath = path + "//" + setfolder + "//" + catefolder
            print(catefolder)
            pro_one_file(filepath)

def pro_one_file(filepath):
    with open(filepath, "r") as file:
        code = file.read()

    file.close()
    code = re.sub('(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/', "", code)
    #print(code)
    with open(filepath, "w") as file:
        file.write(code.strip())
    file.close()

    with open(filepath, "r") as file:
        org_code = file.readlines()
        # print(org_code)
        nor_code = clean_gadget(org_code)
    file.close()
    with open(filepath, "w") as file:
        file.writelines(nor_code)
    file.close()

def main():
    args = parse_options()
    normalize(args.input)
    

if __name__ == '__main__':
    main()
 