import sys,align,os
import time, warnings
import pandas as pd

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

#https://github.com/nickduran/align-linguistic-alignment/blob/master/examples/align-devilsadvocate_example.ipynb

BASE_PATH = os.getcwd()
TRANSCRIPT_PATH = os.path.join(BASE_PATH,'DataSets/') #ending slash
PREPPED_TRANSCRIPTS = os.path.join(BASE_PATH,'Reformatted/')

print(TRANSCRIPT_PATH)
print(PREPPED_TRANSCRIPTS)

ANALYSIS_READY = os.path.join(BASE_PATH,'analysis/')
if not os.path.exists(ANALYSIS_READY):
    os.makedirs(ANALYSIS_READY)

SURROGATE_TRANSCRIPTS = os.path.join(BASE_PATH,'surrogate/')
if not os.path.exists(SURROGATE_TRANSCRIPTS):
    os.makedirs(SURROGATE_TRANSCRIPTS)



start_phase1 = time.time()

model_store = align.prepare_transcripts(
                        input_files=TRANSCRIPT_PATH,
                        output_file_directory=PREPPED_TRANSCRIPTS,
                        run_spell_check=True,
                        minwords=2,
                        use_filler_list=None,
                        filler_regex_and_list=False,
                        training_dictionary=None,
                        add_stanford_tags=False,
                        ### if you want to run the Stanford POS tagger, be sure to uncomment the next two lines
                        # stanford_pos_path=STANFORD_POS_PATH,
                        # stanford_language_path=STANFORD_LANGUAGE,    
                        save_concatenated_dataframe=True)

end_phase1 = time.time()

print(align.calculate_alignment.__doc__)

# set standards to be used for real and surrogate
INPUT_FILES = PREPPED_TRANSCRIPTS
MAXNGRAM = 2
USE_PRETRAINED_VECTORS = True
SEMANTIC_MODEL_INPUT_FILE = os.path.join(TRANSCRIPT_PATH,
                                         'align_concatenated_dataframe.txt')
#PRETRAINED_FILE_DRIRECTORY = PRETRAINED_INPUT_FILE
ADD_STANFORD_TAGS = False
IGNORE_DUPLICATES = True
HIGH_SD_CUTOFF = 3
LOW_N_CUTOFF = 1

start_phase2real = time.time()

[turn_real,convo_real] = align.calculate_alignment(
                            input_files=INPUT_FILES,
                            maxngram=MAXNGRAM,   
                            use_pretrained_vectors=USE_PRETRAINED_VECTORS,
                            #pretrained_input_file=PRETRAINED_INPUT_FILE,
                            semantic_model_input_file=SEMANTIC_MODEL_INPUT_FILE,
                            output_file_directory=ANALYSIS_READY,
                            add_stanford_tags=ADD_STANFORD_TAGS,
                            ignore_duplicates=IGNORE_DUPLICATES,
                            high_sd_cutoff=HIGH_SD_CUTOFF,
                            low_n_cutoff=LOW_N_CUTOFF)

end_phase2real = time.time()

print(align.calculate_baseline_alignment.__doc__)


start_phase2surrogate = time.time()

[turn_surrogate,convo_surrogate] = align.calculate_baseline_alignment(
                                    input_files=INPUT_FILES, 
                                    maxngram=MAXNGRAM,
                                    use_pretrained_vectors=USE_PRETRAINED_VECTORS,
                                    pretrained_input_file=PRETRAINED_INPUT_FILE,
                                    semantic_model_input_file=SEMANTIC_MODEL_INPUT_FILE,
                                    output_file_directory=ANALYSIS_READY,
                                    add_stanford_tags=ADD_STANFORD_TAGS,
                                    ignore_duplicates=IGNORE_DUPLICATES,
                                    high_sd_cutoff=HIGH_SD_CUTOFF,
                                    low_n_cutoff=LOW_N_CUTOFF,
                                    surrogate_file_directory=SURROGATE_TRANSCRIPTS,
                                    all_surrogates=False,
                                    keep_original_turn_order=True,
                                    id_separator='\_',
                                    dyad_label='dyad',
                                    condition_label='cond')

convo_surrogate

end_phase2surrogate = time.time()


# end_phase1 - start_phase1
# end_phase2real - start_phase2real
# end_phase2surrogate - start_phase2surrogate
# end_phase2surrogate - start_phase1



turn_real.head(10)
convo_real.head(10)
turn_surrogate.head(10)
convo_surrogate.head(10)


