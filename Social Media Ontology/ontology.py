from owlready import *
import ast
import string
import random

onto_path.append("/media/sheetal/New Volume/Major Project/Social Media Ontology")
base_irri = 'http://aaa-mp.org/'
onto = Ontology(base_irri+'social_onto.owl')

rel_prefix = 'REL'
loc_prefix = 'GPE'
person_prefix = 'PER'
org_prefix = 'ORG'
political_group_prefix = 'GPE'
time_prefix = 'TIM'
img_prefix = 'IMG'

class Entity(Thing):
    ontology = onto

class Event(Thing):
    ontology = onto

class is_associated_with(Property):
    ontology = onto
    domain = [Entity]
    range = [Event]

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


def add_new_tuple(new_tuple):
    entities = list()
    for item in new_tuple:
        if not item.startswith(rel_prefix):
            entities.append(fetch_entity(item))
    if entities:
        entities.reverse()
        root_entity = entities.pop()
        for entity in entities:
            root_entity.is_related_to.append(entity)

def fetch_entity(name):
    entity = None
    name = name.replace(' ', '_')
    for instance in Entity.instances():
        if instance.name == name:
            entity = instance
    if entity is None:
        entity = Entity(name)
    return entity


def add_quintuple(new_tuple, i):
    event_name = 'event_' + str(i)
    event = Event(event_name)
    prev = None
    r = 0
    for item in new_tuple:
        entity_type = item.split('-')[0]
        entity_names = item.split('-')[1:]
        entity_name = '-'.join(entity_names)
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
            add_quintuple(item, i+1)
            item_count += 1
    print('Read', item_count, 'tuples from file', filename)

add_tuples_from_file("testinput.txt")
onto.save()
#print(to_owl(onto))