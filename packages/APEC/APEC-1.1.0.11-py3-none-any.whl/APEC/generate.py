import numpy,pandas,os,sys,time,scipy.io,scipy.sparse,scipy.stats,subprocess
#import numba
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn
from sklearn.decomposition import PCA
#
#
######## generate pseudotime trajectory by calling monocle
#
#
def monocle_trajectory(project, npc=5, around=[6, 25]):
    """
    project:  Path to the project folder.
    npc:      Number of principal components used to build trajectory, default=5.
    around:   Keep how many digits after the decimal point, default=[6, 25].
    """
    from rpy2.robjects.packages import importr
    from rpy2 import robjects
    reads_csv = project+'/matrix/Accesson_reads.csv'
    reads = pandas.read_csv(reads_csv, sep=',', index_col=0, engine='c', na_filter=False, low_memory=False)
    accessons = pandas.read_csv(project+'/matrix/Accesson_peaks.csv', sep='\t', index_col=0)
    matrix = numpy.around(reads.values, decimals=around[0])
    normal = numpy.array([x/x.sum()*1000000 for x in matrix])
    reads = pandas.DataFrame(normal, index=reads.index.values, columns=reads.columns.values)
#
    pca_result = PCA(n_components=npc, svd_solver='full').fit_transform(reads)
    pca_result = numpy.around(pca_result, decimals=around[1])
    reads = pandas.DataFrame(pca_result[:, :npc], columns=['pc'+str(x) for x in numpy.arange(0,npc)], index=reads.index)
    celltype_df = pandas.read_csv(project+'/matrix/filtered_cells.csv', sep='\t', index_col=0)
    input_csv = project+'/matrix/monocle_reads.csv'
    cells_csv = project+'/matrix/monocle_cells.tsv'
    peaks_csv = project+'/matrix/monocle_peaks.tsv'
    trajectory_csv = project+'/result/monocle_trajectory.csv'
    reduced_csv = project+'/result/monocle_reduced_dimension.csv'
    peaks_df = pandas.DataFrame(reads.columns.values, index=reads.columns.values, columns=['gene_short_name'])
    peaks_df.to_csv(peaks_csv, sep='\t')
    celltype_df.to_csv(cells_csv, sep='\t')
    reads.T.to_csv(input_csv, sep=',')
#
    importr("monocle")
    expr_matrix = robjects.r('read.csv')(input_csv, header=True, sep=',', **{'row.names':1, 'check.names':False})
    cells = robjects.r('read.delim')(cells_csv, **{'row.names':1})
    genes = robjects.r('read.delim')(peaks_csv, **{'row.names':1})
    pd = robjects.r('new')("AnnotatedDataFrame", data=cells)
    fd = robjects.r('new')("AnnotatedDataFrame", data=genes)
    matrix = robjects.r('as.matrix')(expr_matrix)
    negbinomial_size = robjects.r('negbinomial.size')()
    HSMM = robjects.r('newCellDataSet')(matrix, phenoData=pd, featureData=fd, expressionFamily=negbinomial_size)
    HSMM = robjects.r('estimateSizeFactors')(HSMM)
    HSMM = robjects.r('reduceDimension')(HSMM, max_components=3, norm_method='none', num_dim=20, reduction_method='DDRTree')
    HSMM = robjects.r('orderCells')(HSMM)
    robjects.r('write.csv')(HSMM.slots['reducedDimS'], reduced_csv)
    phenoData = HSMM.slots['phenoData']
    robjects.r('write.csv')(phenoData.slots['data'], trajectory_csv)
    print('monocle_trajectory output files:')
    print(trajectory_csv)
    print(reduced_csv)
    return
#
#
######## generate pseudotime trajectory by calling paga
#
#
def paga_trajectory(project, cell_label='notes', npc=5):
    """
    project:        Path to the project folder.
    cell_label:     Color labels for cells, can be 'notes' or 'cluster', default='notes'.
    npc:            Number of principal components used to build trajectory, default=5.
    """
    import scanpy,anndata
    matrix_df = pandas.read_csv(project+'/matrix/Accesson_reads.csv', sep=',', index_col=0,
                                engine='c', na_filter=False, low_memory=False)
    normal = numpy.array([x/x.sum()*1000000 for x in matrix_df.values])
    matrix_df = pandas.DataFrame(normal, index=matrix_df.index.values, columns=matrix_df.columns.values)
    if cell_label=='notes':
        cells_csv = project+'/matrix/filtered_cells.csv'
    elif cell_label=='cluster':
        cells_csv = project+'/result/louvain_cluster_by_APEC.csv'
    else:
        print("Error: wrong <cell_label>, should be 'notes' or 'cluster' !")
        sys.exit()
    cells_df = pandas.read_csv(cells_csv, sep='\t', index_col=0)
    if cell_label=='cluster':
        cells_df[cell_label] = ['cluster_'+str(x) for x in cells_df[cell_label]]
    accessons = matrix_df.columns.values
    acces_df = pandas.DataFrame(accessons, index=['acc_'+str(x) for x in accessons], columns=['index'])
    adata = anndata.AnnData(matrix_df.values, obs=cells_df, var=acces_df)
    scanpy.pp.recipe_zheng17(adata, n_top_genes=len(adata.var), log=False)
    scanpy.tl.pca(adata, svd_solver='arpack')
    scanpy.pp.neighbors(adata, n_neighbors=10, n_pcs=npc)
    scanpy.tl.diffmap(adata)
    scanpy.pp.neighbors(adata, n_neighbors=10, use_rep='X_diffmap')
    scanpy.tl.paga(adata, groups=cell_label)
    fig0, ax0 = plt.subplots(1, 1, figsize=(10,10))
    scanpy.pl.paga(adata, color=cell_label, ax=ax0, show=False)
    outfig0 = project+'/figure/paga_skeleton_with_'+cell_label+'_label.pdf'
    fig0.savefig(outfig0, bbox_inches='tight')
    scanpy.tl.draw_graph(adata, init_pos='paga')
    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    scanpy.pl.draw_graph(adata, color=cell_label, legend_loc='on data', ax=ax, show=False)
    outfig = project+'/figure/paga_trajectory_with_'+cell_label+'_label.pdf'
    fig.savefig(outfig, bbox_inches='tight')
    print('paga_trajectory output files:')
    print(outfig0)
    print(outfig)
    return
#
#
######## generate gene score from nearby peaks
#
#
def get_tss_region(project, genome_gtf):
    genome_df = pandas.read_csv(genome_gtf, sep='\t', index_col=0)
    genes = list(set(genome_df['name2']))
    genes.sort()
    genome_df.index = genome_df['name']
    names, tss = [], []
    for symbol in genes:
        sub_df = genome_df.loc[genome_df['name2']==symbol]
        if len(sub_df.index.values)>=1:
            chrom = list(set(sub_df['chrom'].values))
            strand = list(set(sub_df['strand'].values))
            if len(chrom)==1:
                if strand[0]=='+':
                    starts = list(set(map(str, sub_df['txStart'].values)))
                    start = ','.join(starts)
                elif strand[0]=='-':
                    starts = list(set(map(str, sub_df['txEnd'].values)))
                    start = ','.join(starts)
                names.append(symbol)
                tss.append([chrom[0], start])
    tss = numpy.array(tss)
    tss_df = pandas.DataFrame(tss, index=names, columns=['chrom', 'tss'])
    tss_df.to_csv(project+'/peak/genes_tss_region.csv', sep='\t')
    return
#
#
def get_tss_peaks(project, distal=20000):
    peaks = [[x.split()[0], (int(x.split()[1])+int(x.split()[2]))/2]
             for x in open(project+'/peak/top_filtered_peaks.bed').readlines()]
    peaks_df = pandas.DataFrame(peaks, index=[str(x) for x in numpy.arange(0,len(peaks))],
                                columns=['chrom', 'center'])
    tss_df = pandas.read_csv(project+'/peak/genes_tss_region.csv', sep='\t', index_col=0)
    for gene in tss_df.index.values:
        chrom, tsses = tss_df.loc[gene, 'chrom'], tss_df.loc[gene, 'tss']
        tsses = list(map(int, tsses.split(',')))
        chr_peaks = peaks_df.loc[peaks_df['chrom']==chrom]
        proxim_peaks, distal_peaks = [], []
        for tss in tsses:
            peaks1 = chr_peaks.loc[abs(chr_peaks['center']-tss)<=2000].index.values
            peaks2 = chr_peaks.loc[abs(chr_peaks['center']-tss)<=distal].index.values
            proxim_peaks.extend(peaks1)
            distal_peaks.extend(peaks2)
        proxim_peaks = list(set(proxim_peaks))
        distal_peaks = list(set(distal_peaks)-set(proxim_peaks))
        if len(proxim_peaks)==0: proxim_peaks = ['NONE']
        if len(distal_peaks)==0: distal_peaks = ['NONE']
        proxim_peaks = ';'.join(proxim_peaks)
        tss_df.loc[gene, 'proximal'] = proxim_peaks
        distal_peaks = ';'.join(distal_peaks)
        tss_df.loc[gene, 'distal'] = distal_peaks
    tss_df.to_csv(project+'/peak/genes_TSS_peaks.csv', sep='\t')
    return
#
#
def get_score_from_peaks(project):
    tss_df = pandas.read_csv(project+'/peak/genes_TSS_peaks.csv', sep='\t', index_col=0)
    reads = scipy.sparse.csr_matrix(scipy.io.mmread(project+'/matrix/filtered_reads.mtx')).T
    cells_df = pandas.read_csv(project+'/matrix/filtered_cells.csv', sep='\t', index_col=0)
    all_peaks = numpy.arange(0, reads.shape[1])
    genes, score = [], []
    for igene,gene in enumerate(tss_df.index.values):
        distal = tss_df.loc[gene, 'distal'].split(';')
        proximal = tss_df.loc[gene, 'proximal'].split(';')
        if distal==['NONE']:
            distal = []
        else:
            distal = list(map(int, distal))
        if proximal==['NONE']:
            proximal = []
        else:
            proximal = list(map(int, proximal))
        distal = list(set(distal).union(set(proximal)))
        distal = list(set(distal).intersection(set(all_peaks)))
        if len(distal)>0:
            signal = reads[:, distal].A.mean(axis=1)
            genes.append(gene)
            score.append(signal)
    score = numpy.array(score)
    score_df = pandas.DataFrame(score, index=genes, columns=cells_df.index)
    score_per_cell = score.sum(axis=0)
    R_wave = [numpy.log(x*10000.0/score_per_cell[i]+1) for i,x in enumerate(score.T)]
    R_wave = numpy.array(R_wave)
    normal_df = pandas.DataFrame(R_wave, index=cells_df.index, columns=genes)
    normal_df.to_csv(project+'/matrix/genes_scored_by_TSS_peaks.csv', sep=',')
    return
#
#
def get_nearby_genes(project):
    gene_peaks = pandas.read_csv(project+'/peak/genes_TSS_peaks.csv', sep='\t', index_col=0)
    peak_genes = {}
    for gg in gene_peaks.index.values:
        gg_peaks = gene_peaks.loc[gg,'proximal'].split(';') + gene_peaks.loc[gg,'distal'].split(';')
        gg_peaks = list(set(gg_peaks) - set(['NONE']))
        for pp in gg_peaks:
            if 'peak'+pp not in peak_genes.keys():
                peak_genes['peak'+pp] = gg
            else:
                peak_genes['peak'+pp] = peak_genes['peak'+pp] + ';' + gg
    peak_genes_df = pandas.DataFrame.from_dict(peak_genes, orient='index', columns=['nearby_genes'])
    peak_genes_df.to_csv(project+'/peak/peaks_nearby_genes.csv', sep='\t')
    print('get_nearby_genes output files:')
    print(project+'/peak/peaks_nearby_genes.csv')
    return
#
#
def gene_score(project, genome_gtf='', distal=20000):
    """
    project:     Path to the project folder.
    genome_gtf:  Path to hg19_RefSeq_genes.gtf or mm10_RefSeq_genes.gtf in $reference folder.
    distal:      Genome distance for distal region, default=20000.
    """
    get_tss_region(project, genome_gtf)
    get_tss_peaks(project, distal=20000)
    get_score_from_peaks(project)
    print('gene_score output files:')
    print(project+'/peak/genes_TSS_peaks.csv')
    print(project+'/matrix/genes_scored_by_TSS_peaks.csv')
    return
#
#
######## generate motif-cell deviation matrix
#
#
def motif_search(info):
    motif, bgFile, threshold, motifFile, motifFasta, outFolder = info[0], info[1], info[2], info[3], info[4], info[5]
    motif_name = motif.split('-')[-1]
#    print(motif_name)
    fimoFile = outFolder + '/' + motif +'.fimo'
    subprocess.check_call('fimo --bgfile ' + bgFile + ' --text --thresh ' + threshold + ' --motif ' + motif_name
        + ' --no-qvalue --verbosity 1 ' + motifFile + ' ' + motifFasta + ' > ' + fimoFile, shell=True)
    bedFile = outFolder + '/' + motif +'.bed'
    with open(fimoFile) as fimo, open(bedFile, 'w') as bed:
        for line in fimo:
            if line[0]=='#':
                continue
            else:
                words = line.split('\t')
                chrom = words[1].split(':')[0]
                start = int(words[1].split(':')[1].split('-')[0]) + int(words[2])
                end = int(words[1].split(':')[1].split('-')[0]) + int(words[3])
                strand, score, pvalue, name = words[4], words[5], words[6], words[0]
                newLine = chrom+'\t'+str(start)+'\t'+str(end)+'\t'+strand+'\t'+score+'\t'+pvalue+'\t'+name
                bed.write(newLine+'\n')
    subprocess.check_call('gzip ' + bedFile, shell=True)
    subprocess.check_call('rm ' + fimoFile, shell=True)
    return
#
#
def batch_fimo(backgroudFile, threshold, motifFile, motifFasta, outFolder, n_processor):
    from multiprocessing import Pool
    motifs = []
    with open(motifFile) as mfile:
        for line in mfile:
            words = line.split(' ')
            if words[0] == 'MOTIF':
                info = words[2][:-1]
                info = info.replace('::', '-')
                info = info.replace(' ', '-')
                info = info.replace(':', '-')
                motifs.append(info+'-'+words[1])
    nMotif = len(motifs)
    info = numpy.vstack((motifs, [backgroudFile]*nMotif, [threshold]*nMotif, [motifFile]*nMotif,
                         [motifFasta]*nMotif, [outFolder]*nMotif)).T
    pool = Pool(n_processor)
    pool.map(motif_search, info)
    pool.close()
    pool.join()
    return
#
#
def score_peaks(peaks_file, motif_folder, out_file):
    peaks_info = numpy.loadtxt(peaks_file,'str',delimiter="\t")
    files = [motif_folder+'/'+x for x in os.listdir(motif_folder)]
    files.sort()
    outData = numpy.zeros([len(peaks_info),len(files)])
    headers = []
    for i in range(0,len(files)):
        file = files[i]
        fName = file.split('/')[-1].split('.bed')[0].split('.narrowPeak')[0]
        if os.path.getsize(file)>80:
            chipData = numpy.loadtxt(file, 'str')
        else:
            chipData = []
        headers.append(fName)
        if len(chipData)>0:
            chip = {}
            for line in chipData:
                chrom, start, end = line[0], int(line[1]), int(line[2])
                if chrom not in chip.keys():
                    chip[chrom] = [[start, end]]
                else:
                    chip[chrom].append([start, end])
            for j in range(0,len(peaks_info)):
                peakChr, peakStart, peakEnd = peaks_info[j,0], int(peaks_info[j,1]), int(peaks_info[j,2])
                try:
                    for site in chip[peakChr]:
                        if (site[0]>=peakStart) & (site[1]<=peakEnd):
                            outData[j,i]+=1
                            break
                except:
                    continue
    TFmotif_df = pandas.DataFrame(outData, index=['peak'+str(i) for i in numpy.arange(0,len(peaks_info))], columns=headers)
    TFmotif_df.to_csv(out_file, sep=',')
    return
#
#
def motif_matrix(project,
                 genome_fa='',   # =hg19_chr.fa or mm10_chr.fa
                 background='',   # =tier1_markov1.norc.txt
                 meme='',   # =JASPAR2018_CORE_vertebrates_redundant_pfms_meme.txt
                 pvalue=0.00005,   # P-value, default=0.00005
                 np=4   # Number of CPU cores, default=4
                 ):
    """
    project:     Path to the project folder.
    genome_fa:   Path to hg19_chr.fa or mm10_chr.fa in $reference folder.
    background:  Path to tier1_markov1.norc.txt in $reference folder.
    meme:        Path to JASPAR2018_CORE_vertebrates_redundant_pfms_meme.txt in $reference folder.
    pvalue:      P-value, default=0.00005.
    np:          Number of CPU cores used for parallel calculation, default=4.
    """
    top_peaks = project + '/peak/top_filtered_peaks.bed'
    trans_bias = project + '/peak/transposase_bias_filtered.bed'
    temp02_file = project + '/peak/temp02.bed'
    temp03_file = project + '/peak/temp03.bed'
    with open(top_peaks) as annotate_file, open(temp02_file, 'w') as temp02:
        for i, line in enumerate(annotate_file):
            words = line.split('\t')
            leave = words[0:3]
            temp02.write('\t'.join(leave)+'\n')
    subprocess.check_call('bedtools nuc -fi ' + genome_fa + ' -bed ' + temp02_file + ' > ' + temp03_file, shell=True)
    with open(temp03_file) as temp03, open(trans_bias, 'w') as bias:
        for i, line in enumerate(temp03):
            if i>0:
                words = line.split('\t')
                leave = words[0:3] + [words[4]]
                bias.write('\t'.join(leave)+'\n')
#
    motif_folder = project + '/matrix/motif'
    peaks_file = project + '/peak/top_filtered_peaks.bed'
    if os.path.exists(motif_folder): subprocess.check_call('rm -rf ' + motif_folder, shell=True)
    subprocess.check_call('mkdir ' + motif_folder, shell=True)
    motifFasta = project + '/matrix/motif.fasta'
    subprocess.check_call('bedtools getfasta -fi ' + genome_fa + ' -bed ' + peaks_file + ' -fo ' + motifFasta, shell=True)
    batch_fimo(background, pvalue, meme, motifFasta, motif_folder, np)
    TFmatrix_file = project + '/matrix/motif_filtered.csv'
    score_peaks(peaks_file, motif_folder, TFmatrix_file)
    print('motif_matrix output files:')
    print(TFmatrix_file)
    return
#
#
######## generate differential features
#
#
def group_cells(project, cell_label, target, vs):
    if cell_label=='notes':
        cells_csv = project+'/matrix/filtered_cells.csv'
    elif cell_label=='cluster':
        cells_csv = project+'/result/cluster_by_APEC.csv'
    else:
        print("Error: wrong <cell_label>, should be 'notes' or 'cluster' !")
        sys.exit()
    cells_df = pandas.read_csv(cells_csv, sep='\t', index_col=0)
    kCluster = target.split(',')
    if vs!='all': vsCluster = vs.split(',')
    if 'cluster' not in cells_df.columns.values:
        cells_df['cluster'] = cells_df['notes']
    else:
        kCluster = list(map(int, kCluster))
        if vs!='all': vsCluster = list(map(int, vsCluster))
    if vs=='all': vsCluster = list(set(cells_df['cluster'].values)-set(kCluster))
    cell_inCluster = cells_df.loc[cells_df['cluster'].isin(kCluster)].index.values
    cell_outCluster = cells_df.loc[cells_df['cluster'].isin(vsCluster)].index.values
    print('Cells in target cluster:', len(cell_inCluster))
    print('Cells in versus cluster:', len(cell_outCluster))
    return cell_inCluster, cell_outCluster
#
#
def differential_feature(project,
                         feature='accesson',   # ='accesson' or 'motif' or 'gene'
                         cell_label='cluster',   # ='cluster' or 'notes'
                         target='1',   # ='1'
                         vs='all',   # ='all' or '2' or '2,3,4'
                         pvalue=0.01,
                         log2_fold=1
                         ):
    """
    project:     Path to the project folder.
    feature:     Type of feature, can be 'accesson' or 'motif' or 'gene', default='accesson'.
                 If feature='accesson', run clustering.cluster_byAccesson() first;
                 if feature='motif', run clustering.cluster_byMotif() first;
                 if feature='gene', run generate.gene_score() first.
    cell_label:  Cell labels used for differential analysis, can be 'notes' or 'cluster', default='cluster'.
    target:      The target cluster that users search for differential features, default='1'.
                 if cell_label='cluster', target is one element in the 'cluster' column of cluster_by_APEC.csv;
                 if cell_label='notes', target is one element in the 'notes' column of filtered_cells.csv file.
    vs:          Versus which clusters, can be '2,3,4' or 'all', default='all' (means all the rest clusters).
    pvalue:      P-value for student-t test, default=0.01.
    log2_fold:   Cutoff for log2(fold_change), default=1.
    """
    if feature=='accesson':
        reads_file = project+'/matrix/Accesson_reads.csv'
    elif feature=='motif':
        reads_file = project+'/result/deviation_chromVAR.csv'
    elif feature=='gene':
#        if gene_value=='expression':
#            reads_file = project+'/matrix/gene_expression.csv'
#        elif gene_value=='score':
        reads_file = project+'/matrix/genes_scored_by_TSS_peaks.csv'
    else:
        print("Error: wrong <feature>, should be 'accesson' or 'motif' or 'gene' !")
        sys.exit()
    reads_df = pandas.read_csv(reads_file, sep=',', index_col=0,
                               engine='c', na_filter=False, low_memory=False)
    if feature=='motif': reads_df = reads_df.T
    cell_inCluster, cell_outCluster = group_cells(project, cell_label, target, vs)
    read_inCluster = reads_df.loc[cell_inCluster].values
    read_outCluster = reads_df.loc[cell_outCluster].values
    mean_in, mean_out = read_inCluster.mean(axis=0), read_outCluster.mean(axis=0)
    ttest, pvalues = scipy.stats.ttest_ind(read_inCluster, read_outCluster, equal_var=False)
    if feature=='motif':
        fold = mean_in - mean_out
    else:
        fold = numpy.log2((mean_in + 1e-4) / (mean_out + 1e-4))
    matrix = numpy.vstack((mean_in, mean_out, fold, pvalues)).T
    columns = ['mean_inCluster','mean_outCluster', 'log2_fold', 'p-value']
    matrix_df = pandas.DataFrame(matrix, index=reads_df.columns, columns=columns)
    matrix_df = matrix_df.loc[matrix_df['p-value'] <= float(pvalue)]
    matrix_df = matrix_df.loc[matrix_df['log2_fold'] >= float(log2_fold)]
    matrix_df = matrix_df.sort_values(by=['p-value'])
    nearby_csv = project+'/peak/peaks_nearby_genes.csv'
    if (feature=='accesson') & (os.path.exists(nearby_csv)):
        peaks_df = pandas.read_csv(project+'/matrix/Accesson_peaks.csv', sep='\t', index_col=0)
        nearby_genes_df = pandas.read_csv(nearby_csv, sep='\t', index_col=0)
        for accesson in matrix_df.index.values:
            peaks = [x for x in peaks_df.loc[peaks_df['group']==int(accesson)].index.values]
            peaks = list(set(peaks).intersection(set(nearby_genes_df.index.values)))
            if len(peaks)>0:
                genes = nearby_genes_df.loc[peaks, 'nearby_genes'].values
                genes = [str(x) for x in genes if (x!='NONE')&(type(x)==str)]
                genes = list(set(genes))
                genes.sort()
                genes = ';'.join(genes)
                matrix_df.loc[accesson, 'relevant_genes'] = genes
            else:
                matrix_df.loc[accesson, 'relevant_genes'] = 'NONE'
    out_csv = project+'/result/differential_'+feature+'_of_cluster_'+target+'_vs_'+'_'.join(vs.split(','))+'.csv'
    matrix_df.to_csv(out_csv, sep='\t')
    print('differential_feature output files:')
    print(out_csv)
#    print('Differential '+feature+' for cluster '+target+' VS '+vs+':')
#    print(feature+'\t'+'\t'.join(matrix_df.columns.values))
#    for x in matrix_df.index.values: print(str(x)+'\t'+'\t'.join(list(map(str, matrix_df.loc[x].values))))
    return
#
#
def peaks_of_accesson(project, accesson=1):
    """
    project:     Path to the project folder.
    accesson:    Name/number of accesson that users want to get the peak list.
    """
    peaks_df = pandas.read_csv(project+'/matrix/Accesson_peaks.csv', sep='\t', index_col=0)
    peaks_bed = numpy.array(open(project+'/peak/top_filtered_peaks.bed').readlines())
    peaks = peaks_df.loc[peaks_df['group']==accesson].index.values
    peaks_index = [int(x[4:]) for x in peaks]
    out_bed = project+'/result/accesson_'+str(accesson)+'_peaks.bed'
    with open(out_bed, 'w') as output:
        for line in peaks_bed[peaks_index]:
            words = line.split()
            output.write('\t'.join(words)+'\n')
    print('peaks_of_accesson output files:')
    print(out_bed)
    return
#
#
######## generate potential super enchancer
#
#
def super_enhancer(project, super_range=1000000, p_cutoff=0.01):
    """
    project:         Path to the project folder.
    super_range:    Genome range to search for super enhancer, default=1000000.
    p_cutoff:       Cutoff of p-value, default=0.01.
    """
    peaks = numpy.array([x.split()[:3] for x in open(project+'/peak/top_filtered_peaks.bed').readlines()])
    peaks_df = pandas.DataFrame(peaks[:,0], index=['peak'+str(i) for i in range(0, len(peaks))], columns=['chrom'])
    peaks_df['start'] = list(map(int, peaks[:,1]))
    peaks_df['end'] = list(map(int, peaks[:,2]))
    accesson_df = pandas.read_csv(project+'/matrix/Accesson_peaks.csv', sep='\t', index_col=0)
    accessons = list(set(accesson_df['group'].values))
    nearby_peaks = {}
    for peak in peaks_df.index.values:
        chrom, start, end = peaks_df.loc[peak, 'chrom'], peaks_df.loc[peak, 'start'], peaks_df.loc[peak, 'end']
        position1, position2 = start-super_range, end+super_range
        same_chrom_df = peaks_df.loc[peaks_df['chrom']==chrom]
        in_range_df = same_chrom_df.loc[(same_chrom_df['end']>position1)&(same_chrom_df['start']<position2)]
        nearby_peaks[peak] = in_range_df.index.values
    all_supers = {}
    for access in accessons:
        acc_peaks = accesson_df.loc[accesson_df['group']==access].index.values
        for peak in acc_peaks:
            nearby = nearby_peaks[peak]
            overlap = list(set(nearby).intersection(set(acc_peaks)))
            chrom = peaks_df.loc[overlap[0], 'chrom']
            start = peaks_df.loc[overlap, 'start'].min()
            end = peaks_df.loc[overlap, 'end'].max()
            position = chrom+':'+str(start)+'-'+str(end)
            percent = len(overlap)/float(len(nearby))
            overlap_peaks = '-'.join(overlap)
            if overlap_peaks not in all_supers:
                all_supers[overlap_peaks] = [position, percent, len(overlap)]
            elif all_supers[overlap_peaks][1]<percent:
                all_supers[overlap_peaks] = [position, percent, len(overlap)]
    matrix_df = pandas.DataFrame.from_dict(all_supers, orient='index', columns=['position', 'percent', 'n_peaks_in_accesson'])
    all_percents = matrix_df['percent']
    print(type(all_percents[0]))
    pvalues = []
    for percent in all_percents:
        higher = numpy.where(all_percents>=percent)[0]
        pvalues.append(len(higher)/float(len(all_percents)))
    matrix_df['p-value'] = pvalues
    matrix_df = matrix_df.sort_values(by=['p-value'])
    matrix_df = matrix_df.loc[matrix_df['p-value']<p_cutoff]
    matrix_df = matrix_df.loc[matrix_df['n_peaks_in_accesson']>=5]
    matrix_df.index = [str(x) for x in range(1, len(matrix_df.index)+1)]
    matrix_df.to_csv(project+'/result/potential_super_enhancer.csv', sep='\t')
    return
#
#
