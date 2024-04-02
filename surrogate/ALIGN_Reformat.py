import os

def convert_transcript_to_input_format(transcript_file, output_file):
    with open(transcript_file, 'r') as infile:
        lines = infile.readlines()

    output_lines = []
    participant_label = None

    for line in lines:
        line = line.strip()

        if line:
            speaker, *content = line.split('\t', 1)

            if content:  # check if there is a char in array
                content = content[0]
            else:
                content = ""  #if it's not available

            if speaker == 'C:':
                participant_label = 'P1'
            elif speaker == 'T:':
                participant_label = 'P2'

            output_lines.append(f"{participant_label}\t{content}\n")

    with open(output_file, 'w') as outfile:
        outfile.writelines(output_lines)

def process_folder(input_folder, output_folder):
    #if file was not made, it will make it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #iterate
    for filename in os.listdir(input_folder):
        filename_output = filename+".txt"

        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename_output)

        #convert and save the reformatted file for all files
        convert_transcript_to_input_format(input_file_path, output_file_path)
        print(f"Processed: {filename_output}")

# output/input folder names
input_folder = 'DataSets'
output_folder = 'Reformatted'

# Process the folder
process_folder(input_folder, output_folder)
