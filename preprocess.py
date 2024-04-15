import os
import json


if __name__ == "__main__":
    path = 'data_raw/'
    locution_dataset = {'data': []}
    argumentative_dataset = {'data': []}
    combined_dataset = {'data': []}
    for filename in os.listdir(path):
        if filename.split('.')[1] == 'json':
            print(filename)
            with open(path + filename) as filehandle:
                content = json.load(filehandle)
            hyp_nodes = []

            for node in content['nodes']:
                text_loc = ''
                text_arg = ''

                # Hypotheses
                if node['text'] == 'Hypothesising':

                    # Combined
                    for edge in content['edges']:
                        # Get incoming edge (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        text_loc = text.split(': ')[1]

                        if edge['fromID'] == node['nodeID']:
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If node is the proposition
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text_arg = node2['text']

                    if text_loc != '' and text_arg != '':
                        combined_dataset['data'].append([text_loc+'. '+text_arg, 0])

                    # Locution
                    for edge in content['edges']:
                        # Get incoming edge (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        text = text.split(': ')[1]
                                    locution_dataset['data'].append([text, 0])

                    # Argument
                    for edge in content['edges']:
                        # Get outcoming edge (to proposition)
                        if edge['fromID'] == node['nodeID']:
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If node is the proposition
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text = node2['text']
                                    prop_id = node2['nodeID']

                                    # Search for Argument Relations
                                    potential_ids = []
                                    for edge2 in content['edges']:
                                        # Check if the proposition has a relation going out
                                        if edge2['fromID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['toID'] == edge3['fromID']:
                                                    potential_ids.append([edge3['toID'], edge3['fromID']])
                                        # Check if the proposition has a relation coming in
                                        elif edge2['toID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['fromID'] == edge3['toID']:
                                                    potential_ids.append([edge3['fromID'], edge3['toID']])

                                    # Search for the text in the argumentative nodes related
                                    for id in potential_ids:
                                        for node3 in content['nodes']:
                                            if id[1] == node3['nodeID']:
                                                if node3['type'] == 'RA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            # text += ' [INF] ' + node4['text']
                                                            text += '. ' + node4['text']
                                                elif node3['type'] == 'CA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            # text += ' [CON] ' + node4['text']
                                                            text += '. ' + node4['text']

                                    argumentative_dataset['data'].append([text, 0])

                # Assertions
                if node['text'] == 'Asserting':

                    # Combined
                    for edge in content['edges']:
                        # Get incoming edge (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        text_loc = text.split(': ')[1]

                        if edge['fromID'] == node['nodeID']:
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If node is the proposition
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text_arg = node2['text']

                    if text_loc != '' and text_arg != '':
                        combined_dataset['data'].append([text_loc + '. ' + text_arg, 1])

                    # Locution
                    for edge in content['edges']:
                        # Get incoming edge (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        text = text.split(': ')[1]

                                    locution_dataset['data'].append([text, 1])

                    # Argument
                    for edge in content['edges']:
                        # Get outcoming edge (to proposition)
                        if edge['fromID'] == node['nodeID']:
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If node is the proposition
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text = node2['text']
                                    prop_id = node2['nodeID']

                                    # Search for Argument Relations
                                    potential_ids = []
                                    for edge2 in content['edges']:
                                        # Check if the proposition has a relation going out
                                        if edge2['fromID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['toID'] == edge3['fromID']:
                                                    potential_ids.append([edge3['toID'], edge3['fromID']])
                                        # Check if the proposition has a relation coming in
                                        elif edge2['toID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['fromID'] == edge3['toID']:
                                                    potential_ids.append([edge3['fromID'], edge3['toID']])

                                    # Search for the text in the argumentative nodes related
                                    for id in potential_ids:
                                        for node3 in content['nodes']:
                                            if id[1] == node3['nodeID']:
                                                if node3['type'] == 'RA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            # text += ' [INF] ' + node4['text']
                                                            text += '. ' + node4['text']
                                                elif node3['type'] == 'CA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            # text += ' [CON] ' + node4['text']
                                                            text += '. ' + node4['text']

                                    argumentative_dataset['data'].append([text, 1])

    print(len(argumentative_dataset['data']))
    print(len(locution_dataset['data']))
    print(len(combined_dataset['data']))

    with open('data_ready/argument_hypothesis.json', "w") as outfile:
        json.dump(argumentative_dataset, outfile, indent=4)
    with open('data_ready/locution_hypothesis.json', "w") as outfile:
        json.dump(locution_dataset, outfile, indent=4)
    with open('data_ready/combined_hypothesis.json', "w") as outfile:
        json.dump(combined_dataset, outfile, indent=4)
