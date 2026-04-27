import os 
from androguard.misc import AnalyzeAPK

def JudgeFileExist(FilePath):
    '''
        Given a file path, check whether the file exists
    '''
    if os.path.exists(FilePath)==True:
        return True
    else:
        return False

def ListFile(FilePath,extensions):
    '''
    Given a directory path and a file extension to filter, return a list of files
    '''
    Files = []
    filenames = os.listdir(FilePath)
    for file in filenames:
        Absolutepath = os.path.abspath(os.path.join(FilePath,file))  # Absolute path of the file
        if os.path.splitext(file)[1]==extensions:  # os.path.splitext separates filename and extension
            Files.append(Absolutepath)
    return Files


def extract_feature(ApkDirectoryPaths):
    '''
        Extract features from APK files in the given malware and benign software directories
    '''

    ApkFileList = []
    for FilePath in ApkDirectoryPaths.keys():
        # Add files with no extension and files with .apk extension to the list
        ApkFileList.extend(ListFile(FilePath,""))
        ApkFileList.extend(ListFile(FilePath,".apk"))

    for ApkFile in ApkFileList:
        # Save the extracted APK features into a file with .feature extension
        path = os.path.join(ApkDirectoryPaths[os.path.split(ApkFile)[0]],os.path.split(ApkFile)[1])

        if JudgeFileExist(path+'.feature'):
            pass
        else:
            try:
                a,d,dx = AnalyzeAPK(ApkFile)
                fp = open(path+'.feature','w')
                for Apkclass in dx.get_classes():
                    for meth in dx.classes[Apkclass.name].get_methods():
                        for _,call,_ in meth.get_xref_to():
                            fp.write("{}:{}\n".format(call.class_name,call.name))
                        #fp.write("{}\n".format(call.class_name))
                fp.close()
            except:
                continue
    return 


