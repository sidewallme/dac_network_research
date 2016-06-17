import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import listdir
from os.path import isfile, join
import json
import sys


import os

BASE_URL = "http://www.scopus.com"


def getReferences(title):
  references = []
  # start a new instance of Firefox
  driver = webdriver.Firefox()
  driver.get(BASE_URL)
  #try:
  # search for the paper on scopus
  elem = driver.find_element_by_id("searchterm1")
  print elem
  elem.send_keys(title)
  elem.send_keys(Keys.ENTER)
  time.sleep(2)
  # go through the search results
  paper_results_list = driver.find_elements_by_class_name("dataCol2") # list of papers
  conference_results_list = driver.find_elements_by_class_name("dataCol5")  # where the corresponding paper was presented
  i = 0
  for paper in paper_results_list:
    conf_presented = conference_results_list[i].text
    try:
      if(((conf_presented.find("DETC") > -1) and (conf_presented.find("Proceedings") > -1)) or ((conf_presented.find("ASME") > -1) and (conf_presented.find("Proceedings") > -1)) or (conf_presented.find("International Design Engineering Technical Conferences and Computers and Information in Engineering") > -1)):
        #print(conf_presented)
        paper.find_element_by_tag_name("a").click()
        break
    except ValueError:
        i += 1
        continue
    i += 1
  time.sleep(2)

  #reference_list = driver.find_element_by_class_name("referenceLists")
  reference_blks = driver.find_elements_by_class_name("referencesBlk")
  #print("found ", len(reference_blks))
  for reference_blk in reference_blks:
    reference_title = ''
    try:
      ref_title = reference_blk.find_element_by_class_name("refDocTitle")
      reference_title = ref_title.find_element_by_tag_name('a').text
    except Exception as e:
      print e
      try:
        reference_title = reference_blk.find_element_by_tag_name('em').text
      except Exception as e1:
        print e1
        #print("Didn't find 'em' tag")
        continue
    references.append(reference_title)
  #finally:
  driver.close()
  # return the list of references
  return references

def processPapers():
  infile = sys.argv[1]
  outfile = sys.argv[2]
  citations = []
  papers = json.load(open(infile, 'r'))
  with open(outfile, 'w') as outfile:
    for paper in papers:
      title = paper['Title']
      print title
      entry = paper.copy()
      entry['References'] = []
      refs = getReferences(title)
      print refs
      for ref in refs:
        if len(ref)>1:
          entry['References'].append(ref)
      citations.append(entry)
      break
    json.dump(citations,outfile,indent=4)

processPapers()


