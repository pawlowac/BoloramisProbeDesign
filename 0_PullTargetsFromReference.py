from Bio import SeqIO
import argparse
import os


def main(target_file, result_file, reference_fp):
    """
        Read the target file, compare them to the reference file, and save
    results in the result file.
    """
    # make sure cmdline arg filepaths exist
    try:
        if not os.path.exists(reference_fp):
            raise FileNotFoundError("No such file or directory: {}"
                                    "".format(reference_fp))
    except FileNotFoundError as e:
        raise e

    reference_seqs = SeqIO.parse(reference_fp, 'fasta')

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
                        help='Location of file with all targets, with 1 target '
                             'per line. Name must be an isoform found in '
                             'Gencode database.')
    # outfile is writable file
    parser.add_argument('-o', '--outfile', nargs=1, required=True,
                        type=argparse.FileType('w'),
                        help='Location to save the fasta file to be used for '
                             'input to '
                             '1_DesignProbesAndRunOfftargetPrediction.py.')
    # ref can't be imported as a file because it is opened in main() with SeqIO
    parser.add_argument('-r', '--ref', nargs=1, required=True, type=str,
                        help='Location of the file containing the Gencode '
                             'database for the organism you are targetting in '
                             'fasta format.')

    # parse args
    args = parser.parse_args()

    # run main script
    main(args.infile[0], args.outfile[0], args.ref[0])

    # close imported files
    args.infile[0].close()
    args.outfile[0].close()

