#!/usr/bin/env python3

import os
import subprocess
import argparse
import time

def create_directory(outdir):
    """Function to create the output directory"""
    if os.path.exists(outdir):
        raise Exception(f"Directory {outdir} already exists")
    os.makedirs(outdir, exist_ok=True)

def run_command(command):
    """Run a command using subprocess.run and handle exceptions"""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{' '.join(command)}' failed with error: {e}")
        raise

def flye_command(flye_path, long_reads, outdir, threads):
    command = [flye_path, '--nano-raw', long_reads, '--out-dir', outdir, '--threads', str(threads)]
    run_command(command)

def circlator_command(circlator_path, dnaA_file, infile, sample_name, command_type):
    command = [circlator_path, command_type, '--genes', dnaA_file, infile, sample_name, '--verbose']
    run_command(command)

def medaka_command(medaka_path, long_reads, contigs, outdir, threads):
    command = [
        medaka_path, '-i', long_reads, '-d', contigs,
        '-o', os.path.join(outdir, 'medaka_results'), '-m', 'r941_min_high_g360', '-t', str(threads)
    ]
    run_command(command)

def bwa_command(bwa_path, assembly_reference, pe_reads, outdir, threads, racon_polish_number):
    print("Indexing assembly reference for BWA alignment")
    run_command([bwa_path, 'index', assembly_reference])

    print("BWA-MEM alignment with assembly reference and paired-end short-reads")
    sam_output = os.path.join(outdir, f'align_{racon_polish_number}.sam')
    command = [bwa_path, 'mem', '-t', str(threads), '-o', sam_output, assembly_reference, pe_reads]
    run_command(command)

def racon_command(racon_path, pe_reads, overlaps, target_sequences, outdir, sample_name, threads, racon_polish_number):
    racon_output = os.path.join(outdir, f'{sample_name}_racon{racon_polish_number}.fasta')
    command = [racon_path, '-t', str(threads), pe_reads, overlaps, target_sequences, '>', racon_output]
    run_command(command)

def run_pipeline(args):
    start = time.time()

    create_directory(args.outdir)

    # Flye assembly
    print("Running Flye assembly...")
    flye_command(args.flye_path, args.long_reads, args.outdir, args.threads)

    # Circlator
    print("Running Circlator fixstart...")
    circlator_command(args.circlator_path, args.dnaA_file, args.infile, args.sample_name, 'fixstart')

    # Medaka polishing
    print("Running Medaka polishing...")
    medaka_command(args.medaka_path, args.long_reads, args.contigs, args.outdir, args.threads)

    # BWA and Racon
    print("Running BWA and Racon polishing...")
    bwa_command(args.bwa_path, args.assembly_reference, args.pe_reads, args.outdir, args.threads, 1)
    racon_command(args.racon_path, args.pe_reads, args.overlaps, args.target_sequences, args.outdir, args.sample_name, args.threads, 1)

    end = time.time()
    print(f"Total Wall Time: {end - start} seconds")
    print("Fin! Enjoy your day!")

def main():
    parser = argparse.ArgumentParser(description="Flye Assembly Pipeline")
    parser.add_argument("--flye_path", required=True, help="Path to Flye")
    parser.add_argument("--circlator_path", required=True, help="Path to Circlator")
    parser.add_argument("--medaka_path", required=True, help="Path to Medaka")
    parser.add_argument("--bwa_path", required=True, help="Path to BWA")
    parser.add_argument("--racon_path", required=True, help="Path to Racon")
    parser.add_argument("--long_reads", required=True, help="Path to long reads file")
    parser.add_argument("--pe_reads", required=True, help="Path to paired-end reads file")
    parser.add_argument("--dnaA_file", required=True, help="Path to dnaA file for Circlator")
    parser.add_argument("--infile", required=True, help="Input file for Circlator")
    parser.add_argument("--contigs", required=True, help="Contigs file for Medaka")
    parser.add_argument("--assembly_reference", required=True, help="Assembly reference for BWA")
    parser.add_argument("--overlaps", required=True, help="Overlaps file for Racon")
    parser.add_argument("--target_sequences", required=True, help="Target sequences file for Racon")
    parser.add_argument("--sample_name", required=True, help="Sample name")
    parser.add_argument("--outdir", required=True, help="Output directory")
    parser.add_argument("--threads", type=int, required=True, help="Number of threads to use")

    args = parser.parse_args()
    run_pipeline(args)

if __name__ == "__main__":
    main()

