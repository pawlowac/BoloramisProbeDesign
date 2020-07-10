from Bio import SeqIO
import argparse

def main(target_file, result_file, reference_fp):
    """
        Read the target file, compare them to the reference file, and save
    results in the result file.
    """

    # result_file = open('jenny_02182020.fasta', 'w')
    reference_seqs = SeqIO.parse(reference_fp, 'fasta')
    # reference_seqs = SeqIO.parse('./REFERENCE/gencode.v29.transcripts.fa',
    #                              'fasta')
    # target_file = open('jenny_02182020.txt', 'r')

    targets = []
    # Unpack target_file into a list
    for line in target_file:
        line = line.strip()
        targets.append(line)

    # compare targets to reference file
    for reference_seq in reference_seqs:
        name = reference_seq.name
        header = name.split('|')
        transcript_id = name.split('|')[4]
        if transcript_id in targets:
            # for data in header:
            #    if 'CDS:' in data:
            #        cds_region = data
            #        cds_start = int(cds_region.replace('CDS:','').split('-')[0])-1
            #        cds_stop = int(cds_region.replace('CDS:','').split('-')[1])
            result_file.write('>{}\n{}\n'.format(transcript_id,
                                                 reference_seq.seq))

    # close ref file
    reference_seqs.close()


if __name__ == '__main__':
    # set up argument parsing
    parser = argparse.ArgumentParser()

    # infile is read-only file
    parser.add_argument('-i','--infile', nargs=1, required=True,
                        type=argparse.FileType('r'),
                        help='Location of .fasta file containing a list of '
                        'probes to be compared to the reference file.')
    # outfile is writable file
    parser.add_argument('-o', '--outfile', nargs=1, required=True,
                        type=argparse.FileType('w'),
                        help='Location of text file to save results.')
    # ref can't be imported as a file because it is opened in main() with SeqIO
    parser.add_argument('-r', '--ref', nargs=1, required=True, type=str,
                        help='Location of reference .fa file to be compared '
                             'to the infile.')

    # parse args
    args = parser.parse_args()

    # run main script
    main(args.infile[0], args.outfile[0], args.ref[0])

    # close imported files
    infile.close()
    outfile.close()
