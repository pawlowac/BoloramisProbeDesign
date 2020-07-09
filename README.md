**Purpose**

Barcoded Oligonucleotides Ligated On RNA Amplified for Multiplexed and parallel In-Situ analysis (BOLORAMIS) is a reverse-transcription (RT)-free method for spatially-resolved,
targeted, in situ RNA identification of single or multiple targets


**Dependencies**

python3.7.6
bowtie2 v2.3.4.3
biopython v1.76
RNAfold 2.4.11
dna_mathews2004.par - place in root folder from https://github.com/ViennaRNA/ViennaRNA/tree/master/misc

**Instructions**
- Index reference with bowtie2-build. Place the fasta file and index in the REFRENCE dir. Make sure to use the entire reference name (e.g., gencode.v29.transcripts.fa and not gencode.v29.transcripts for the bt2_index_base).
- Run script 0, 1, and 2


**Instructions for 0_PullTargetsFromReference.py**
- Target Input -> File with all targets, with 1 target per line. Name must be an isoform found in Gencode database.
	
	For example;\
		>ENST00000321358.11|ENSG00000065978.18|OTTHUMG00000007523.6|OTTHUMT00000019786.2|YBX1-201|YBX1|1514|protein_coding|\
		AGTTCGA...\
		\
		Isoform target - YBX1-201
		CDS - YBX1
		\
		Therefore, if you want to target YBX1 via isoform 201, you would have YBX1-201 in your Target Input file.
	
	Note:\
		Targets are pulled using string matching, so must be YBX1-201 and not Ybx1-201.\
		
- Reference input -> The Gencode database for the organism you are targetting in fasta format
	
	For example;\
		gencode.v29.transcripts.fa
		
- Output -> Fasta file ready for input to 1_DesignProbesAndRunOfftargetPrediction.py

**Instructions for 1_DesignProbesAndRunOfftargetPrediction.py**

- You will need to manually change the number of threads in the script to what you want to use. Default is 4.
- Input -> Target file created using 0_PullTargetsFromReference.py.
	
	- Can manually make file in fasta format with CDS name only in the header.\
	>YBX1\
	AGTTCGA...\

- Reference input -> The reference database used. This points to both the fasta file (e.g., gencode.v29.transcripts.fa) and the bowtie2 index (gencode.v29.transcripts.fa...bt2), which is why the bowtie2 index must contain the fasta file name as the prefix. 
- Output -> All possible probes that pass the requiurements of SplintR substrate specificity and do not contain G or C tetrapolymers, and predicted hybiridization events in the reference database. The alignments are reported in a reduced file with 6 or less mismatches. More than 6 are filtered out and assumed to not be targets for hybridization.
	
	For example;\
		./part1/YBX1_AllProbes.fasta - All probes found\
		./part1YBX1.sub_sam - Reduced output from bowtie2 for offtarget prediction\
	
	Notes;\
		Offtarget prediction (script 1) and probe design (script 2) are not completing in 1 step because offtarget prediction is CPU intensive and can take some time to 		complete with large number of targets. Sometimes you may find that with the default stringency (6) you may not find enough (or any) probes and therefore may wish 		to reduce stringency. In this case you can just run script 2 with different mismatch settings to find a number that works for you without recomputing the 			offtarget alignments.\

**Instructions for 2_AssembleProbes.py**
- Automatically parses the files present in ./part1/ and designs probes
- Can choose mismatches allowed in offtarget alignments using the -mm flag.
- Adapter input -> Input file adapters.txt that contains a target-adapter pair separated by a tab. Adapters must be 23 nt long. You use this sequence for sequencing the 		adjacent barcode, or as a landing pad for fluorescent oligos if using FISH to confirm libraries or low number of targets.
	- All targets can have the same adapter sequencing, but it's good to start with multicolour FISH using different adapters as confirmation.
	
	- For example;\
		YBX1	ATAGCGATCTGCCCGGGCCTTGA

- Barcode Input ->  Input file barcodes.txt that contains a barcode-target pair separated by a tab. Barcodes must be 8 nt long and the entire 8 nt will be appended to the 3' 		end of the adapter sequence, and the last 4 nt will be appended to the 5' end of the adapter. This allows flexibility to sequence 8 nt in a row 5' to 3', or to sequence 	the first 4 nt from 5' to 3', then the last 4 nt in reverse order from 3' to 5' of the adapter.
	- If you wish, you can specify the barcode to use for each target. If you do not manually add this, a random barcode will be chosen if the target does not exist in the 	barcode file. 
	
	- For example;/
		cggaagaa	YBX1

- Outputs -> in ./probes/ dir
	
	1. *_#off_PostBowtie.fasta - Used by RNAfold to predict secondary structure
	2. *_#off_FinalTargets.fasta - The entire hybridization sequence without probe structure
	3. *_#off_FinalProbes.fasta - Pick e.g., top 10 and synthesize. You may synthesize with a 5' phosphate or add it with T4 PNK. Either way works, but SplintR requires 		this 5' phosphate. 

- Summary output - A summary file with barcode identity and number of probes found as summary_file_#off.txt in the root dir

	
	
**Citation**

All errors are the fault of Andrew Pawlowski

<Add citation>
