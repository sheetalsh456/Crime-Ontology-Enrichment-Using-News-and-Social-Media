from owlready import *
import ast
import string
import random

onto_path.append("/media/sheetal/New Volume/Major Project/Newspaper Ontology")
base_irri = 'http://aaa-mp.org/'

onto = Ontology(base_irri+'news_onto.owl')

rel_prefix = 'REL'
loc_prefix = 'GPE'
person_prefix = 'PER'
org_prefix = 'ORG'
political_group_prefix = 'GPE'
time_prefix = 'TIM'
img_prefix = 'IMG'
rm_prefix = 'RM'

class Entity(Thing):
    ontology = onto

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

class person(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with

class org(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with
    
class action(Property):
    ontology = onto
    domain = [Entity]
    range = [Entity]
    
class image(Property):
    ontology = onto
    domain = [Event]
    range = [Entity]
    inverse_property = is_associated_with



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
            break
    if entity is None:
        entity = Entity(name)
    return entity

def add_quintuple(new_tuple, i, j):
    event = Event('event_'+str(i)+'_'+str(j))
    prev = None
    r = 0
    for item in new_tuple:
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
            if(entity_type == rel_prefix):
                if prev is not None:
                    # prev.action.append(entity)
                    rel = entity_name
                    r = 1
            elif(entity_type == loc_prefix):
                event.location.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == time_prefix):
                event.time.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == img_prefix):
                event.image.append(entity)
            elif(entity_type == person_prefix):
                event.person.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
                    prev.action.append(rel)
                    entity.action.append(rel)
                r = 0
            elif(entity_type == org_prefix):
                event.org.append(entity)
                if r==1:
                    rel=fetch_entity(rel)
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
            add_quintuple(item, i+1, j+1)
            item_count += 1
    print('Read', item_count, 'tuples from file', filename)

add_tuples_from_file("testinput.txt")
onto.save()
#print(to_owl(onto))