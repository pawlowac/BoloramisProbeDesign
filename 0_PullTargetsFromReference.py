from Bio import SeqIO
result_file = open('jenny_02182020.fasta', 'w')
reference_seqs = SeqIO.parse('./REFERENCE/gencode.v29.transcripts.fa', 'fasta')

target_file = open('jenny_02182020.txt', 'r')
targets = []
for line in target_file:
	line = line.strip()
	targets.append(line)
	
for reference_seq in reference_seqs:
	name = reference_seq.name
	header = name.split('|')
	transcript_id = name.split('|')[4]
	if transcript_id in targets:
		#for data in header:
		#	if 'CDS:' in data:
		#		cds_region = data
		#		cds_start = int(cds_region.replace('CDS:','').split('-')[0])-1
		#		cds_stop = int(cds_region.replace('CDS:','').split('-')[1])
		result_file.write('>{}\n{}\n'.format(transcript_id, reference_seq.seq))
	