dependencies

bowtie2 v2.3.4.3
biopython v1.76
RNAfold 2.4.11
dna_mathews2004.par in root folder from https://github.com/ViennaRNA/ViennaRNA/tree/master/misc

Instructions
Index reference with bowtie2-build. Place the fasta file and index in the REFRENCE dir. Make sure to use the entire reference name (e.g., gencode.v29.transcripts.fa and not gencode.v29.transcripts for the bt2_index_base).
Create a fasta file where the name EXACTLY matches the name in the reference file. The script 0_XYZ.py can pull out these sequences and name them for you. This is important to avoid treating self-matches as potential offtarget hybridization events. Ensure capitalization is exactly the same since it's string matching
Run 1_XYZ.py to design probes and predict off target hybridization. You will need to manually change the number of threads in the script to what you want to use. Default if 4. Input fasta file with targets with '-in' and reference index as '-ref'
Edit the adapter file to specify what adapter sequencing you want to use for each target (must be 23 nt is length). All targets can have the same adapter sequencing, but it's good to start with multicolour FISH using different adapters as confirmation. It's tab-deliniated with target name on left and sequence on right.
If you wish, you can specify the barcode to use for each target. If you do not manually add this, a random barcode will be chosen if the target does not exist in the barcode file. 
Run 2_XYZ.py. This will produce 3 files in the probe dir.
	1. *_#off_PostBowtie.fasta - Used by RNAfold to predict secondary structure
	2. *_#off_FinalTargets.fasta - The entire hybridization sequence without probe structure
	3. *_#off_FinalProbes.fasta - Pick e.g., top 10 and synthesize. You may synthesize with a 5' phosphate or add it with T4 PNK. Either way works, but SplintR requires this 5' phosphate. 
2_XYZ.py also produces a summary file with barcode identity and number of probes found