from zope.interface import implements
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory

from collective.geo.contentlocations import ContentLocationsMessageFactory as _
from collective.geo.contentlocations import COORDTYPE


class baseVocabulary(object):
    implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for term in self.terms:
            terms.append(vocabulary.SimpleVocabulary.createTerm(term[0],
                                                                term[0],
                                                                _(term[1])))

        return vocabulary.SimpleVocabulary(terms)


class coordsVocab(baseVocabulary):
    terms = COORDTYPE
