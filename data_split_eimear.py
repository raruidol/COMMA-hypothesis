import json
import os

if __name__ == "__main__":

    for filename in ['locution_hypothesis.json', 'argument_hypothesis.json', 
                     'li_hypothesis.json', 'l_arg_hypothesis.json', 'l_arg_lex_hypothesis.json',
                     'l_arg_tok_hypothesis.json', 'l_arg_tok_dir_hypothesis.json']:
        with open(os.path.join('data_ready', filename)) as filehandle:
            dataset = json.load(filehandle)

        split_by_label = {1: [], 0: []}
        for sample in dataset['data']:
            split_by_label[sample[1]].append(sample)

        print(f"{filename} Hypotheses = ", len(split_by_label[0]))
        print(f"{filename} Assertions = ", len(split_by_label[1]))

        dataset['train'] = split_by_label[0][0:int(len(split_by_label[0])*0.8)]+split_by_label[1][0:int(len(split_by_label[1])*0.8)]
        dataset['dev'] = split_by_label[0][int(len(split_by_label[0])*0.8):int((len(split_by_label[0])*0.8)+(len(split_by_label[0])*0.1))]+split_by_label[1][int(len(split_by_label[1])*0.8):int((len(split_by_label[1])*0.8+len(split_by_label[1])*0.1))]
        dataset['test'] = split_by_label[0][int((len(split_by_label[0])*0.8)+(len(split_by_label[0])*0.1)):-1]+split_by_label[1][int((len(split_by_label[1])*0.8+len(split_by_label[1])*0.1)):-1]

        with open(os.path.join('data_split', filename), "w") as outfile:
            json.dump(dataset, outfile, indent=4)
