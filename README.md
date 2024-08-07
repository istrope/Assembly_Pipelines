FLYE PIPELINE: </br>
Setup and Initialization:

Define paths to necessary tools and databases.
Create output directories.
Quality Control with FastQC:

Runs FastQC to assess the quality of raw sequencing reads.
Trimming with Trimmomatic:

Uses Trimmomatic to remove adapter sequences and low-quality bases from the reads.
Assembly with SPAdes:

Executes SPAdes to assemble the trimmed reads into contigs.
Contig Filtering:

Filters out contigs below a certain length threshold.
Quality Assessment with QUAST:

Uses QUAST to evaluate the quality of the assembly.
Annotation with Prokka:

Annotates the assembled genome to identify genes and other features.
MLST and Abricate:

MLST (Multi-Locus Sequence Typing) to identify sequence types.
Abricate to screen the assembly for resistance genes, plasmids, and other features.
Time Tracking:

Measures and reports the total time taken for the entire pipeline.
## Input

Required input are: 
(1) out-directory (**outdir**) 
(2) ONT long-reads (either gzip or non-compressed files will work)
(3) Interleaved paired-end short-reads (either gzip or non-compressed files will work)
(4) **genome_size** estimated genome size based on previous knowledge of species (+/- 1 Mb genome size estimate is fine for flye k-mer selection)

**Note that paired-end reads MUST be interleaved for racon to work. You can interleave short-read data using the `bbmap` tool `reformat.sh`. For racon to work properly, make sure there are underscores in lieu of white-space in headers of short-read fastq files by using the `underscore=t` option in `reformat.sh`. Example command-line for reformat.sh is as follows:**
```
$reformat.sh in1=PE_read1.fastq.gz in2=PE_read2.fastq.gz out=PEIL.fastq.gz underscore=t
```

## Usage

Usage with Flye assembler:
```
$python3 flye_pipeline.py -t 2 -s sample_name -o outdir -pe interleaved_pe_reads.fastq.gz -l long_reads.fastq.gz --genome_size 5.3m -d dnaA_file.fasta
```

Usage for error correction of previously assembled genome:
```
$python3 flye_pipeline.py -t 2 -s sample_name -o outdir -x -c assembly.fasta -pe interleaved_pe_reads.fastq.gz -l long_reads.fastq.gz -d dnaA_file.fasta
```

## Output

Final assembly can be found in `outdir_name/shortRead_polish_results/` and will be named **SAMPLENAME_final.fasta**

## Usage tips

(1) Note that any database of genes of interest to orient contigs can be used for the purposes of orienting any linear or circular DNA structure when using the `-d` paramter in pipeline. For example, if assembling *K. pneumoniae* genomes, one can use the manually curated, database of commonly observed F-type replication initiation protein genes found in plasmids as well as the *dnaA* gene for *K. pneumoniae* in the db directory with the file name **dnaA_and_plasmid_startSites.fasta**. 

If one wants to use `--meta` and `--plasmid` options for their flye assemblies, please use the `-mp` argument in the pipeline.


# SPADES PIPELINE:
Flye is a de novo assembler for long reads (e.g., PacBio or Oxford Nanopore sequencing). Here’s a step-by-step explanation of the Flye pipeline:

Setup and Initialization:

Define paths to necessary tools.
Create output directories.
Assembly with Flye:

Runs Flye to assemble the long reads into contigs.
Circularization with Circlator:

Uses Circlator to circularize contigs and fix start positions.
Polishing with Medaka:

Uses Medaka to polish the assembly, improving accuracy by correcting errors based on the long reads.
Polishing with BWA and Racon:

Uses BWA to align short reads to the assembly and Racon to correct the assembly based on these alignments.
Additional Polishing and Cleanup:

Repeats BWA and Racon polishing steps multiple times to improve assembly accuracy.
Cleans up and fixes any remaining issues, ensuring high-quality final assembly.
Summary
SPAdes Pipeline:

Tailored for short reads.
Includes steps for quality control, trimming, assembly, and annotation.
Uses a variety of tools to ensure a high-quality final assembly.
Flye Pipeline:

Tailored for long reads.
Focuses on assembling long reads, circularizing contigs, and polishing the assembly to correct errors.
Utilizes specialized tools for handling long-read data and ensuring high accuracy. 
