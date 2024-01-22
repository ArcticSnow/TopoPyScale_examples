#!/bin/bash



#SBATCH -J naryn_worker # A single job name for the array
#SBATCH -p node # Partition (required)
#SBATCH -A node
#SBATCH -q normal # QOS (required)
#SBATCH -n 4 # one cores
#SBATCH -t 48:00:00 # Running time of 2 days
#SBATCH --mem 8000 # Memory request of 4 GB
#SBATCH -o LOG_naryn-%j-%a.out # Standard output - write the console output to the output folder %A= Job ID, %a = task or Step ID
#SBATCH -e LOG_naryn-%j-%a.err # Standard error -write errors to the errors folder and
#SBATCH --array=1-23 # this is number of years in downscaling job
#SBATCH --mail-user=joelfiddes@gmail.com
#SBATCH --mail-type=ALL  # Send me some mails when jobs end or fail.
pwd; hostname; date


source /home/caduff/.bashrc
conda activate downscaling

python run_worker.py ${SLURM_ARRAY_TASK_ID}



