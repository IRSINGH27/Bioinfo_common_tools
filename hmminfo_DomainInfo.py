def main(code):
    from Bio import SearchIO
    for data in SearchIO.parse(code,'hmmer3-text'):
        for hit in data:
            for hsp in hit:
                yield hit.id,data.id,str(hsp.bitscore),str(hsp.hit_range[0]),str(hsp.hit_range[-1])

def writer(code,_output,_input):
    name=_output+'/'+code.split('_')[0]+'_protein_domain_position.info'
    with open(name,'w') as f:
        f.write('ID\tdomainFam\tbitScore\talignStart\talignEnd\n')
        for data in main(code=f'{_input}{code}'):
            _=f.write('\t'.join(data)+'\n')
    return None

if __name__=='__main__':
    from argparse import ArgumentParser
    from os import listdir as ls
    from multiprocessing import Pool,Manager
    parse=ArgumentParser(prog='Hmminfo into info file')
    parse.add_argument('--input','-i', help='Input File folder',type=str)
    parse.add_argument('--output','-o', help='output File folder',type=str)
    parse.add_argument('--process','-nt', help='Cores multiprocess',type=int)
    args=parse.parse_args()
    with Manager() as man:
        codes=man.list([(i,args.output,args.input) for i in ls(args.input) if 'hmminfo' in i])
        with Pool(args.process) as p:
            p.starmap(writer,codes)
            