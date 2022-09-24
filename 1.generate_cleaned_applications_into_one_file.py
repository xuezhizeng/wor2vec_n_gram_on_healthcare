import os

path = os.getcwd()
print("path:",path)

def readfile(path):
    fp = open(path, "r", encoding='utf-8', errors='ignore')
    content = fp.read()
    fp.close()
    return content

#this function is used to list all files in one folder but ingore the hidden file
def listdir_nohidden(dir):
    #print("dir:",dir)
    newpath = os.path.join(path + '/output',dir)
    print("newpath:",newpath)
    for f in os.listdir(newpath + '/'):
        if not f.startswith('.'):
            yield f




def generate_cleaned_application_text(clean_data_path,application_research_files_path):
    #for i in range(1):
    with open(application_research_files_path, 'w', encoding='utf_8') as application_research_files:
        catelist = listdir_nohidden(clean_data_path[0] + '/')
        print("catelist:", catelist)
        for mydir in catelist:
            class_path = path + '/output/' + clean_data_path[0] + '/' + mydir + '/'
            file_list = listdir_nohidden(class_path)
            for file_path in file_list:
                fullname = class_path + file_path
                application_id = file_path.strip().split()[0]
                content = readfile(fullname)
                label = mydir
                line = application_id + '\t\t\t' + content
                application_research_files.write(line + '\n')


if __name__ == '__main__':

    clean_data_path = ['research_files_clean']
    #application_research_files_path = open(path + '/output/application_research_files.txt', 'a')
    cleaned_application_research_files_path = os.path.join(path + '/output', 'cleaned_application_research_files.txt')
    print("application_research_files_path:",cleaned_application_research_files_path)
    generate_cleaned_application_text(clean_data_path,cleaned_application_research_files_path)
