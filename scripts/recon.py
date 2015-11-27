#!/usr/bin/python

"""
Domain model for NED, NewsReader project.

@author: U{Filip Ilievski<filipilievski.wordpress.com>}
@author: U{Antske Fokkens<http://wordpress.let.vupr.nl/antske/>}
@version: 0.1
@contact: U{f.ilievski@vu.nl<mailto:f.ilievski@vu.nl>}
@contact: U{antske.fokkens@vu.nl<mailto:antske.fokkens@vu.nl>}
@since: 08-Jul-2015
"""

__version__ = '0.1'
__modified__ = '08Jul2015'
__author__ = 'Filip Ilievski, Antske Fokkens'

from KafNafParserPy import *
import os
import sys
import json
import time
sys.path.append('./')
from dbpediaEnquirerPy import *

##########################################################################################
################################### HELPER FUNCTIONS #####################################
##########################################################################################

def get_start_term(parser):
	# Find the start of sentence 2 (after title)
	for token in parser.get_tokens():
		if token.get_sent()=="2":
			token_after_title=int(token.get_id().replace("w", ""))
			break		
	# Process from sentence 2 on
	# First find the appropriate term where sentence 2 starts
	for term in parser.get_terms():
		target_ids=term.get_span().get_span_ids()
		if int(target_ids[0].replace("w", ""))>=token_after_title:
			term_after_title=int(term.get_id().replace("t", ""))
			break
	return term_after_title

def get_most_confident_link(e, filename):
	maxconf=-0.1
	maxref=None
	for ref in e.get_external_references():
		try:
			if ref.get_resource()=="byADEL" and float(ref.get_confidence())>maxconf:
				maxconf=float(ref.get_confidence())
				maxref=ref.get_reference()
		except:
			w_err.write(filename + " " + ref.get_confidence() + "\n")
			maxref=None
			break
	return maxref

def get_entity_terms(entity):
	for ref in entity.get_references():
		terms=ref.get_span().get_span_ids()
	return terms
		

def get_terms_mention(parser, terms):
    	term_text=[]
	c=0
	new_terms=terms
	for tid in terms:
		c+=1
		word=parser.get_token(tid).get_text()
		if (c==1 or c==len(terms)) and (word=="'" or word=="''" or word=="\""):
			new_terms.remove(tid)
			continue
		term_text.append(word)
        res=(" ").join(term_text)
	return res, new_terms

def get_entity_mention(parser, entity):
	terms=get_entity_terms(entity)
	return get_terms_mention(parser, terms)

def get_initials(entity_string):
	initials=""
	ent_split=entity_string.split()
	if len(ent_split)>1:
		for word in ent_split:
			#if word.isupper():
			#	initials+=word
			if word[0].isupper():
				initials+=word[0]
	else:
		initials=None
	return initials

def is_person(dblink):
	return not dblink or my_dbpedia.is_person(dblink)

def add_entity_extref(entity, extref):
	my_ext_ref = CexternalReference()
	my_ext_ref.set_reference(extref)
	my_ext_ref.set_resource('domain_model')
	my_ext_ref.set_confidence('1.0')
	entity.add_external_reference(my_ext_ref)
	return entity

def prestore_terms_and_tokens(parser):
	global term_sentences
	term_sentences={}
	for token in parser.get_tokens():
		token_id=token.get_id()
		term_sentences[token_id]=token.get_sent()

##########################################################################################
#################################### Recognition #########################################
##########################################################################################

def extend_string_with_numbers_and_nnps(entity_string, ts, parser):
	sentence=term_sentences[ts[0]]
	begin=int(ts[0].replace("t",""))
	end=int(ts[len(ts)-1].replace("t", ""))
	new_terms=list(ts)
	num_terms=len(term_sentences)
	# prepend
	ext_string=""

	# Append
	ext_string= ext_string.strip() + " " + entity_string
	temp=end
	while True:
		temp+=1
		if temp>num_terms:
			break
		new_term="t" + str(temp)
		try:
			addition, added_terms = get_terms_mention(parser, [new_term])
			if term_sentences[new_term]==sentence and (parser.get_term(new_term).get_pos() in ["NNP", "NNPS"] or (addition!="" and addition.isdigit())):
				ext_string =  ext_string + " " + addition
				new_terms.append(new_term)
			else:
				break
		except KeyError: #out of bounds
			break
	return ext_string.strip(), new_terms


##########################################################################################
####################################### MODULES ##########################################
##########################################################################################

def get_most_specific_type(entity):
	dominant_link=get_most_confident_link(entity, "")
	return my_dbpedia.get_deepest_ontology_class_for_dblink(dominant_link)

def type_fits(ent_type, dblink):
	return True
	if ent_type and ent_type!="MISC" and ent_type.strip()!="":
	    if ent_type=="ORGANIZATION":
		ent_type="http://dbpedia.org/ontology/Organisation"
	    elif ent_type=="PERSON":
		ent_type="http://dbpedia.org/ontology/Person"
	    elif ent_type=="LOCATION":
		ent_type="http://dbpedia.org/ontology/Place"
	    link_types=my_dbpedia.get_dbpedia_ontology_labels_for_dblink(dblink)
	    return (ent_type in link_types)
	elif ent_type=="MISC":
	    link_types=my_dbpedia.get_dbpedia_ontology_labels_for_dblink(dblink)
	    return ("http://dbpedia.org/ontology/Organisation" not in link_types) and ("http://dbpedia.org/ontology/Place" not in link_types) and ("http://dbpedia.org/ontology/Person" not in link_types)
	else:
	    return True

def get_previous_occurrence(e, all_entities, entity_string): #1
	other_ref=None

	for ent in all_entities:
		if e!=ent and ((int(e["eid"]>int(ent["eid"])) and (e["title"] is ent["title"])) or (e["title"] and not ent["title"])):
		# Entities that are different AND either (entities that passed from the same text type (main or title) OR entities in title)

			ekey=None
			if ent["original"]["extref"] or ent["original"]["nwr_extref"]:
				ekey=ent["original"]["mention"].lower()
				
				if entity_string==ekey: 
					other_ref=ent["original"]["extref"]
					if other_ref:
						break
				elif entity_string in ekey.split():

					if ent["original"]["extref"] is not None: 
						this_extref=ent["original"]["extref"]
					else: # NOTE: THIS SHOULD NEVER BE THE CASE
						this_extref=ent["original"]["nwr_extref"]
					if is_person(this_extref):
						other_ref=this_extref
						if other_ref:
							break
	return other_ref

def solve_initials_and_abbreviations(entity, entity_string, all_entities): #3
	#2 Initials and abbreviations
	extref=None
	for other_entity in all_entities:
		if other_entity!=entity:
			if other_entity["original"]["extref"]:
				initials=other_entity["original"]["initials"]
				other_ref=other_entity["original"]["extref"]
				if entity_string==initials:
					extref=other_ref
			else:
				initials=other_entity["original"]["initials"]
				other_ref=other_entity["original"]["nwr_extref"]
				if entity_string==initials:
					extref=other_ref
	return extref

def do_disambiguation(entity, entity_string, all_entities):
			
	extref=get_previous_occurrence(entity, all_entities, entity_string.lower()); #D1  Get previous occurrence

	if not extref or not type_fits(entity["type"], extref):
		if len(entity_string.split())==1 and entity_string.replace(".","").isupper(): # If one term, all-upper, then it may be an abbreviation
			extref = solve_initials_and_abbreviations(entity, entity_string.replace(".", ""), all_entities)
	if type_fits(entity["type"], extref):
		return extref
	else:
		return None

def occurred_in_article(extname, all_entities):
	for ent in all_entities:
		if extname==ent["original"]["mention"]:
			return ent["original"]["nwr_extref"]
		
def get_from_es(pattern, type):
	max_occurrences=0
	best_candidate=None
	total=0
	if pattern in lemma_to_entity:
		for candidate in lemma_to_entity[pattern]:
			num_occurrences=lemma_to_entity[pattern][candidate]
			if num_occurrences>max_occurrences:
				max_occurrences=lemma_to_entity[pattern][candidate]
				best_candidate=candidate
			total+=num_occurrences
		if max_occurrences>10 and max_occurrences/float(total)>=0.5 and type_fits(type, best_candidate):			
			return best_candidate
		else:
			return None
	return None
				
def create_dbpedia_uri(t):
	dburl="http://dbpedia.org/resource/" + t.replace(" ", "_")
	return dburl

def get_from_dbpedia(mention):
	dblink=create_dbpedia_uri(e["extended"]["mention"])
	results=my_dbpedia.query_dbpedia_for_unique_dblink(dblink)
	return dblink if (results is not None and len(results)>0) else None

##########################################################################################
####################################### MAIN #############################################
##########################################################################################

global term_sentences

global lemma_to_entity

fname="lemma.json"
f=open(fname, "r")

w_err=open("errors_file.log", "w")

for line in f:
        lemma_to_entity=json.loads(line)

if __name__=="__main__":

	if len(sys.argv)<2:
		print "Please specify input file"
		sys.exit(1)
    #changed: using stdin now
    #file=sys.stdin
#	file=open("/Users/filipilievski/Processed/corpus_airbus/3835_Chinese_airlines_agree_purchase_of_Boeing_787_Dreamliners.naf", "r")
	#get begin time
	begintime = time.strftime('%Y-%m-%dT%H:%M:%S%Z')

	#if len(sys.argv)>1: # Local instance is specified
	#	my_dbpedia = Cdbpedia_enquirer(sys.argv[1])		
	#else: # default remote dbpedia
	my_dbpedia = Cdbpedia_enquirer()
	#path="NWR_EvalSet/"
	#path="eval_corpus/"
	#out_path="POCUS_EvalSet/"
	path="ADEL/" + sys.argv[1] + "/"
	count_all = 0
	count_dis=0
	reranks=0
	
	s=0
    	for file in os.listdir(path):
		print file
		if not file.endswith(".naf"):
			continue
		parser=KafNafParser(path + file)
	    	#putting the actual process in a try, except
	    	#if this module breaks it should return the original naf file (and print a warning)
		prestore_terms_and_tokens(parser)
	
		#we're using stdin now
		out_file="RECON/" + sys.argv[1] + "/" + file

		

		all_entities=[]
		max_id=0
		for entity in parser.get_entities():
			if int(entity.get_id())>max_id:
				max_id=int(entity.get_id())
			entity_string, terms = get_entity_mention(parser, entity)
			if int(term_sentences[terms[0]])>6:
				continue
			# Normalization step
			if len(terms)==1 and entity_string.endswith("-based"):
				norm_entity_string=entity_string[:-6]
			else:
				norm_entity_string=entity_string
		
			istitle = (term_sentences[terms[0]]=="1")
		
			entity_entry = {"eid": entity.get_id(), "type": entity.get_type() or get_most_specific_type(entity), "original": {"raw": entity_string, "mention": norm_entity_string, "terms": terms, "nwr_extref": get_most_confident_link(entity, file), "extref": None, "initials": get_initials(norm_entity_string)}, "title": istitle}
		
			all_entities.append(entity_entry)
		s+=len(all_entities)
		for consider_title_entities in [False, True]:
			#for e in all_entities:
			#	if e["title"] is consider_title_entities: # 1) Extended mention - This line ensures title entities get processed in a second iteration
				#	if "extended" in e: # 1) extension
						#e["extended"]["extref"]=occurred_in_article(e["extended"]["mention"], all_entities) or get_from_es(e["extended"]["mention"]) or get_from_dbpedia(e["extended"]["mention"]) # TODO: Try without ES
				#		e["extended"]["extref"]=occurred_in_article(e["extended"]["mention"], all_entities) or get_from_es(e["extended"]["mention"]) or get_from_dbpedia(e["extended"]["mention"]) # TODO: Try without ES
		
			for e in all_entities:
				if e["title"] is consider_title_entities: # 2) original mention	 - This line ensures title entities get processed in a second iteration	
#					e["original"]["extref"]=do_disambiguation(e, e["original"]["mention"], all_entities) # or get_from_es(e["original"]["mention"], e["type"]) # TODO: Try without ES
                                        e["original"]["extref"]=get_from_es(e["original"]["mention"], e["type"]) # TODO: Try without ES

			for e in all_entities:
				if e["title"] is consider_title_entities: # 3) original mention, last resort - This line ensures title entities get processed in a second iteration

					if e["original"]["extref"] is None: # TODO: Maybe Enable this block later!
						#if consider_title_entities:
						#	e["original"]["extref"]="--NME--"
						#else:
						e["original"]["extref"]=e["original"]["nwr_extref"]
					else:
						reranks+=1
				
		for e in all_entities:
			sextref=""
			mention=""
			single=True
			if e["original"]["extref"]:
				sextref=e["original"]["extref"]
				mention=e["original"]["mention"]
						
				ext_ref = CexternalReference()
				ext_ref.set_resource("dbp")
				ext_ref.set_source("ReCon")
				ext_ref.set_reference(sextref)
				ext_ref.set_confidence("1.0")
			
				parser.add_external_reference_to_entity(e["eid"], ext_ref)

	
			
		parser.dump(out_file)
	print reranks
