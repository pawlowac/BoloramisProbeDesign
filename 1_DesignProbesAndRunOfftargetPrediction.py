from Bio import SeqIO
from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio.SeqUtils import MeltingTemp as mt
from io import StringIO
import io
import subprocess
import os
import sys
import random
import time
import argparse

THREADS = '4'

def main(target_file, reference_database):
	start_time = time.time()

	# make sure cmdline arg filepaths exist
	try:
		if not os.path.exists(target_file):
			raise FileNotFoundError("infile not found: {}"
									"".format(target_file))
		if not os.path.exists(reference_database):
			raise FileNotFoundError("reference file not found: {}"
									"".format(reference_database))
	except FileNotFoundError as e:
		raise e

	targets = SeqIO.parse(target_file, 'fasta')
	reference_file = SeqIO.parse('{}'.format(reference_database), 'fasta')

	# Create a folder named 'part1' within the current working directory, this
	# will be where all probes are saved and the sub_sam files.
	working_dir = os.getcwd()
	if os.path.exists(os.path.dirname('{}/part1/'.format(working_dir))):
		pass
	else:
		os.makedirs(os.path.dirname('{}/part1/'.format(working_dir)))

	# Loading in the gene names from the reference database. This will throw
	# error messages if the gene name is not present (e.g., eGFP) but is also a
	# good measure in case the gene name is not exactly the same as the
	# reference database (e.g., Cd8 vs. CD8).
	database_gene_list = set()
	for seq in reference_file:
		gene_name = (seq.name)
		gene_name = gene_name.split('|')[5]
		database_gene_list.add(gene_name)

	for target in targets:
		if str(target.name).count('-') == 0:
			target_name = str(target.name)
		elif str(target.name).count('-') == 1:
			target_name = str(target.name).split('-')[0]
		elif str(target.name).count('-') == 2:
			z = str(target.name).split('-')
			target_name = z[0] + '-' + z[1]
		print('Now predicting probes for {}'.format(target_name))
		# Nothing happens if target not in reference, just throws a warning.
		# Good for trouble shooting if gene names are not an exact match
		# (e.g., Cd8 vs. CD8)
		if target_name not in database_gene_list:
			raise ValueError('Sequence {} from infile is not found in the '
							 'reference database. This should not happen '
							 'if using the output from Script 0.'
							 ''.format(target_name))

		seq = target.seq
		sub_seq_list = []

		# iterate over all 25 bp windows, avoid homotetramers, ensure proper
		# junction use, and avoid excessively low or high GC use
		for n in range(0, len(seq)-24):
			sub_seq = str(seq[n:n+25].reverse_complement()).upper()

			# look for TG junctions
			if GC(sub_seq) > 50 and GC(sub_seq) < 90:
				if 'GGGG' not in sub_seq:
					if 'CCCC' not in sub_seq:
						comparison = False
						if sub_seq[7] == 'T' and sub_seq[6] == 'C':
							comparison = True
						elif sub_seq[7] == 'A' and sub_seq[6] == 'T':
							comparison = True
						elif sub_seq[7] == 'T' and sub_seq[6] == 'T':
							comparison = True
						elif sub_seq[7] == 'A' and sub_seq[6] == 'G':
							comparison = True
						elif sub_seq[7] == 'A' and sub_seq[6] == 'A':
							comparison = True
						elif sub_seq[7] == 'T' and sub_seq[6] == 'A':
							comparison = True
						elif sub_seq[7] == 'A' and sub_seq[6] == 'C':
							comparison = True
						elif sub_seq[7] == 'T' and sub_seq[6] == 'G':
							comparison = True
						elif sub_seq[7] == 'C' and sub_seq[6] == 'T':
							comparison = True

						# if any of the elifs were true, append to sub_seq_list
						if comparison:
							probe_name = '{}_{}-{}'.format(target_name, n, n+25)
							sub_seq_list.append(
								{'Name': probe_name,
								 'Sequence': sub_seq,
								 'Tm': mt.Tm_GC(sub_seq, Na=300)})

		temp_probe_list = open('./part1/{}_AllProbes.fasta'.format(target_name),
							   'w')
		pre_triage_probe_dict = {}
		for hit in sub_seq_list:
			temp_probe_list.write('>{}_{}\n{}\n'.format(hit['Name'],
								  int(hit['Tm']), hit['Sequence']))
			pre_triage_probe_dict['{}_{}'.format(hit['Name'],
								  int(hit['Tm']))] = hit['Sequence']
		print(len(pre_triage_probe_dict.keys()))
		temp_probe_list.close()

		try:
			os.remove('only_bowtie.sam')
		except OSError:
			pass
		pruned_bowtie_results = open('./part1/{}.sub_sam'.format(target_name),
									 'w')
		buildcmd = ['bowtie2', '--reorder', '--no-sq', '--nofw',
					'-p', '{}'.format(THREADS),
					'-D', '20',
					'-R', '3',
					'-N', '1',
					'-L', '9',
					'-i', 'L,0,0.80',
					'--gbar', '13',
					'-k', '50000',
					'-x', '{}'.format(reference_database),
					'-f', './part1/{}_AllProbes.fasta'.format(target_name),
					'-S', 'only_bowtie.sam',
					'--score-min', 'C,-42,0']
					#'--rdg', '5,10',
					#'--rfg', '5,10']
		subprocess.call(buildcmd)

		# parse bowtie2 output
		bowtie_output = open('only_bowtie.sam', 'r')

		for result in bowtie_output:
			if result[0] != '@':
				result = result.split('\t')
				probe_name = result[0]
				hit_name = result[2]
				hit_gene_name = hit_name.split('|')[5]
				for detail in result:
					# search for edit difference between target and probe
					if 'NM:i:' in detail:
						mismatches = int(detail.replace('NM:i:',''))
				if mismatches <= 6:
					pruned_bowtie_results.write('{}\t{}\t{}\t{}\n'
												''.format(probe_name,
														  hit_gene_name,
														  hit_name,
														  mismatches))
		pruned_bowtie_results.close()
		bowtie_output.close()

	targets.close()
	reference_file.close()

	print("--- {} seconds ---".format(time.time() - start_time))


if __name__ == '__main__':
	# set up argument parsing
	parser = argparse.ArgumentParser()

	# infile can't be imported as a file because it is opened in main() w/ SeqIO
	parser.add_argument('-i','--infile', nargs=1, required=True, type=str,
						help='Location of file created using '
							 '0_PullTargetsFromReference.py.')
	# ref can't be imported as a file because it is opened in main() w/ SeqIO
	parser.add_argument('-r', '--ref', nargs=1, required=True, type=str,
						help='Location of the reference database used. This '
							 'points to both the fasta file '
							 '(e.g. gencode.v29.transcripts.fa) and the '
							 'bowtie2 index '
							 '(gencode.v29.transcripts.fa...bt2).')

	# parse args
	args = parser.parse_args()

	# run main script
	main(args.infile[0], args.ref[0])
