# get only crime relevant data, by comparing REL and proper nouns

from owlready import *
import ast
import string
import random
import nltk
from nltk.corpus import wordnet
import re, math
from collections import Counter
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import urllib
import cv2
import numpy as np
from skimage.transform import resize
from skimage.io import imread
from skimage import color
import urllib.request
import numpy as np
import urllib
import cv2
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
WORD = re.compile( r'\w+' )
# base_irri = 'http://aaa-mp.org/'
# onto = Ontology('onto.owl')

onto_path.append("/media/sheetal/New Volume/Major Project/Combined Ontology")
base_irri = 'http://aaa-mp.org/'

onto = Ontology(base_irri+'combined_onto.owl')
rel_prefix = 'REL'
rel_weight = 0.1
loc_prefix = 'GPE'
loc_weight = 0.1
person_prefix = 'PER'
person_weight = 0.25
org_prefix = 'ORG'
org_weight = 0.25
political_group_prefix = 'GPE'
time_prefix = 'TIM'
img_prefix = 'IMG'
img_weight = 0.3
rm_prefix = 'RM'

red = [1.0, 0., 0., 0.6]
blue = [0., 0., 1.0, 0.6]
yellow = [1., 1., 0., 0.6]
white = [1., 1., 1., 1]
class Entity(Thing):
    ontology = onto
    color = None

class Event(Thing):
    ontology = onto

class is_associated_with(Property):
    ontology = onto
    domain = [Entity]
    range = [Event]

class Relevance(Thing):
    ontology = onto

class weight(FunctionalProperty):
    ontology = onto
    domain = [Relevance]
    range = [str]

class source(Property):
    ontology = onto
    domain = [Relevance]
    range = [Event]

class dest(Property):
    ontology = onto
    domain = [Relevance]
    range = [Entity]

class org(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with

class person(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with

class image(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with
  
class location(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with

class time(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with
    
class action(Property):
    ontology = onto
    domain = [Entity]
    range = [Entity]
    
    
class subjects(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with

      
def fetch_entity(name):
    entity = None
    name = name.replace(' ', '_')
    for instance in Entity.instances():
        if instance.name == name:
            entity = instance
    if entity is None:
        entity = Entity(name)
    return entity

def match_synonymn(social_entity_name, news_entity_name):
    synonyms = []
 
    for syn in wordnet.synsets(news_entity_name):
        for l in syn.lemmas():
            synonyms.append(l.name())
    if(social_entity_name in synonyms):
        return 1
    return 0
 


def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    return Counter(WORD.findall(text))

def match_string(a,b):
    a = text_to_vector(a.strip().lower())
    b = text_to_vector(b.strip().lower())
    if(get_cosine(a, b)>=0.4):
        return 1
    else:
        return 0
    


def match_image(social_entity_name, news_entity_name):
    print(social_entity_name)
    print(news_entity_name)

    req = urllib.request.Request(social_entity_name, headers={'User-Agent' : "Magic Browser"}) 
    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    imageA = cv2.imdecode(image, cv2.IMREAD_COLOR) 

    req = urllib.request.Request(news_entity_name, headers={'User-Agent' : "Magic Browser"}) 
    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    imageB = cv2.imdecode(image, cv2.IMREAD_COLOR) 

    imageA = resize(imageA, (256, 256, 3))
    imageB = resize(imageB, (256, 256, 3))
    s = ssim(color.rgb2gray(imageA), color.rgb2gray(imageB))
    if(s>0.8):
        return 1
    else:
        return 0

def add_quintuple(news_tuple, i, j):
    total_weight = 0
    threshold = 0.25
    flag = 0
    prev = None
    r = 0
    event = Event('event_'+str(i)+'_'+str(j))
    for item in news_tuple:
        entity_type = item.split('-')[0]
        entity_names = item.split('-')[1:]
        entity_name = '-'.join(entity_names)
        if(entity_type == rm_prefix):
            entity = event.image[0]
            relevance = Relevance()
            relevance.weight = entity_name
            relevance.source = [event]
            relevance.dest = [entity]
        else:
            if(entity_type != rel_prefix):
                entity = fetch_entity(entity_name)
                entity.color = red
            if(entity_type == rel_prefix):
                if prev is not None:
                    # prev.action.append(entity)
                    rel = entity_name
                    r = 1
            elif(entity_type == loc_prefix):
                event.location.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    rel.color = white
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == time_prefix):
                event.time.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    rel.color = white
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == img_prefix):
                event.image.append(entity)
            elif(entity_type == person_prefix):
                event.person.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    rel.color = white
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == org_prefix):
                event.org.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    rel.color = white
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            else:
                event.subjects.append(entity)
            if(entity_type != rel_prefix):
                prev = entity


    f1 = open("social_input.txt", 'r')
    for line in f1.readlines():
        l = ast.literal_eval(line)
        for social_tuple in l:
            total_weight = 0
            for attr in news_tuple:
                news_entity_type = attr.split('-')[0]
                news_entity_name = attr.split('-')[1:]  
                news_entity_name = '-'.join(news_entity_name)
                for item in social_tuple:
                    social_entity_type = item.split('-')[0]
                    social_entity_name = item.split('-')[1:]
                    social_entity_name = '-'.join(social_entity_name)
                    if(social_entity_type == rel_prefix and news_entity_type == rel_prefix):
                        total_weight += rel_weight*match_synonymn(social_entity_name, news_entity_name)
                    if(social_entity_type == loc_prefix and news_entity_type == loc_prefix):
                        total_weight += loc_weight*match_string(social_entity_name, news_entity_name)
                    if(social_entity_type == person_prefix and news_entity_type == person_prefix):
                        total_weight += person_weight*match_string(social_entity_name, news_entity_name)
                    if(social_entity_type == org_prefix and news_entity_type == org_prefix):
                        total_weight += org_weight*match_string(social_entity_name, news_entity_name)
                    if(social_entity_type == img_prefix and news_entity_type == img_prefix):
                        total_weight += img_weight*match_image(social_entity_name, news_entity_name)
            print(total_weight)
            if(total_weight >= threshold):    
                for item in social_tuple:
                    entity_type = item.split('-')[0]
                    entity_names = item.split('-')[1:]
                    entity_name = '-'.join(entity_names)
                    if(entity_type != rel_prefix):
                        entity = fetch_entity(entity_name)
                        if entity.color == red:
                            entity.color = yellow
                        else:
                            entity.color = blue

                    if(entity_type == rel_prefix):
                        if prev is not None:
                            # prev.action.append(entity)
                            rel = entity_name
                            r = 1
                    elif(entity_type == loc_prefix):
                        event.location.append(entity)
                        if r==1:
                            rel=fetch_entity(rel)
                            rel.color = white
                            prev.action.append(rel)
                            entity.action.append(rel)
                        r = 0
                    elif(entity_type == time_prefix):
                        event.time.append(entity)
                        if r==1:
                            rel=fetch_entity(rel)
                            rel.color = white
                            prev.action.append(rel)
                            entity.action.append(rel)
                        r = 0
                    elif(entity_type == img_prefix):
                        event.image.append(entity)
                    elif(entity_type == person_prefix):
                        event.person.append(entity)
                        if r==1:
                            rel=fetch_entity(rel)
                            rel.color = white
                            prev.action.append(rel)
                            entity.action.append(rel)
                        r = 0
                    elif(entity_type == org_prefix):
                        event.org.append(entity)
                        if r==1:
                            rel=fetch_entity(rel)
                            rel.color = white
                            prev.action.append(rel)
                            entity.action.append(rel)
                        r = 0
                    else:
                        event.subjects.append(entity)
                    if(entity_type != rel_prefix):
                        prev = entity

def add_tuples_from_file(filename):
    f = open(filename, 'r')
    item_count = 0
    for i, line in enumerate(f.readlines()):
        l = ast.literal_eval(line)
        for j, item in enumerate(l):
            #add_new_tuple(item)
            add_quintuple(item, i+1, j+1)
            item_count += 1
    print('Read', item_count, 'tuples from file', filename)



