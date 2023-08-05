import logging
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

import pkg_resources

try:
    pkg_resources.get_distribution("Products.Archetypes")
except pkg_resources.DistributionNotFound:
    HAS_ARCHETYPES = False
else:
    HAS_ARCHETYPES = True
    from Products.Archetypes.CatalogMultiplex import CatalogMultiplex

logger = logging.getLogger(__name__)


def indexObject(self, *args, **kwargs):
    logger.debug("Ignoring indexObject call.")


def unindexObject(self, *args, **kwargs):
    logger.debug("Ignoring unindexObject call.")


def reindexObject(self, *args, **kwargs):
    logger.debug("Ignoring reindexObject call.")


catalogMultiplexMethods = {}
catalogAwareMethods = {}

TO_PATCH = [(CMFCatalogAware, catalogAwareMethods)]
if HAS_ARCHETYPES:
    TO_PATCH.append((CatalogMultiplex, catalogMultiplexMethods))


def apply(reindex=True, index=True, unindex=True):
    # Hook up the new methods.
    for module, container in TO_PATCH:
        if not container:
            container.update({
                'index': module.indexObject,
                'reindex': module.reindexObject,
                'unindex': module.unindexObject,
            })
            if index:
                module.indexObject = indexObject
                logger.info('index patched %s', str(module.indexObject))
            if reindex:
                module.reindexObject = reindexObject
                logger.info('reindex patched %s', str(module.reindexObject))
            if unindex:
                module.unindexObject = unindexObject
                logger.info('unindex patched %s', str(module.unindexObject))
            logger.warn('Indexing operations will be ignored from now on.')


def unapply():
    # Hook up the old methods.
    for module, container in TO_PATCH:
        if not container:
            continue
        # We use 'pop' to make the dictionary empty again.
        module.indexObject = container.pop('index')
        module.reindexObject = container.pop('reindex')
        module.unindexObject = container.pop('unindex')
        logger.info('unpatched %s', str(module.indexObject))
        logger.info('unpatched %s', str(module.reindexObject))
        logger.info('unpatched %s', str(module.unindexObject))
        logger.warn('Indexing operations will be resumed from now on.')
