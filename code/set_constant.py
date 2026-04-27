########## choose path ##########
apk_path = '../data/apk'
if apk_path == '../data/apk_2_152':
	TYPE = 2 # Number of classes
	TYPE_list=["goodware","malware"]
elif apk_path  == '/data/ugstudent1/thordroid/code/data/apk_20':
	TYPE = 21
	TYPE_list=["goodware","Adrd","FakeInstaller","Iconosys","SendPay","BaseBridge","FakeRun","Imlog","SMSreg","DroidDream","Gappusin","Kmin","DroidKungFu","Geinimi","MobileTx","ExploitLinuxLotoor","GinMaster","Opfake","FakeDoc","Glodream","Plankton"]
elif apk_path == '../data/apk':
	TYPE = 2 # Number of classes
	TYPE_list=["goodware","malware"]

apis_path='../data/apis'
identifiers_path='../data/identifiers'
train_path="../data/identifiers/train"
test_path="../data/identifiers/test"
useful_api_class="../../useful_api_class"
classes="../../classes"
mapping_to_identifier_path='../method_dict.pickle'
word2vec_model_path='./word2vec.model'
save_model_path = '../deep_learning.model' # Save the trained model here
type_map={TYPE_list[i]:i for i in range(TYPE)}
########## choose path ##########


########## word2vec ##########
K = 64 # K
L = 2500 # L
########## word2vec ##########


########## CNN ##########
maxpooling_size = (14,14)
batch_size=10  # Number of samples fed to the model per batch
filter_count = 512  # filter count, 512 in the paper
kernel_size_ = 3	 # kernel size i.e. filter size, 3 in the paper
first_neuron_count = 256	# Number of neurons in the first fully connected layer, 256 in the paper
dropout = 0.5   # Regularization parameter, 0.5 in the paper
epochs_=15	   # epoch
val_split=0.2	# Validation set ratio
test_split = 0.1
KFCV = True
KFCV_K = 5
########## CNN ##########


########## fuctions ##########
def Get_file_line(filename,L=-1):# Read lines of a file into a list; L specifies how many lines to read (-1 means all); pads with 0 if not enough lines
	with open(filename,encoding='utf-8') as f:
		Sequence = f.readlines()
		if L != -1:
			lens=len(Sequence)
			if L <= lens:
				Sequence=Sequence[:L]
			else:
				Sequence.extend(['0\n']*(L-lens))
	return Sequence

def sentences_append(sentences,path,L=-1):# Read all file lines under the path directory into a 2D matrix (i=file, j=line); L specifies how many lines per file (-1 means all)
	import os
	files=os.listdir(path)
	for i in range(len(files)):
		sentences.append(Get_file_line(path+'/' + files[i],L))
	return files

def read_dict(path):# Read the mapping-to-identifier dictionary
	import pickle
	dict_file=open(path,'rb')
	dic=pickle.load(dict_file)
	return dic

def mkdir(path):# Create a directory
	import os
	folder = os.path.exists(path)
 
	if not folder:				   # Check if directory exists; if not, create it
		os.makedirs(path)			# makedirs creates intermediate directories if the path doesn't exist
	else:
		print ("---  There is this folder.  ---")

def folders_set():
	mkdir(identifiers_path)
	for i in range(TYPE):
		mkdir(apis_path+'/'+TYPE_list[i])
		mkdir(train_path+'/'+TYPE_list[i])
		mkdir(test_path+'/'+TYPE_list[i])

	return True
########## fuctions ##########


########## ??? ##########
folders_set()
########## ??? ##########
