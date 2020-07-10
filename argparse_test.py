import argparse

def main(infile, outfile, ref):
    print("infile:\n{}".format(infile.readline()))
    outfile.write("sample out")
    print("reference:\n{}".format(ref))

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
