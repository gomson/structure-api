
import os
from nose.tools import eq_, ok_
import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, APISimpleTestCase

from .models import NeoBaseNode, NeoDependencyRelation
from .serializers import BaseNodeSerializer


from neomodelstruct.models import NeoBaseNode, NeoDependencyRelation


# WORKING EXAMPLE   (because classes are defined in local context)
#
# from neomodel import (StructuredNode,
#                       StructuredRel,
#                       StringProperty,
#                       IntegerProperty,
#                       DateTimeProperty,
#                       RelationshipTo,
#                       RelationshipFrom)
# from pprint import pprint
# class DependencyRel(StructuredRel):
#     reason = StringProperty()
#     
# class Course(StructuredNode):
#     name = StringProperty()
#     prerequisites = RelationshipTo('Course', 'prerequisite', model=DependencyRel)
#     usedfors      = RelationshipFrom('Course', 'prerequisite', model=DependencyRel)
# 
# n1 = Course(name='physics')
# n1.save()
# n2 = Course(name='math')
# n2.save()
# r12 = n1.prerequisites.connect(n2, {'reason':'math is needed for physics'})
# n1.prerequisites.all()
#
# unfortunately doesn't work with models defined in app/models so nevermind.



class TestCreateUpdateRetrieveNeoBaseNode(APISimpleTestCase): #APITestCase):

    def setUp(self):
        self._delete_all_testnodes()
        # print 'in setUp ...'
        client = APIClient()
        # http://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        # admin = User.objects.get(id=1)
        # client.force_login(urlresolvers

    def tearDown(self):
        self._delete_all_testnodes()
        
    def _delete_all_testnodes(self):
        all_nodes = NeoBaseNode.nodes.all()
        test_nodes = [n for n in all_nodes if n.path.startswith('test/') ]
        for tn in test_nodes:
            tn.delete()

    def _create_test_node(self):
        nonce = str(random.randint(200,300))
        self._newpath = "test/path" + nonce
        nodedata = {
            "path": self._newpath,
            "scope": "minireftest",
            "version": "0.1",
            "comment": "Le comment",
        }
        url = reverse('neobasenode-list')
        response = self.client.post(url, nodedata, format='json')
        # print response.status_code, response.data['id'], response
        # print response.data
        self._nodeid = response.data['id']
        eq_(response.status_code, status.HTTP_201_CREATED, "Can't create.")

    def test_create_node(self):
        self._create_test_node()

    def test_update_node(self):
        self._create_test_node()
        # GET
        url = reverse('neobasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        # print response.status_code, response
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], self._newpath)
        # CHANGE
        putdata = response.data
        putdata['path'] = "test/updated_path"
        # PUT
        response = self.client.put(url, putdata, format='json')
        # print response.status_code, response
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], self._nodeid)
        eq_(response.data['path'], "test/updated_path")

    def test_retrieve_node(self):
        self._create_test_node()
        url = reverse('neobasenode-detail', kwargs={'uuid':self._nodeid})
        response = self.client.get(url, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        ok_(response.data['id'])
        eq_(response.data['path'], self._newpath)


