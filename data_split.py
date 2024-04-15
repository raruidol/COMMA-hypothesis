import json


if __name__ == "__main__":

    with open('data_ready/locution_hypothesis.json') as filehandle:
        locution_dataset = json.load(filehandle)
    with open('data_ready/argument_hypothesis.json') as filehandle:
        argument_dataset = json.load(filehandle)
    with open('data_ready/combined_hypothesis.json') as filehandle:
        combined_dataset = json.load(filehandle)

    locutions = {1: [], 0: []}
    for locution in locution_dataset['data']:
        locutions[locution[1]].append(locution)

    arguments = {1: [], 0: []}
    for argument in argument_dataset['data']:
        arguments[argument[1]].append(argument)

    combined = {1: [], 0: []}
    for comb in combined_dataset['data']:
        combined[comb[1]].append(comb)

    print('Argument Hypotheses = ', len(arguments[0]))
    print('Argument Assertions = ', len(arguments[1]))
    print('Locution Hypotheses = ', len(locutions[0]))
    print('Locution Assertions = ', len(locutions[1]))
    print('Combined Hypotheses = ', len(combined[0]))
    print('Combined Assertions = ', len(combined[1]))

    argument_dataset['train'] = arguments[0][0:int(len(arguments[0])*0.8)]+arguments[1][0:int(len(arguments[1])*0.8)]
    locution_dataset['train'] = locutions[0][0:int(len(locutions[0])*0.8)]+locutions[1][0:int(len(locutions[1])*0.8)]
    combined_dataset['train'] = combined[0][0:int(len(combined[0])*0.8)]+combined[1][0:int(len(combined[1])*0.8)]

    argument_dataset['dev'] = arguments[0][int(len(arguments[0])*0.8):int((len(arguments[0])*0.8)+(len(arguments[0])*0.1))]+arguments[1][int(len(arguments[1])*0.8):int((len(arguments[1])*0.8+len(arguments[1])*0.1))]
    locution_dataset['dev'] = locutions[0][int(len(locutions[0])*0.8):int((len(locutions[0])*0.8)+(len(locutions[0])*0.1))]+locutions[1][int(len(locutions[1])*0.8):int((len(locutions[1])*0.8+len(locutions[1])*0.1))]
    combined_dataset['dev'] = combined[0][int(len(combined[0])*0.8):int((len(combined[0])*0.8)+(len(combined[0])*0.1))] + combined[1][int(len(combined[1])*0.8):int((len(combined[1])*0.8+len(combined[1])*0.1))]

    argument_dataset['test'] = arguments[0][int((len(arguments[0])*0.8)+(len(arguments[0])*0.1)):-1]+arguments[1][int((len(arguments[1])*0.8+len(arguments[1])*0.1)):-1]
    locution_dataset['test'] = locutions[0][int((len(locutions[0])*0.8)+(len(locutions[0])*0.1)):-1]+locutions[1][int((len(locutions[1])*0.8+len(locutions[1])*0.1)):-1]
    combined_dataset['test'] = combined[0][int((len(combined[0])*0.8)+(len(combined[0])*0.1)):-1]+combined[1][int((len(combined[1])*0.8+len(combined[1])*0.1)):-1]

    with open('data_split/argument_hypothesis.json', "w") as outfile:
        json.dump(argument_dataset, outfile, indent=4)
    with open('data_split/locution_hypothesis.json', "w") as outfile:
        json.dump(locution_dataset, outfile, indent=4)
    with open('data_split/combined_hypothesis.json', "w") as outfile:
        json.dump(combined_dataset, outfile, indent=4)

