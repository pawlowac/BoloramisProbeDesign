import argparse

def main(mm):
    print("mm:\n{}".format(mm))

if __name__ == '__main__':
    # set up argument parsing
    parser = argparse.ArgumentParser()

    # mismatches allowed
    parser.add_argument("mm", metavar="MM", nargs='?', default=6, type=int,
                        help='Number of mismatches allowed in offtarget '
                             'alignments (default: 6).')

    # parse args
    args = parser.parse_args()

    # run main script
    main(args.mm)
