import json


if __name__ == "__main__":

    with open('data_ready/locution_hypothesis.json') as filehandle:
        locution_dataset = json.load(filehandle)
    with open('data_ready/argument_hypothesis.json') as filehandle:
        argument_dataset = json.load(filehandle)
    with open('data_ready/li_hypothesis.json') as filehandle:
        li_dataset = json.load(filehandle)
    with open('data_ready/l_arg_hypothesis.json') as filehandle:
        l_arg_dataset = json.load(filehandle)

    locutions = {1: [], 0: []}
    for locution in locution_dataset['data']:
        locutions[locution[1]].append(locution)

    arguments = {1: [], 0: []}
    for argument in argument_dataset['data']:
        arguments[argument[1]].append(argument)

    li = {1: [], 0: []}
    for comb in li_dataset['data']:
        li[comb[1]].append(comb)
    
    l_arg = {1: [], 0: []}
    for comb in l_arg_dataset['data']:
        l_arg[comb[1]].append(comb)

    print('Argument Hypotheses = ', len(arguments[0]))
    print('Argument Assertions = ', len(arguments[1]))
    print('Locution Hypotheses = ', len(locutions[0]))
    print('Locution Assertions = ', len(locutions[1]))
    print('Combined L+I Hypotheses = ', len(li[0]))
    print('Combined L+I Assertions = ', len(li[1]))
    print('Combined L+Arg Hypotheses = ', len(l_arg[0]))
    print('Combined L+Arg Assertions = ', len(l_arg[1]))

    argument_dataset['train'] = arguments[0][0:int(len(arguments[0])*0.8)]+arguments[1][0:int(len(arguments[1])*0.8)]
    locution_dataset['train'] = locutions[0][0:int(len(locutions[0])*0.8)]+locutions[1][0:int(len(locutions[1])*0.8)]
    li_dataset['train'] = li[0][0:int(len(li[0])*0.8)]+li[1][0:int(len(li[1])*0.8)]
    l_arg_dataset['train'] = l_arg[0][0:int(len(l_arg[0])*0.8)]+l_arg[1][0:int(len(l_arg[1])*0.8)]

    argument_dataset['dev'] = arguments[0][int(len(arguments[0])*0.8):int((len(arguments[0])*0.8)+(len(arguments[0])*0.1))]+arguments[1][int(len(arguments[1])*0.8):int((len(arguments[1])*0.8+len(arguments[1])*0.1))]
    locution_dataset['dev'] = locutions[0][int(len(locutions[0])*0.8):int((len(locutions[0])*0.8)+(len(locutions[0])*0.1))]+locutions[1][int(len(locutions[1])*0.8):int((len(locutions[1])*0.8+len(locutions[1])*0.1))]
    li_dataset['dev'] = li[0][int(len(li[0])*0.8):int((len(li[0])*0.8)+(len(li[0])*0.1))] + li[1][int(len(li[1])*0.8):int((len(li[1])*0.8+len(li[1])*0.1))]
    l_arg_dataset['dev'] = l_arg[0][int(len(l_arg[0])*0.8):int((len(l_arg[0])*0.8)+(len(l_arg[0])*0.1))] + l_arg[1][int(len(l_arg[1])*0.8):int((len(l_arg[1])*0.8+len(l_arg[1])*0.1))]

    argument_dataset['test'] = arguments[0][int((len(arguments[0])*0.8)+(len(arguments[0])*0.1)):-1]+arguments[1][int((len(arguments[1])*0.8+len(arguments[1])*0.1)):-1]
    locution_dataset['test'] = locutions[0][int((len(locutions[0])*0.8)+(len(locutions[0])*0.1)):-1]+locutions[1][int((len(locutions[1])*0.8+len(locutions[1])*0.1)):-1]
    li_dataset['test'] = li[0][int((len(li[0])*0.8)+(len(li[0])*0.1)):-1]+li[1][int((len(li[1])*0.8+len(li[1])*0.1)):-1]
    l_arg_dataset['test'] = l_arg[0][int((len(l_arg[0])*0.8)+(len(l_arg[0])*0.1)):-1]+l_arg[1][int((len(l_arg[1])*0.8+len(l_arg[1])*0.1)):-1]


    with open('data_split/argument_hypothesis.json', "w") as outfile:
        json.dump(argument_dataset, outfile, indent=4)
    with open('data_split/locution_hypothesis.json', "w") as outfile:
        json.dump(locution_dataset, outfile, indent=4)
    with open('data_split/combined_hypothesis.json', "w") as outfile:
        json.dump(li_dataset, outfile, indent=4)
    with open('data_split/l_arg_hypothesis.json', "w") as outfile:
        json.dump(l_arg_dataset, outfile, indent=4)
