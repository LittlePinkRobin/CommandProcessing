'''
:author: Robin Avenoso
This is a program for a simple dynamic command processor that takes in a file
with possible commands and corisponding 'action codes' which are just
identifying values that can be used to perform a task.
'''

class Node:
    '''
    Node structure that holds the value of a word in the command structure.
    '''

    def __contains__(self, item):
        return self.neighbors.keys().__contains__(item)

    def __init__(self, value):
        self.value = value
        self.neighbors = dict()

    def get(self, item):
        return self.neighbors[item]

    def add(self, key, value):
        self.neighbors[key] = value

class BlankNode:
    '''
    Special type of Node for gathering parameters from.
    '''

    def __contains__(self, item):
        return self.neighbors.keys().__contains__(item)

    def __init__(self):
        self.neighbors = dict()

    def get(self, item):
        return self.neighbors[item]

    def add(self, key, value):
        self.neighbors[key] = value

class ActionNode:
    '''
    Special Node to hold the action value to take for this branch.
    '''

    def __init__(self, value):
        self.value = value

class CommandProcessor:
    '''
    The processor object that you use to parse commands.
    '''

    def __init__(self, file):
        '''
        Creats a CommandProcessor object that builds a tree based off the
        possible commands.
        :param file: Name of a configuration file of the correct format
        '''
        self.start_node = Node(None)

        with open(file) as o:
            for line in o:
                curr_node = self.start_node
                line = line.replace('\n', '')
                action = line[line.index(';')+1:len(line)].strip()
                line = line[0:line.index(';')]
                for word in line.split():
                    if word in curr_node:
                        curr_node = curr_node.get(word)
                    else:
                        if  word == '_':
                            tmp = BlankNode()
                            curr_node.add('_', tmp)
                            curr_node = tmp
                        else:
                            tmp = Node(word)
                            curr_node.add(word, tmp)
                            curr_node = tmp
                curr_node.add('ACTION', ActionNode(action))

    def parse(self, string):
        '''
        This function takes in a string that is pre-sanitized and determines
        what the parameters in the command are and what the action code is as
        it traverses the branches of the tree.
        :param string: A string that holds the input value to process
        :return: A list containing the action code followed by the parameters
        '''
        parameters = list()
        command = string.split()
        curr_node = self.start_node
        for word in command:
            if word in curr_node:
                curr_node = curr_node.get(word)
            elif '_' in curr_node:
                parameters.append(word)
                curr_node = curr_node.get('_')
            else:
                raise LookupError("No command of this structure")
        return [curr_node.neighbors.get('ACTION').value] + parameters

