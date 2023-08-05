import os,numpy,pandas,subprocess
#
#
def convert_10X(data_10X, project):
    if not os.path.exists(project+'/matrix'): subprocess.check_call('mkdir '+project+'/matrix', shell=True)
    if not os.path.exists(project+'/peak'): subprocess.check_call('mkdir '+project+'/peak', shell=True)
    subprocess.check_call('cp '+data_10X+'/matrix.mtx '+project+'/matrix/filtered_reads.mtx', shell=True)
    subprocess.check_call('cp '+data_10X+'/peaks.bed '+project+'/peak/top_filtered_peaks.bed', shell=True)
    cells = [x[:-1] for x in open(data_10X+'/barcodes.tsv').readlines()]
    celltypes = ['10X']*len(cells)
    cells_df = pandas.DataFrame(celltypes, index=cells, columns=['notes'])
    cells_df.to_csv(project+'/matrix/filtered_cells.csv', sep='\t')
    return
#
#
