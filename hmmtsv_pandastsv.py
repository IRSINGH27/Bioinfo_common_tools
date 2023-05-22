import os
import argparse
import pandas as pd
parser=argparse.ArgumentParser(prog='hmmtsv to pandas tsv',description='Takes hmm tsv file and convert it into pandas tsv')
parser.add_argument('-i','--input',help='hmm tsv')
parser.add_argument('-o','--output',help='pandas file')
args=parser.parse_args()

def main():
    df=convertor(_file=args.input)
    df.to_csv(args.output,sep='\t')
def convertor(_file:str)->pd.DataFrame:
    import re
    with open(_file,'r') as f:
                file=f.read().split('\n')[0:-1]
    header=['target_name','accession', 'query_name','accession_2','E-value','score','bias','E-value_2','score_2','bias_2','exp','reg','clu','ov','env','dom','rep','inc','description_of_target']
    df_file=[]
    for line in file:
        if '#' !=line[0]:
            temp_df1=re.sub(r'\s+',' ',line)
            temp_df2=re.split(r'\s',temp_df1)[:18]
            last_column='_'.join(re.split(r'\s',temp_df1)[18::])
            temp_df2.append(last_column)
            df_file.append(temp_df2)
    df=pd.DataFrame.from_records(df_file,columns=header)
    del df_file,temp_df1,temp_df2,last_column,line,header
    df=df.fillna('-')
    for i in df.index:
        df.at[i,'score']=float(df.at[i,'score'])
        df.at[i,'E-value']=float(df.at[i,'E-value'])
        df.at[i,'bias']=float(df.at[i,'bias'])
        df.at[i,'score_2']=float(df.at[i,'score_2'])
        df.at[i,'E-value_2']=float(df.at[i,'E-value_2'])
        df.at[i,'bias_2']=float(df.at[i,'bias_2'])
    return df
if __name__=='__main__':
	main()
