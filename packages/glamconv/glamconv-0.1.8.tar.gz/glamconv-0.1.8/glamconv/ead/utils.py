# -*- coding: utf-8 -*-
"""
Module defining several useful functions that will be used inside
the transform actions defined in the other modules of this sub-package.
"""

import re


NS = {
    'ead': 'urn:isbn:1-931666-22-9',
    'xlink': 'http://www.w3.org/1999/xlink',
}


QNAME_PATTERN = re.compile("({.*})?(.+)")


def split_qname(qname):
    namespace, local_name = QNAME_PATTERN.match(qname).groups()
    if namespace is not None:
        namespace = namespace[1:-1]
    if namespace == u"":
        namespace = None
    return namespace, local_name


def write_hierarchy(xml_elt):
    ancest = xml_elt.xpath("ancestor-or-self::*")
    hierarchy = u""
    for idx, elt in enumerate(ancest):
        hierarchy += "/{0}".format(elt.xpath("name()"))
        if elt.get(u"id"):
            hierarchy += u'[id="{0}"]'.format(elt.get(u"id"))
        elif idx != 0:
            xpath_expr = (u'count(preceding-sibling::{0})+1'
                          u''.format(elt.xpath("name()")))
            elt_index = int(elt.xpath(xpath_expr, namespaces=NS))
            xpath_expr = u'count(../{0})'.format(elt.xpath("name()"))
            max_index = int(elt.xpath(xpath_expr, namespaces=NS))
            if max_index > 1:
                hierarchy += u'[{0}]'.format(elt_index)
    return hierarchy


def log_element(xml_elt, attributes=None, text_content=False, msg=u""):
    log_entry = write_hierarchy(xml_elt)
    if msg:
        log_entry += u"\n    " + msg
    if attributes:
        log_entry += u"\n   "
        for attrname in attributes:
            attrval = xml_elt.xpath(u"string(@{0})".format(attrname),
                                    namespaces=NS)
            if len(attrval) == 0:
                continue
            if len(attrval) > 50:
                attrval = attrval[:47] + u"..."
            log_entry += u" {0}=\"{1}\"".format(attrname, attrval)
    if text_content:
        log_entry += u"\n    Text content: "
        txt = xml_elt.xpath(u"string()")
        if len(txt) > 50:
            txt = txt[:47] + u"..."
        log_entry += txt
    return log_entry


def suppress_element(xml_elt):
    parent = xml_elt.getparent()
    text = (xml_elt.text or u"") + (xml_elt.tail or u"")
    previous = xml_elt.getprevious()
    if previous is not None:
        previous.tail = (previous.tail or u"") + text
    else:
        parent.text = (parent.text or u"") + text
    parent.remove(xml_elt)


def add_text_around_element(xml_elt, before=u"", after=u""):
    previous = xml_elt.getprevious()
    parent = xml_elt.getparent()
    if before:
        if previous is not None:
            previous.tail = (previous.tail or u"") + before
        else:
            parent.text = (parent.text or u"") + before
    if after:
        xml_elt.tail = (xml_elt.tail or u"") + after


def adjust_content_in_mixed(xml_elt, keep_tags=tuple()):
    """
    Erase from ``xml_elt`` all the XML elements except those whose tag name
    is given in ``keep_tags`` tuple. The text inside ``xml_elt`` and its
    children is kept (even if the elements are removed).

    If an XML element must be kept, it is kept as it is (with all its
    sub-elements). Therefore, if you want to erase XML elements that can
    occur at several levels in the XML tree, you have to walk depth-first in
    the tree and call the function first from the bottom levels and upwards.
    """
    for child in xml_elt:
        if child.tag in keep_tags:
            # If child must be kept, keep it as it is and go to next child
            continue
        # Recursively call the same function to get all the text content from
        # child (``keep_tags`` is empty because we don't want to keep any
        # XML element from ``child`` that will not be kept).
        adjust_content_in_mixed(child, tuple())
        # Keep text content of ``child`` inside the element before ``child``
        child_text_content = (child.text or u"") + (child.tail or u"")
        if child_text_content:
            previous = child.getprevious()
            if previous is not None:
                previous.tail = (previous.tail or u"") + child_text_content
            else:
                xml_elt.text = (xml_elt.text or u"") + child_text_content
        # Finally, remove child from the XML tree
        xml_elt.remove(child)


def insert_child_at_element_beginning(xml_elt, child):
    if xml_elt.text is not None:
        child.tail = (child.tail or u"") + xml_elt.text
        xml_elt.text = None
    xml_elt.insert(0, child)


def insert_text_at_element_end(xml_elt, text):
    if not text:
        return
    if len(xml_elt) == 0:
        xml_elt.text = (xml_elt.text or u"") + text
    else:
        last_child = xml_elt[-1]
        last_child.tail = (last_child.tail or u"") + text


def insert_text_before_element(xml_elt, text):
    if not text:
        return
    prev = xml_elt.getprevious()
    if prev is None:
        parent = xml_elt.get_parent()
        parent.text = (parent.text or u"") + text
    else:
        prev.tail = (prev.tail or u"") + text
