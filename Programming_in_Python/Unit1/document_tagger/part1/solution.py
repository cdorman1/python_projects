import re
import sys
from pg_sample_texts import DIV_COMM, MAG_CART
 
documents = [DIV_COMM, MAG_CART]
 
# PREPARE OUR REGEXES FOR METADATA SEARCHES #
# we'll use re.compile() here, which allows you to assign a regex pattern
# to a variable. We'll do this for each our metadata fields.
# 
# Also note how we're using paretheses to create two search groups. Looking
# at title_search, see how we use one group to match on the presence of "title:".
# 
# Also, note how in the second group is a named group -- we use ?p<name> .
# 
# Finally, note that we're passing the re.IGNORECASE flag as an optional
# argument to re.compile. We're doing this because it's human beings who create
# the metadata headers at the top of Project gutenberg docs, and we want to account 
# for possibility of "title: Some Title", "Title: Some Title", and "TITLE: Some Title").
title_search = re.compile(r"""
                         (?:title:\s*)
                         (?P<title>
                         (
                            (
                                \S*
                                (\ )?
                                
                                
                                
                            )+
                         )
                         (
                            (\n(\ )+)
                            (\S*(\ )?)*
                         )*
                         )""",  
                         re.VERBOSE | re.IGNORECASE)

author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)
 

kws = dict.fromkeys([kw for kw in sys.argv[1:]], None)

for kw in kws:
    kws[kw] = re.compile(r'\b' + kw + r'\b', re.IGNORECASE)         
    

# now iterate over the documents and extract and print output about metadata
# for each one. Note the use of enumerate here, which gives you a counter variable
# (in this case 'i') that keeps track of the index of the list (in this case documents)
# your currently on in your loop. You should memorize how enumerate works, and google it
# if you need more explanation. It's a highly productive built in function, and there are
# common problems that you'll encounter as a programmer that enumerate is great for.

for i, doc in enumerate(documents):
  author = re.search(author_search, doc)
  if author:
      author = author.group('author')
  translator = re.search(translator_search, doc)
  if translator:
    translator = translator.group('translator')
  illustrator = re.search(illustrator_search, doc)
  if illustrator:
      illustrator = illustrator.group('illustrator')
  title = re.search(title_search, doc).group('title')
  print "***" * 25
  print "Here's the info for doc {}:".format(i)
  print "Title: {}".format(title)
  print "Author(s): {}".format(author)
  print "Translator(s): {}".format(translator)
  print "Illustrator(s): {}".format(illustrator)
  print "\n****KEYWORD REPORT****\n\n"

  for kw in kws:
      print "\"{0}\": {1}".format(kw, len(re.findall(kws[kw], doc)))
  print '\n\n'

 

