def main(file_name:str,dbName:str):
    from Bio import SeqIO
    import pandas as pd
    from os import listdir as ls
    if not dbName.endswith('.parquet'):
        raise ValueError("dbName should be a parquet file")
    file=pd.read_parquet(dbName)
    for fasta in [file_name+i for i in ls(file_name) if '.fasta' in i]:
        data=SeqIO.parse(f'./{fasta}','fasta')
        fasta_file=open(fasta.replace('.fasta','_working_aa.fasta'),'w')
        for i in data:
            if 'X' not in i.seq:
                a,b,c=i.id.split(':')[0],i.id.split(':')[1],i.seq
                if (a,f'{a}:{b}') in file.index:
                    start,end=file.at[(a,f'{a}:{b}'),'alignStart'],file.at[(a,f'{a}:{b}'),'alignEnd']
                    header,seq=f'{a}:{b} | {start}_{end}',c[int(start):int(end)]
                    content=f'>{header}\n{seq}\n'
                    _=fasta_file.write(content)
        fasta_file.close()

if __name__=='__main__':
    from argparse import ArgumentParser
    parse=ArgumentParser(prog='Fasta translator and domain getter')
    parse.add_argument('--input','-i',help='Fasta folder name',type=str)
    parse.add_argument('--dataframe','-db',help='DataFrame having domain info',type=str)
    args=parse.parse_args()
    main(file_name=args.input,dbName=args.dataframe)
