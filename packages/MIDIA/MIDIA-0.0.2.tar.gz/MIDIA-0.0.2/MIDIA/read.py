from pathlib import Path

data_f = Path("/home/matteo/Projects/bruker/BrukerMIDIA")
all_datasets = list(f for f in data_f.glob("**/*.d") if f.is_dir())
tdf_datasets = [f for f in all_datasets if (f/'analysis.tdf').exists()]

