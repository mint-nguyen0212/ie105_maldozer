import argparse
import os
from extract_feature import extract_feature
from set_constant import L,apk_path,apis_path
# Set L!!

def main(Args):
    # Convert all paths to absolute paths
    MalDir = os.path.abspath(Args.maldir)
    GoodDir = os.path.abspath(Args.gooddir)
    goodfeaturedir = os.path.abspath(Args.goodfeaturedir)
    malfeaturedir = os.path.abspath(Args.malfeaturedir) 
    Dir = dict()  
    Dir[MalDir] = malfeaturedir
    Dir[GoodDir] = goodfeaturedir
    extract_feature(Dir)  # Form a dict where keys are file directories and values are feature directories


def ParseArgs(TYPE,TYPE_list): # Runtime arguments
    '''
        This may be changed in the future; currently set for binary classification
    '''
    Args = argparse.ArgumentParser("maldozer")
    Args.add_argument("--maldir", default = apk_path+'/'+TYPE_list[1])  # Malware sample location for training data
    Args.add_argument("--gooddir", default=apk_path+'/'+TYPE_list[0])  # Benign sample location for training data
    Args.add_argument("--goodfeaturedir",default=apis_path+'/'+TYPE_list[0])
    Args.add_argument("--malfeaturedir",default=apis_path+'/'+TYPE_list[1])
    return Args.parse_args()

def get_api(TYPE,TYPE_list):
	main(ParseArgs(TYPE,TYPE_list))
	print("Having finished first stop:get apis!")
	return

if __name__ == "__main__":
	
	from set_constant import L,TYPE_list,TYPE


	get_api(TYPE,TYPE_list)
