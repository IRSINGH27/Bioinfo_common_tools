import argparse

parser=argparse.ArgumentParser(prog='GCF Protein Fetcher',description='Takes gcf and fetch its protein.faa')
parser.add_argument('-i','--input',help='provide single gcf or list of gcf seperated by newline')
parser.add_argument('-o','--output',help='Output_directory')
args=parser.parse_args()
def main():
    _=link_generator(args.input)
    # print(_)
    wget_function(_,args.output) 

def link_generator(_file:str):
    from re import findall
    with open(_file,'r') as f:
        content=f.read()
        if '\n' in content:
            content=content.split('\n')[0:-1]
        else:
            pass
    if type(content) is list:
        dict_gcf={i:'/'.join(findall(r'...',findall(r'\d+',i)[0])) for i in content}
    else:
        dict_gcf={content:'/'.join(findall(r'...',findall(r'\d+',content)))}
    dict_gcf=link_corrector(dict_gcf)
    return dict_gcf
    
def wget_function(_dict:dict,output:str):
    import requests
    import os
    if os.path.exists(output) == False:
        os.mkdir(output)
    else:
        pass
    for i in _dict.keys():
        # print(i,_dict[i])
        print("{} started".format(i))
        with open(output+'/'+i+'_protein.faa.gz','wb') as f:
            data=requests.get(_dict[i])
            f.write(data.content)
        print("done")
def link_corrector(_dict:dict):
    from bs4 import BeautifulSoup as bs
    from requests import get
    try:
        for i in _dict.keys():
            _link='https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/'+_dict[i]
            content=bs(get(_link).text,'html.parser')
            l=max([i.text for i in content.find_all('a') if 'GCF_' in i.text])
            _link=_link+'/'+l+'/'+l+'_protein.faa.gz'
            _dict[i]=_link
    except:
        print(l)
    return _dict
    
if __name__ =='__main__':
    main()