#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import listdir
from os.path import isfile, join
from termcolor import colored
import json
import sys
import codecs
import atexit


import os

BASE_URL = "http://www.scopus.com"
driver = None

def edit(sa, sb):
  la=len(sa)
  lb=len(sb)
  if la*lb == 0:
    return la+lb
  m = [[0 for j in range(lb+1)] for i in range(la+1)]
  m[0] = [i for i in range(lb+1)]
  for i in range(la, -1, -1):
    m[i][0] = i
  for i in range(1,la+1):
    for j in range(1, lb+1):
      rem = m[i-1][j]+1
      ins = m[i][j-1]+1
      sub = m[i-1][j-1]if sa[i-1]==sb[j-1] else m[i-1][j-1]+1
      m[i][j] = min(rem,ins,sub)
  return m[la][lb]

def check(ta, tb):
  ta = (ta.lower()).strip()
  tb = (tb.lower()).strip()
  w = (' '.join([ta,tb])).split(' ')
  try:
    ml = max([len(x) for x in w])+2
  except Exception:
    ml = 2
  dist = edit(ta, tb)
  return dist<=ml




def getReferences(title):
  global driver
  try:
    title = title.encode('ascii', 'ignore')
  except Exception:
    pass
  references = []
  # start a new instance of Firefox
  driver = webdriver.Firefox()
  driver.get(BASE_URL)
  #try:
  # search for the paper on scopus
  elem = driver.find_element_by_id("searchterm1")
  elem.send_keys(title)
  elem.send_keys(Keys.ENTER)
  time.sleep(2)
  # go through the search results
  paper_results_list = driver.find_elements_by_class_name("dataCol2") # list of papers
  # conference_results_list = driver.find_elements_by_class_name("dataCol5")  # where the corresponding paper was presented
  found = False
  for paper in paper_results_list:
    try:
      title_link = paper.find_element_by_tag_name("a")
      current_title = title_link.text
      try:
        current_title = current_title.encode('ascii', 'ignore')
      except Exception:
        pass
      print '{}'.format(current_title)
      if check(title,current_title):
        print colored('FOUND: {}'.format(current_title),'blue')
        title_link.click()
        found = True
        break
    except Exception:
        continue
  if not found:
    print colored('NOT FOUND: {}'.format(title),'red')
    driver.close()
    return []
  while len(driver.find_elements_by_id('recordPageFormId'))==0:
    pass
  reference_blks = driver.find_elements_by_class_name("referencesBlk")
  print colored("found {}".format(len(reference_blks)),'red')
  for reference_blk in reference_blks:
    reference_title = ''
    try:
      ref_title = reference_blk.find_element_by_class_name("refDocTitle")
      reference_title = ref_title.find_element_by_tag_name('a').text
    except Exception:
      continue
    print colored(reference_title,'cyan')
    references.append(reference_title)
  # return the list of references
  return references

if __name__ == '__main__':
  infile = sys.argv[1]
  outfile = sys.argv[2]
  citations = []
  def exitfunc():
    if driver:
      driver.close()
  atexit.register(exitfunc)
  papers = json.load(codecs.open(infile, 'r',encoding='utf-8'))
  with codecs.open(outfile, 'w',encoding='utf-8') as outfile:
    for paper in papers:
      title = paper['Title']
      print colored(title,'green')
      entry = paper.copy()
      entry['References'] = []
      refs = getReferences(title)
      if len(refs) == 0:
        continue
      for ref in refs:
        if len(ref)>1:
          entry['References'].append(ref)
      citations.append(entry)
      driver.close()
      driver = None
      #break
    json.dump(citations,outfile,indent=4)
  if driver:
    driver.close()





