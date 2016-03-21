#!/usr/bin/env python3

from KafNafParserPy import *
import sys

with open(sys.argv[1]) as f:
    content = f.readlines()
 
my_parser = KafNafParser(None, type='NAF')  
raw = '' 
outputfile = 'test.naf' 
wordcounter = 1 
offset = 0   
entity_counter = 0 
mycount=0
for item in content:
	if len(item) < 2:
	#	print item.rstrip(), " ", len(item)
		continue
	if '-DOCSTART-' in item:
		if len(raw) > 2:
			# Create the raw text layer 
			rawlayer = my_parser.set_raw(raw)
			raw = ''
			wordcounter = 1 
			offset = 0
			# print the NAF file
			my_parser.dump(outputfile)
	#	print "new document", item 
		parts = item.split(" ")
	#	print parts[1][1:]
		outputfile = parts[1][1:] + '.naf'
		
		# Init KafNafParserobject
		my_parser = KafNafParser(None, type='NAF')
		my_parser.root.set('{http://www.w3.org/XML/1998/namespace}lang','en')
		my_parser.root.set('version','v3')	
    
    	# Set the header
		header = my_parser.get_header()
		if header is None:
			#Create a new one
			header =  CHeader()
			my_parser.set_header(header)
		
		my_file_desc = header.get_fileDesc()
		if my_file_desc is None:
    		#Create a new one
			my_file_desc =  CfileDesc()
			header.set_fileDesc(my_file_desc)
        
			#Modify the attributes
			my_file_desc.set_title(parts[1][1:])
			my_file_desc.set_filename(parts[1][1:])
	#		my_file_desc.set_creationtime(data['publishedDate'])

	else:
		elements = item.split("\t")
		elements[0] = elements[0].rstrip()
		wf = Cwf() 
		wf.set_id(str(wordcounter))
		wf.set_sent("1")
		wf.set_para("1")
		wf.set_offset(str(offset))
		offset = offset + len(elements[0])
		wf.set_length(str(len(elements[0])))
		wf.set_text(elements[0])
		my_parser.add_wf(wf)
		term = Cterm()
		term.set_id(str(wordcounter))
		term.set_lemma(elements[0])
		term_span = Cspan()
		term_target = Ctarget()
		term_target.set_id(str(wordcounter))
		term_span.add_target(term_target)
		term.set_span(term_span)
		my_parser.add_term(term)
		raw = raw + elements[0] + " " 
		
		# This is where the entity layer will be created
		if len(elements) > 1 and 'B' in elements[1]:  
			entity = Centity()
			entity.set_id(str(entity_counter))
			externalreferenceslayer = CexternalReferences()
			new_ext_reference = CexternalReference()
			new_ext_reference.set_resource('GoldStandardAnnotation')
			if len(elements)>4 and '--NME--' not in elements[4]:
				try:
					new_ext_reference.set_reference(elements[4])	
				except:
					print(elements)
					pass
			else:
				mycount+=1
			new_ext_reference.set_confidence('1.0')
			entity.add_external_reference(new_ext_reference)
			my_parser.add_entity(entity)
			# Here there will be some magic to get the spans right 
			entity_parts = elements[2].split(' ')
			entity_span = []
			counter = wordcounter - 1 
			for x in entity_parts:
				counter = counter + 1 
				entity_span.append(str(counter))
			reference = Creferences()
			reference_span = Cspan()
			span_target = Ctarget()
			reference_span.add_target(span_target)
			span_targets = entity_span # this is a list with the target IDs 
			reference.add_span(span_targets)
			entity.add_reference(reference)
			entity_counter = entity_counter + 1 
		
		wordcounter = wordcounter + 1
print(mycount)
print(entity_counter)
