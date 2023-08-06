# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 19:14:46 2019

@author: Yichun Shi
"""

#!/usr/bin/env python3

## Your code goes here.
import heapq


def read_terms_slowComplete(filename):
    """
    given a file path, will read each line into word and weight,
    and append the words and weights to a list. The list can be called in 
    slowComplete()
    
    @input:filepath
    @output: a list of words and its associated weight
    """
    array = []
    list_of_words = []
    with open(filename, "r", encoding="utf-8") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))  
    
    for element in array[1:]:
        weight = int(element.split(None,1)[0])
        word = element.split(None,1)[1]
        list_of_words.append((word, weight))
    return list_of_words
    

def slowComplete(input_word, list_of_words,K):
    """
    assuming list of words given which each line as a string like '123 happy', split each line into word 
    and its associated weight, find the words matching with prefix, and return K number of top matches
    
    @input: prefix of interest, a list of words with its associated weight,
    K number of final suggestions
    @output:K number of top matches
    """
    from heapq import heappush, heappop
    matches = []
    final_K_results = []
    i = 0
    length_of_input = len(input_word)
    for line in list_of_words:
        word = line[0]
        weight = line[1]
        if word[:length_of_input] == input_word:
            heappush(matches,(-weight, word))
    if K > len(matches):
        K = len(matches)
    while i < K:
        match = heappop(matches)
        final_K_results.append((-match[0], match[1]))
        i += 1
    if len(final_K_results) > 0:
        return final_K_results
    else:
        print('Prefix does not exist, try again')
        

class Node:
    def __init__(self):
        self.word = ''
        self.children = {}   #the child nodes are dictionary. key = partial words, value = corresponding children nodes to those partial words
        self.weight = -1  #weight of that node # a heap queue storing all children nodes by 1/weight of each node
        self.max_children_weight = -1  #an int that stores max children node weight
        self.end_of_word = False    # to keep track in other functions on whether a word is ended
        
    def __lt__(self, other):
        return True
        
# this class defines the Trie object        
class Trie:
    def __init__(self):
        self.root = Node()
        
       
    def insert(self,word,word_weight):
        """
        Takes a word and word_weight as input, go through each letter within the word,
        create a new child node if the partial word ending in that letter is not in children 
        nodes. 
        After creating the node for last letter in the word, heaqpush this last node's weight
        to node.children_weight.
        Finally after going through the word, assign the word_weight to that last node
        
        @input: trie, word and its weight
        @output: a trie with the associated nodes of that word inserted
        """
        node = self.root
        partial_word = "" 

        for letter in word:
            partial_word = partial_word + letter
            if partial_word in node.children:
                node = node.children[partial_word]
                if node.max_children_weight < word_weight:
                    node.max_children_weight = word_weight
            else:
                node.children[partial_word] = Node()
                if node.max_children_weight < word_weight:
                    node.max_children_weight = word_weight
                node = node.children[partial_word]
                node.word = partial_word
        node.weight = word_weight
        node.max_children_weight = word_weight
        node.end_of_word = True


    def search(self,prefix):
        """
        search through the trie to locate the node that is the word inputted 
        @input: a prefix
        @output: a node that exactly matches the prefix 
        """
        node = self.root
        partial_word = ""
        for letter in prefix:
            partial_word =  partial_word + letter
            if partial_word in node.children:
                node = node.children[partial_word]
            else:
                return []
        return node
    
    def delete(self,word):
        """
        for a given word, check for each letter in the word if the node has more 
        than 1 child node, or the node has end_of_word = true but still has more 
        child node. If so, mark that node as need to delete the child node representing
        partial word. After going through all letters in the given word, check 
        if the current node has no children. If so, delete the matching node representing
        the marked string from the children dictionary of the marked node. If it 
        has children nodes, change end_of_word to false on that last letter node.

        """
        node = self.root
        mark_for_delete_node = Node()
        mark_for_delete_word = ""
        partial_word = ""
        for letter in word:
            partial_word = partial_word + letter
            if partial_word in node.children:
                if len(node.children) > 1 or node.end_of_word:
                    mark_for_delete_node = node
                    mark_for_delete_word = partial_word
                node = node.children[partial_word]
        if bool(node.children) == False:
            mark_for_delete_node.children.pop(mark_for_delete_word)
        else:
            node.end_of_word = False
                    
        
    def update_weight(self,word,func):
        """
        for a given word, iterate through each letter of the word and check for 
        corresponding node of each substring, whether the new weight after given
        function is yielding a larger weight than current max_children_weight, and
        update that accordingly. Finally at the ending letter of the word, update
        node.weight
        """
        node = self.root
        partial_word = ""
        before_weight = Trie.search(self, word).weight
        new_weight = func(before_weight)
        
        for letter in word:
            partial_word = partial_word + letter
            if partial_word in node.children:
                if node.children[partial_word].max_children_weight < new_weight:
                    node.children[partial_word].max_children_weight = new_weight
                node = node.children[partial_word]
        node.weight = new_weight
        if node.max_children_weight < node.weight:
            node.max_children_weight = node.weight
            
    def insert_or_update(self,word):
        """
        Called with a given term, the function should insert the term into 
        the trie (with weight as 1) if it is not there already, or increase 
        the weight of the term by 1 if it is.
        
        @input: trie, word string
        @output: updated trie  
        """
        
        if Trie.search(self,word) == []:
            Trie.insert(self,word,1)
        else:
            Trie.update_weight(self,word,lambda x: x + 1)
            
    def prune_trie(self,threshold):
        """
        For a given threshold, delete all terms that have weight under this 
        threshold
        
        @input: trie, threshold, which is an int
        @output: updated trie 
        """
        node = self.root
        Trie.prune_node(node,threshold)
    
    def prune_node(node,threshold):
        """
        helper function for prune_trie, traverse to the children nodes of trie
        and prune appropriately 
        
        """
        for child_node in list(node.children.values()):
            if child_node.max_children_weight < threshold:
                node.children.pop(child_node.word)
            elif child_node.weight <= threshold:
                if bool(child_node):
                    child_node.end_of_word = False
                else:
                    node.children.pop(child_node.word)
            Trie.prune_node(child_node,threshold)

                
    def rescale_weight(self,func):
        """
        given a trie and a function,rescale the weight and max_children_weight
        on all nodes in trie according to function
        
        @input: trie, a function
        @output: trie with all weights updated according to given function 
        """
        node = self.root
        Trie.rescale_node_weight(node,func)
            
    def rescale_node_weight(node,func):
        """
        helper function for rescale_weight. Given node and function, rescale weight
        and max_children_weight of all children nodes, and repeat this for recursively 
        for all nodes below
        """
        for child_node in node.children.values():
            child_node.max_children_weight = func(child_node.max_children_weight)
            if child_node.end_of_word:
                child_node.weight = func(child_node.weight)
            Trie.rescale_node_weight(child_node,func)
        
        
  
    def createSuggestions(self,node,K):
        """
        starting from a desired node, add the node into a priority queue. if node 
        is an actual word, insert 1) with actual word weight and 2) with max_children_weight 
        (hence inserted twice). If node is not an actual word, insert with max_children_weight
        when inserting, insert it like to_visit.insert({node,node.end_of_word},node.weight)
        
        After inserting, everytime pop a top element from the prioirity queue, and
        call already_visited() to check if the node should be recorded in final_result
        
        Finally, the function will return final_result which is a list of K
        number of suggestions.
        
        @input: trie, node, K
        @return: a list with K number of suggestions

        """

        from PriorityQueue import PriorityQueue
        to_visit = PriorityQueue()
        list_of_matches = []
        
        if node.end_of_word and node.max_children_weight > node.weight:
            to_visit.insert(node, node.max_children_weight,False)
            to_visit.insert(node, node.weight, node.end_of_word)            
        else:
            to_visit.insert(node, node.max_children_weight,node.end_of_word)  
            
        while not to_visit.is_empty() and len(list_of_matches) < K :
            current_node, state = to_visit.extract_highest()
            if state:
                list_of_matches.append((current_node.weight, current_node.word))
            for child_node in current_node.children.values(): 
                if child_node.end_of_word and child_node.max_children_weight > child_node.weight:
                    to_visit.insert(child_node, child_node.max_children_weight, False)
                    to_visit.insert(child_node, child_node.weight, child_node.end_of_word)
                else:
                    to_visit.insert(child_node, child_node.max_children_weight, child_node.end_of_word)
            
                
        return list_of_matches
                    
   

def read_terms(filename):
    """
    read the file, stores each line in an array. For each element in the array, 
    split the string into keyword and weight, then call Trie.insert(keyword,weight)
    @input: file
    @output: Trie
    """
    word_trie = Trie()
    array = []
    with open(filename, "r", encoding="utf-8") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))  
    
    for element in array[1:]:
        weight = int(element.split(None,1)[0])
        word = element.split(None,1)[1]
        Trie.insert(word_trie,word,weight)
        
    return word_trie



def autocomplete(prefix,word_trie,num_of_suggestion):

    """
    using the word_trie that was constructed by read_terms, first call .search() to 
    locate the exact node that is that prefix word, then call createSuggestions() on that node to get 
    the list matching children nodes, and finally pop num_of_suggestion elements from that list
    
    @input: prefix, trie constructed by read_terms, number of suggestions
    @output: list of final suggestions
    """
    
    node_of_prefix = Trie.search(word_trie,prefix)
    if node_of_prefix == []:
        suggestions = "Prefix does not exist, try again"
    else:
        suggestions = Trie.createSuggestions(word_trie,node_of_prefix,num_of_suggestion)
        return suggestions

