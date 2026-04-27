from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import word2vec
import os
from set_constant import K,train_path,test_path,word2vec_model_path
from set_constant import sentences_append

def word_count(nums):
    dict={}
    for it in nums:
        if it not in dict:
            dict[it] = 1
        else:
            dict[it] += 1
    return dict

def word2evc_test(sentences,_min_count=1,_hs=1,_window=4,_size=K):
	path = get_tmpfile(word2vec_model_path) # Create temporary file
	'''
	·  sentences: Can be a list. For large corpora, it is recommended to use BrownCorpus, Text8Corpus, or LineSentence.
	·  sg: Sets the training algorithm. Default is 0 (CBOW); sg=1 uses skip-gram.
	·  size: Dimensionality of the feature vectors. Default is 100. Larger sizes need more training data but yield better results. Recommended range: tens to hundreds.
	·  window: Maximum distance between the current word and the predicted word within a sentence.
	·  alpha: Learning rate.
	·  seed: Seed for the random number generator. Related to word vector initialization.
	·  min_count: Prunes the dictionary. Words with frequency less than min_count are discarded. Default is 5.
	·  max_vocab_size: Sets a RAM limit during vocabulary building. If unique words exceed this, the least frequent one is removed. Approximately 1GB of RAM per 10 million words. Set to None for no limit.
	·  sample: Threshold for random downsampling of high-frequency words. Default is 1e-3, range is (0, 1e-5).
	·  workers: Controls the number of parallel training threads.
	·  hs: If 1, hierarchical softmax is used. If 0 (default), negative sampling is used.
	·  negative: If > 0, negative sampling is used. Sets how many noise words to use.
	·  cbow_mean: If 0, uses sum of context word vectors; if 1 (default), uses mean. Only applies to CBOW.
	·  hashfxn: Hash function for weight initialization. Default is Python's hash function.
	·  iter: Number of iterations. Default is 5.
	·  trim_rule: Sets vocabulary trimming rules, specifying which words to keep and which to discard. Can be None (min_count is used) or a function that returns RULE_DISCARD, utils.RULE_KEEP, or utils.RULE_DEFAULT.
	·  sorted_vocab: If 1 (default), words are sorted by frequency in descending order before assigning word indices.
	·  batch_words: Number of words passed to each thread per batch. Default is 10000.
	'''# Word2Vec function parameter annotations
	model = word2vec.Word2Vec(sentences, hs=_hs,min_count=_min_count,window=_window,size=_size)
	model.save(word2vec_model_path)
	return model


def word2vec_model(TYPE,TYPE_list):
	sentences=[] # Corpus
	for i in range(0,TYPE):
		sentences_append(sentences,train_path+"/"+TYPE_list[i])
		sentences_append(sentences,test_path+"/"+TYPE_list[i])
	# Word2Vec training
	min_counts=1
	model=word2evc_test(sentences,min_counts)
	# Build a frequency dictionary; when generating the matrix, entries with count less than min_counts are discarded

	#Counter=[]
	#for m in sentences:
	#	Counter.append(word_count(m))

	#if mapping:
	#	# Map the application's API sequence to a matrix based on the mapping
	#	for i in range(len(sentences)):
	#		Matrix=[] # Each Matrix corresponds to one App
	#		for j in sentences[i]:
	#			if Counter[i][j]>=min_counts:
	#				Matrix_line=model.wv[j]# Convert API to vector using the model
	#				Matrix.append(Matrix_line.tolist())
	#		# Save the matrix to a file
	#		x=len(goodfile)
	#		if(i<x):
	#			f = open('./code/data/matrix/goodmatrix/'+goodfile[i]+'.Coded', "w")
	#		else:
	#			f = open('./code/data/matrix/badmatrix/'+malfile[i-x]+'.Coded', "w")
	#		f.write(str(Matrix))
	#		f.close()
	print("Having finished third stop:word2vec!")


	return model
if __name__=="__main__":
	from set_constant import TYPE_list,TYPE

	word2vec_model(TYPE,TYPE_list)
