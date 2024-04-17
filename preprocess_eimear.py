import os
import json





if __name__ == "__main__":
    path = 'data_raw/'
    locution_dataset = {'data': []}
    argumentative_dataset = {'data': []}
    li_dataset = {'data': []}

    l_arg_dataset = {'data': []}
    l_arg_lex_dataset = {'data': []}
    l_arg_tok_dataset = {'data': []}
    l_arg_tok_dir_dataset = {'data': []}
    
    
    for filename in os.listdir(path):
        if filename.split('.')[1] == 'json':
            # print(filename)
            with open(path + filename) as filehandle:
                content = json.load(filehandle)
            hyp_nodes = []

        

            for node in content['nodes']:
                text_loc = ''
                text_arg = ''

                # Hypotheses
                if node['text'] == 'Hypothesising':

                    # Combined L-text I-text
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
                        li_dataset['data'].append([text_loc+'. '+text_arg, 0])

                    # L + ARG
                    for edge in content['edges']:
                        # LOCUTION TEXT
                        # Get incoming edge to Hyp (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        l_text = text.split(': ')[1]
                        
                        
                        # ARG REP
                        # Get outgoing edge from Hyp (only if to I-node)
                        if edge['fromID'] == node['nodeID']: # get target node of edge
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If target node of hyp is proposition, search for connected argument relations
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text = node2['text'] # hyp-anchored I-node text

                                    # Make copies of the starter I-node text for the different kinds of concatentation
                                    lex_text = text
                                    tok_text = text
                                    tok_dir_text = text

                                    prop_id = node2['nodeID'] # hyp-anchored I-node id

                                    # Search for Argument Relations
                                    potential_ids = [] # potential 

                                    # Look for edges connecting to the hyp proposition
                                    # Collecting list of ID lists, each item 
                                    for edge2 in content['edges']: 
                                        
                                        # Edge FROM the proposition: Check if the proposition has a relation going out
                                        if edge2['fromID'] == prop_id: 
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['toID'] == edge3['fromID']:
                                                    potential_ids.append([edge3['toID'], edge3['fromID'], 'from_prop'])
                                        
                                        # Edge TO the proposition: Check if the proposition has a relation coming in
                                        elif edge2['toID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['fromID'] == edge3['toID']:
                                                    potential_ids.append([edge3['fromID'], edge3['toID'], 'to_prop'])

                                    
                                    # Search for the text in the argumentative nodes related
                                    for id in potential_ids:
                                        for node3 in content['nodes']: 
                                            if id[1] == node3['nodeID']: 
                                                if node3['type'] == 'RA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            if id[2] == 'from_prop':
                                                                lex_text += '. Therefore ' + node4['text']
                                                                tok_dir_text += ' [IFP] ' + node4['text'] # format: [premise prop] [inference: first was premise] [conclusion prop]
                                                            elif id[2] == 'to_prop':
                                                                lex_text += '. Because ' + node4['text']
                                                                tok_dir_text += ' [IFC] ' + node4['text'] # format: [conclusion prop] [inference: first was conclusion] [premise prop]
                                                            tok_text += ' [INF] ' + node4['text']
                                                            text += '. ' + node4['text']
                                                elif node3['type'] == 'CA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            if id[2] == 'from_prop':
                                                                lex_text += '. Despite ' + node4['text']
                                                                tok_dir_text += ' [CNP] ' + node4['text'] # format: [premise/attacker prop] [conclict: first was premise/attacker] [conclusion/target prop]
                                                            elif id[2] == 'to_prop':
                                                                lex_text += '. However ' + node4['text']
                                                                tok_dir_text += ' [CNC] ' + node4['text'] # format: [conclusion/target prop] [conclict: first was conclusion/target] [premise/attacker prop]
                                                            tok_text += ' [CON] ' + node4['text']
                                                            text += '. ' + node4['text']
                                    if l_text != '' and text != '':
                                        l_arg_dataset['data'].append([l_text + '. ' + text, 0])
                                        l_arg_lex_dataset['data'].append([l_text + '. ' + lex_text, 0])
                                        l_arg_tok_dataset['data'].append([l_text + '. ' + tok_text, 0])
                                        l_arg_tok_dir_dataset['data'].append([l_text + '. ' + tok_dir_text, 0])



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

                    # L-text + I-text
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
                        li_dataset['data'].append([text_loc + '. ' + text_arg, 1])
                    
                    # L + ARG
                    for edge in content['edges']:
                        # LOCUTION TEXT
                        # Get incoming edge to Assert (from locution)
                        if edge['toID'] == node['nodeID']:
                            # Search for the locution
                            for node2 in content['nodes']:
                                # If node is the locution
                                if node2['nodeID'] == edge['fromID'] and node2['type'] == 'L':
                                    text = node2['text']
                                    if ':' in text:
                                        l_text = text.split(': ')[1]
                        
                        # ARG REP
                        # Get outgoing edge from Assert (only if to I-node)
                        if edge['fromID'] == node['nodeID']: # get target node of edge
                            # Search for the proposition
                            for node2 in content['nodes']:
                                # If target node of assert is proposition, search for connected argument relations
                                if node2['nodeID'] == edge['toID'] and node2['type'] == 'I':
                                    text = node2['text'] # assert-anchored I-node text

                                    # Make copies of the starter I-node text for the different kinds of concatentation
                                    lex_text = text
                                    tok_text = text
                                    tok_dir_text = text

                                    prop_id = node2['nodeID'] # hyp-anchored I-node id

                                    # Search for Argument Relations
                                    potential_ids = [] # potential 

                                    # Look for edges connecting to the hyp proposition
                                    # Collecting list of ID lists, each item 
                                    for edge2 in content['edges']: 
                                        
                                        # Edge FROM the proposition: Check if the proposition has a relation going out
                                        if edge2['fromID'] == prop_id: 
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['toID'] == edge3['fromID']:
                                                    potential_ids.append([edge3['toID'], edge3['fromID'], 'from_prop'])
                                        
                                        # Edge TO the proposition: Check if the proposition has a relation coming in
                                        elif edge2['toID'] == prop_id:
                                            # Search for the other end of the relation
                                            for edge3 in content['edges']:
                                                if edge2['fromID'] == edge3['toID']:
                                                    potential_ids.append([edge3['fromID'], edge3['toID'], 'to_prop'])

                                    
                                    # Search for the text in the argumentative nodes related
                                    for id in potential_ids:
                                        for node3 in content['nodes']: 
                                            if id[1] == node3['nodeID']: 
                                                if node3['type'] == 'RA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            if id[2] == 'from_prop':
                                                                lex_text += '. Therefore ' + node4['text']
                                                                tok_dir_text += ' [IFP] ' + node4['text'] # format: [premise prop] [inference: first was premise] [conclusion prop]
                                                            elif id[2] == 'to_prop':
                                                                lex_text += '. Because ' + node4['text']
                                                                tok_dir_text += ' [IFC] ' + node4['text'] # format: [conclusion prop] [inference: first was concl] [premise prop]
                                                            tok_text += ' [INF] ' + node4['text']
                                                            text += '. ' + node4['text']
                                                elif node3['type'] == 'CA':
                                                    for node4 in content['nodes']:
                                                        if id[0] == node4['nodeID'] and node4['type'] == 'I':
                                                            if id[2] == 'from_prop':
                                                                lex_text += '. Despite ' + node4['text']
                                                                tok_dir_text += ' [CNP] ' + node4['text'] # format: [premise/attacker prop] [conclict: first was premise/attacker] [conclusion/target prop]
                                                            elif id[2] == 'to_prop':
                                                                lex_text += '. However ' + node4['text']
                                                                tok_dir_text += ' [CNC] '  + node4['text'] # format: [conclusion/target prop] [conclict: first was conclusion/target] [premise/attacker prop]
                                                            tok_text += ' [CON] ' + node4['text']
                                                            text += '. ' + node4['text']

                                    if l_text != '' and text != '':
                                        l_arg_dataset['data'].append([l_text + '. ' + text, 1])
                                        l_arg_lex_dataset['data'].append([l_text + '. ' + lex_text, 1])
                                        l_arg_tok_dataset['data'].append([l_text + '. ' + tok_text, 1])
                                        l_arg_tok_dir_dataset['data'].append([l_text + '. ' + tok_dir_text, 1])




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
    print(len(li_dataset['data']))
    print(len(l_arg_dataset['data']))
    print(len(l_arg_lex_dataset['data']))
    print(len(l_arg_tok_dataset['data']))
    print(len(l_arg_tok_dir_dataset['data']))

    with open('data_ready/argument_hypothesis.json', "w") as outfile:
        json.dump(argumentative_dataset, outfile, indent=4)
    with open('data_ready/locution_hypothesis.json', "w") as outfile:
        json.dump(locution_dataset, outfile, indent=4)
    with open('data_ready/li_hypothesis.json', "w") as outfile:
        json.dump(li_dataset, outfile, indent=4)
    with open('data_ready/l_arg_hypothesis.json', "w") as outfile:
        json.dump(l_arg_dataset, outfile, indent=4)
    with open('data_ready/l_arg_lex_hypothesis.json', "w") as outfile:
        json.dump(l_arg_lex_dataset, outfile, indent=4)
    with open('data_ready/l_arg_tok_hypothesis.json', "w") as outfile:
        json.dump(l_arg_tok_dataset, outfile, indent=4)
    with open('data_ready/l_arg_tok_dir_hypothesis.json', "w") as outfile:
        json.dump(l_arg_tok_dir_dataset, outfile, indent=4)