import os
import shutil
import argparse
from datetime import datetime
import multiprocessing as mp
from BioSAK.global_functions import force_create_folder
from BioSAK.global_functions import sep_path_basename_ext


download_GenBank_genome_parser_usage = '''
================================== dwnld_GenBank_genome example commands ==================================

# Usage:
# 1. Go to https://www.ncbi.nlm.nih.gov/genome/browse#!/prokaryotes/refseq_category:reference
# 2. Search genomes you want to download (e.g. prokaryotes, proteobacteria, psychrobacter)
# 3. Click "Download" on the right side
# 4. provide the downloaded csv file with '-csv'

# Download all genomes in file prokaryotes.csv
BioSAK dwnld_GenBank_genome -csv prokaryotes.csv -fna
BioSAK dwnld_GenBank_genome -csv prokaryotes.csv -fna -faa -gbff

===========================================================================================================
'''


def genome_download_worker(argument_list):

    genome_record_split =       argument_list[0]
    downloaded_genome_folder =  argument_list[1]
    get_fna =                   argument_list[2]
    get_faa =                   argument_list[3]
    get_gbff =                   argument_list[4]
    with_name =                  argument_list[5]

    genome_name = genome_record_split[0][1:-1]
    genome_name_no_space = '_'.join(genome_name.split(' '))
    GenBank_FTP = genome_record_split[-2][1:-1]
    GenBank_FTP_id = GenBank_FTP.strip().split('/')[-1]
    assembly_id = genome_record_split[5]

    # prepare cmds
    wget_fna_cmd = 'wget %s/%s_genomic.fna.gz -P %s -q' % (GenBank_FTP, GenBank_FTP_id, downloaded_genome_folder)
    wget_faa_cmd = 'wget %s/%s_protein.faa.gz -P %s -q' % (GenBank_FTP, GenBank_FTP_id, downloaded_genome_folder)
    wget_gbk_cmd = 'wget %s/%s_genomic.gbff.gz -P %s -q' % (GenBank_FTP, GenBank_FTP_id, downloaded_genome_folder)

    # download, decompress and rename
    if get_fna is True:
        os.system(wget_fna_cmd)
        print(wget_fna_cmd)
        os.system('gunzip %s/%s_genomic.fna.gz' % (downloaded_genome_folder, GenBank_FTP_id))
        if with_name is False:
            os.system('mv %s/%s_genomic.fna %s/%s.fna' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id))
        else:
            os.system('mv %s/%s_genomic.fna %s/%s_%s.fna' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id, genome_name_no_space))

    if get_faa is True:
        os.system(wget_faa_cmd)
        os.system('gunzip %s/%s_protein.faa.gz' % (downloaded_genome_folder, GenBank_FTP_id))
        if with_name is False:
            os.system('mv %s/%s_protein.faa %s/%s.faa' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id))
        else:
            os.system('mv %s/%s_protein.faa %s/%s_%s.faa' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id, genome_name_no_space))

    if get_gbff is True:
        os.system(wget_gbk_cmd)
        os.system('gunzip %s/%s_genomic.gbff.gz' % (downloaded_genome_folder, GenBank_FTP_id))
        if with_name is False:
            os.system('mv %s/%s_genomic.gbff %s/%s.gbff' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id))
        else:
            os.system('mv %s/%s_genomic.gbff %s/%s_%s.gbff' % (downloaded_genome_folder, GenBank_FTP_id, downloaded_genome_folder, assembly_id, genome_name_no_space))


def download_GenBank_genome(args):

    csv_file =      args['csv']
    get_fna =       args['fna']
    get_faa =       args['faa']
    get_gbff =      args['gbff']
    with_name =     args['name']
    num_threads =   args['t']

    time_format = '[%Y-%m-%d %H:%M:%S] '

    in_file_path, in_file_basename, in_file_extension = sep_path_basename_ext(csv_file)
    downloaded_genome_folder = '%s_genomes' % in_file_basename
    force_create_folder(downloaded_genome_folder)

    # report
    print(datetime.now().strftime(time_format) + 'Downloading genomes with %s cores' % (num_threads))

    # download genome with multiprocessing
    list_for_multiple_arguments_download_worker = []
    for genome_record in open(csv_file):

        if not genome_record.startswith('#Organism Name'):
            genome_record_split = genome_record.strip().split(',')
            list_for_multiple_arguments_download_worker.append([genome_record_split, downloaded_genome_folder, get_fna, get_faa, get_gbff, with_name])

    # run COG annotaion files with multiprocessing
    pool = mp.Pool(processes=num_threads)
    pool.map(genome_download_worker, list_for_multiple_arguments_download_worker)
    pool.close()
    pool.join()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-csv',  required=True,                       help='csv file from NCBI genome_browse')
    parser.add_argument('-fna',  required=False, action="store_true", help='download gna file')
    parser.add_argument('-faa',  required=False, action="store_true", help='download faa file')
    parser.add_argument('-gbff', required=False, action="store_true", help='download gbff file')
    parser.add_argument('-name', required=False, action="store_true", help='include genome name in the downloaded files')
    parser.add_argument('-t',    required=False, default=1, type=int, help='number of threads')

    args = vars(parser.parse_args())

    download_GenBank_genome(args)
