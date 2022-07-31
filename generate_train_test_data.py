import pickle, os, glob
import argparse
import pandas as pd
from collections import Counter
def sava_data(filename, data):
    print("开始保存数据至于：", filename)
    f = open(filename, 'wb')
    pickle.dump(data, f)
    f.close()

def load_data(filename):
    print("开始读取数据于：", filename)
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close()
    return data

def parse_options():
    parser = argparse.ArgumentParser(description='Generate and split train datasettest_data.')
    parser.add_argument('-i', '--input', help='The path of a dir which consists of some pkl_files')
    parser.add_argument('-o', '--out', help='The path of output.', required=True)
    parser.add_argument('-n', '--num', help='Num of K-fold.', required=True)
    args = parser.parse_args()
    return args
    
def generate_dataframe(input_path, save_path):
    input_path = input_path + "/" if input_path[-1] != "/" else input_path
    save_path = save_path + "/" if save_path[-1] != "/" else save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    dic = []
    for type_name in os.listdir(input_path):
        dicname = input_path + type_name
        filename = glob.glob(dicname + "/*.pkl")
        for file in filename:
            data = load_data(file)
            dic.append({
                "filename": file.split("/")[-1].rstrip(".pkl"), 
                "length":   len(data[0]), 
                "data":     data, 
                "label":    0 if type_name == "No-Vul" else 1})
    final_dic = pd.DataFrame(dic)
    sava_data(save_path + "all_data.pkl", final_dic)

def gather_data(input_path, output_path):
    # generate_dataframe("/root/data/qm_data/vulcnn/data/outputs/ffmpeg", "/root/data/qm_data/vulcnn/data/pkl/ffmpeg")
    # generate_dataframe("/root/data/qm_data/vulcnn/data/outputs/qemu", "/root/data/qm_data/vulcnn/data/pkl/qemu")
    # generate_dataframe("/root/data/qm_data/vulcnn/data/outputs/sard", "/root/data/qm_data/vulcnn/data/pkl/sard")
    # generate_dataframe("/root/data/qm_data/vulcnn/data/outputs/sard-1", "/root/data/qm_data/vulcnn/data/pkl/sard-1")
    # generate_dataframe("/root/data/qm_data/vulcnn/data/outputs/sard-2", "/root/data/qm_data/vulcnn/data/pkl/sard-2")
    generate_dataframe(input_path, output_path)

def split_data(all_data_path, save_path, kfold_num):
    df_test = load_data(all_data_path)
    save_path = save_path + "/" if save_path[-1] != "/" else save_path
    seed = 0
    df_dict = {}
    train_dict = {i:{} for i in range(kfold_num)}
    test_dict = {i:{} for i in range(kfold_num)}
    from sklearn.model_selection import KFold
    kf = KFold(n_splits = kfold_num, shuffle = True, random_state = seed)
    for i in Counter(df_test.label.values):
        df_dict[i] = df_test[df_test.label == i]
        for epoch, result in enumerate(kf.split(df_dict[i])):
            train_dict[epoch][i]  = df_dict[i].iloc[result[0]]
            test_dict[epoch][i] =  df_dict[i].iloc[result[1]] 
    train_all = {i:pd.concat(train_dict[i], axis=0, ignore_index=True) for i in train_dict}
    test_all = {i:pd.concat(test_dict[i], axis=0, ignore_index=True) for i in test_dict}
    sava_data(save_path + "train.pkl", train_all)
    sava_data(save_path + "test.pkl", test_all)

def main():
    args = parse_options()
    input_path = args.input
    output_path = args.out
    kfold_num = args.num
    gather_data(input_path, output_path)
    # split_data("/root/data/qm_data/vulcnn/data/pkl/ffmpeg/all_data.pkl", "/root/data/qm_data/vulcnn/data/pkl/ffmpeg/")
    # split_data("/root/data/qm_data/vulcnn/data/pkl/qemu/all_data.pkl", "/root/data/qm_data/vulcnn/data/pkl/qemu/")
    # split_data("/root/data/qm_data/vulcnn/data/pkl/sard/all_data.pkl", "/root/data/qm_data/vulcnn/data/pkl/sard/")
    # split_data("/root/data/qm_data/vulcnn/data/pkl/sard-1/all_data.pkl", "/root/data/qm_data/vulcnn/data/pkl/sard-1/")
    # split_data("/root/data/qm_data/vulcnn/data/pkl/sard-2/all_data.pkl", "/root/data/qm_data/vulcnn/data/pkl/sard-2/")
    split_data(output_path + "all_data.pkl", output_path, kfold_num)
    

if __name__ == "__main__":
    main()