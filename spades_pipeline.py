#!/usr/bin/env python3

import os
import subprocess
import argparse
import time

# Define constants for database paths and tool paths
ADAPTER_DATABASE1 = '/data/opt/jarfiles/trimmomatic/v0.39/Trimmomatic-0.39/adapters/All_adapters.fa'
KRAKEN2_DATABASE1 = '/data/opt/databases/kraken2/RefSeq_Kraken2_std_2019_02_12'
TRIMMOMATIC_PATH = '/data/opt/jarfiles/trimmomatic/v0.39/Trimmomatic-0.39/trimmomatic-0.39.jar'
FASTQC_PATH = '/data/opt/programs/etc/fastqc/FastQC-v0.11.9/fastqc'

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

def fastqc_command(perl_path, fastqc_path, threads, sample_name, outdir, read1, read2):
    fastqc_outdir = os.path.join(outdir, f"{sample_name}_fastqc")
    command = [perl_path, fastqc_path, "--threads", str(threads), "--outdir", fastqc_outdir, read1, read2]
    run_command(command)

def trimmomatic_command(java_path, trimmomatic_path, threads, sample_name, outdir, read1, read2, adapter_database):
    output_dir = os.path.join(outdir, f"{sample_name}_trimmomatic")
    command = [
        java_path, "-jar", trimmomatic_path, "PE", "-phred33",
        read1, read2,
        os.path.join(output_dir, f"{sample_name}_forward_paired.fq.gz"),
        os.path.join(output_dir, f"{sample_name}_forward_unpaired.fq.gz"),
        os.path.join(output_dir, f"{sample_name}_reverse_paired.fq.gz"),
        os.path.join(output_dir, f"{sample_name}_reverse_unpaired.fq.gz"),
        "ILLUMINACLIP:" + adapter_database + ":2:30:10",
        "LEADING:3", "TRAILING:3", "SLIDINGWINDOW:4:15", "MINLEN:36"
    ]
    run_command(command)

# Define other functions similarly with appropriate error handling...

def run_pipeline(args):
    start = time.time()
    
    create_directory(args.outdir)
    
    # FastQC step
    print("Running FastQC...")
    fastqc_command(args.perl_path, FASTQC_PATH, args.threads, args.sample_name, args.outdir, args.read1, args.read2)
    
    # Trimmomatic step
    print("Running Trimmomatic...")
    trimmomatic_command(args.java_path, TRIMMOMATIC_PATH, args.threads, args.sample_name, args.outdir, args.read1, args.read2, ADAPTER_DATABASE1)
    
    # Add other steps here...
    
    end = time.time()
    print(f"Total Wall Time: {end - start} seconds")
    print("Fin! Enjoy your day!")

def main():
    parser = argparse.ArgumentParser(description="SPAdes Assembly Pipeline")
    parser.add_argument("--perl_path", required=True, help="Path to perl")
    parser.add_argument("--java_path", required=True, help="Path to java")
    parser.add_argument("--threads", type=int, required=True, help="Number of threads to use")
    parser.add_argument("--sample_name", required=True, help="Sample name")
    parser.add_argument("--outdir", required=True, help="Output directory")
    parser.add_argument("--read1", required=True, help="Path to read1 file")
    parser.add_argument("--read2", required=True, help="Path to read2 file")
    
    args = parser.parse_args()
    run_pipeline(args)

if __name__ == "__main__":
    main()

