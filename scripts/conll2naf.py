# coding: utf-8 
#!/usr/bin/env python

# This script reads a CoNLL ADEl output file and converts it to NAF XML 

# Date: 22 October 2015
# Author: Marieke van Erp  
# Contact: marieke.van.erp@vu.nl

import sys
import re
from KafNafParserPy import *

# Init KafNafParserobject
my_parser = KafNafParser(None, type='NAF')
my_parser.root.set('{http://www.w3.org/XML/1998/namespace}lang','en')
my_parser.root.set('version','v3')
textlayer = Ctext()
termlayer = Cterms()

offset = 0
num = 1 
rawtext = ''

conllfile = sys.argv[1]

lines = [line.rstrip('\n') for line in open(conllfile)]

sentence_number = 1
offset = 0
number = 1
entityno = 0
previous_links = ""
# Initialise text and term layers 
for line in lines:
    terms = line.split('\t')
    if len(terms) < 2:
        sentence_number = sentence_number + 1
        continue
    wf = Cwf()
    wf.set_id(str(number))
    wf.set_sent(str(sentence_number))
    wf.set_para("1")
    wf.set_offset(str(offset))
    # This is where we store the offset index with the token id 
    offset = offset + len(terms[0]) + 1
    wf.set_length(str(len(terms[0])))
    terms[0] = terms[0].decode('utf8')
    wf.set_text(terms[0])
    my_parser.add_wf(wf)
  #  term = Cterm()
  #  term.set_id(str(number))
  #  term.set_lemma(token)
  #  term_span = Cspan()
  #  term_target = Ctarget()
  #  term_target.set_id(str(num))
  #  term_span.add_target(term_target)
  #  term.set_span(term_span)
  #  my_parser.add_term(term)
    terms[1] = terms[1].rstrip()
    number = number + 1
    if terms[1] == "O":
        continue
    entity_comparison = terms[1] + terms[2]
    if entity_comparison == previous_links:
        span_range.append(str(number-1))
        previous_links = entity_comparison
    else:
        # store the last entity and start a new one
        previous_links = entity_comparison
        try:
            my_parser.add_entity(entity)
            reference_span = Cspan()
            span_target = Ctarget()
            reference_span.add_target(span_target)
            targets = []
            for item in span_range:
                for word_obj in my_parser.get_tokens():
                    if word_obj.get_id() == str(item):
                        targets.append(str(item))
            reference_span.add_target(span_target)
            span_targets = targets
            reference.add_span(span_targets)            
            entity.add_reference(reference)
        except:
            pass
        entity = Centity()
        entity.set_id(str(entityno))
        terms[1] = terms[1].rstrip()
        entity.set_type(terms[1])
        externalreferenceslayer = CexternalReferences()
        for item in range(2, len(terms) - 1, 1):
            parts = terms[item].split(';')
            new_ext_reference = CexternalReference()
            new_ext_reference.set_resource('byADEL')
            try:
                new_ext_reference.set_reference(parts[0])
                new_ext_reference.set_confidence(parts[len(parts)-1])
                entity.add_external_reference(new_ext_reference)
            except:
                pass
        reference = Creferences()
        span_range = []
        span_range.append(str(number-1))
        entityno = entityno + 1
    
# Print the whole thing
my_parser.dump()
    
    