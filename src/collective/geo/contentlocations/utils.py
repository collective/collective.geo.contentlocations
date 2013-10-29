import pkg_resources

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True


def isDexterityContentType(obj):
    if HAS_DEXTERITY:
        from plone.dexterity.interfaces import IDexterityContent
        return IDexterityContent.providedBy(obj)
    return False
