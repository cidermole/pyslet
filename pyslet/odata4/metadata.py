#! /usr/bin/env python

from . import model as odata
from ..py2 import (
    is_text,
    to_text
    )
from ..rfc2396 import URI
from ..xml import namespace as xmlns
from ..xml import structures as xml
from ..xml import xsdatatypes as xsi


PACKAGING_NAMESPACE = 'http://docs.oasis-open.org/odata/ns/edmx'
EDMX1_NAMESPACE = 'http://schemas.microsoft.com/ado/2007/06/edmx'
EDM_NAMESPACE = 'http://docs.oasis-open.org/odata/ns/edm'

_edmx_version = {
    PACKAGING_NAMESPACE: (4, 0),
    EDMX1_NAMESPACE: (1, 0)
    }


def edmx_version(ns):
    if is_text(ns):
        ns = URI.from_octets(ns)
    if not isinstance(ns, URI):
        raise TypeError
    ns = ns.canonicalize()
    return _edmx_version.get(str(ns), None)


EDM10_NAMESPACE = 'http://schemas.microsoft.com/ado/2006/04/edm'
EDM11_NAMESPACE = 'http://schemas.microsoft.com/ado/2007/05/edm'
EDM12_NAMESPACE = 'http://schemas.microsoft.com/ado/2008/01/edm'
EDM20_NAMESPACE = 'http://schemas.microsoft.com/ado/2008/09/edm'
EDM30_NAMESPACE = 'http://schemas.microsoft.com/ado/2009/11/edm'

_edm_version = {
    EDM_NAMESPACE: (4, 0),
    EDM30_NAMESPACE: (3, 0),
    EDM20_NAMESPACE: (2, 0),
    EDM12_NAMESPACE: (1, 2),
    EDM11_NAMESPACE: (1, 1),
    EDM10_NAMESPACE: (1, 0)
    }


def edm_version(ns):
    if is_text(ns):
        ns = URI.from_octets(ns)
    if not isinstance(ns, URI):
        raise TypeError
    ns = ns.canonicalize()
    return _edm_version.get(str(ns), None)


def validate_simple_identifier(value):
    if odata.NameTable.is_simple_identifier(value):
        return value
    else:
        raise ValueError(
            "Can't parse SimpleIdentifier from :%s" % repr(value))


def validate_namespace(value):
    if odata.NameTable.is_namespace(value):
        return value
    else:
        raise ValueError(
            "Can't parse Namespace from :%s" % repr(value))


def validate_qualified_name(value):
    if odata.NameTable.is_namespace(value) and "." in value:
        return value
    else:
        raise ValueError(
            "Can't parse Qualified Name from :%s" % repr(value))


def path_from_str(value):
    # TODO
    return value


def path_to_str(path):
    # TODO
    return path


def path_expression_from_str(value):
    # TODO
    return value


def path_expression_to_str(path):
    # TODO
    return path


def type_from_str(value):
    # TODO
    return value


def type_to_str(t):
    # TODO
    return t


class CSDLElement(xmlns.XMLNSElement):
    XMLCONTENT = xml.ElementType.ElementContent

    def get_entity_model(self):
        edmx = self.find_parent(Edmx)
        if edmx:
            return edmx.entity_model
        else:
            return None

    def validate(self):
        """All CSDL elements support validation.

        Covers element-specific constraints, see
        :meth:`CSDLDocument.validate` for details."""
        for child in self.get_children():
            if isinstance(child, CSDLElement):
                child.validate()


class ReferenceContent(object):

    """Abstract mixin class for elements allowed in Reference"""
    pass


class SchemaContent(object):

    """Abstract mixin class for elements allowed in Schema"""
    pass


class EntityTypeContent(object):

    """Abstract mixin class for elements allowed in EntityType"""
    pass


class ComplexTypeContent(object):

    """Abstract mixin class for elements allowed in ComplexType"""
    pass


class NavigationPropertyContent(object):

    """Abstract mixin class for elements allowed in NavigationProperty"""
    pass


class EnumTypeContent(object):

    """Abstract mixin class for elements allowed in EnumType"""
    pass


class ActionFunctionContent(object):

    """Abstract mixin class for elements allowed in Action or Function"""
    pass


class RecordContent(object):

    """Abstract mixin class for elements allowed in Record"""
    pass


class EntityContainerContent(object):

    """Abstract mixin class for elements allowed in EntityContainer"""
    pass


class AnnotedNavigationContent(object):

    """Abstract mixin class for elements allowed in EntitySet/Singleton"""
    pass


class FacetsMixin(object):

    XMLATTR_MaxLength = ('max_length', xsi.integer_from_str,
                         xsi.integer_to_str)
    XMLATTR_Precision = ('precision', xsi.integer_from_str, xsi.integer_to_str)
    XMLATTR_Scale = 'scale'     # 'variable' or non-negative integer
    XMLATTR_SRID = 'srid'       # 'variable' or non-negative integer

    def __init__(self):
        self.max_length = None
        self.precision = None
        self.scale = None
        self.srid = None


class GInlineExpressionsMixin(object):

    """Abstract class for holding attribution declarations.

    No constructor is provided as these are left to the automated
    handling of default attributes in XML elements."""

    # constant expressions
    XMLATTR_Binary = ('binary_value', odata.BinaryValue.from_str, str)
    XMLATTR_Bool = ('bool_value', odata.BooleanValue.from_str, str)
    XMLATTR_Date = ('date_value', odata.DateValue.from_str, str)
    XMLATTR_DateTimeOffset = ('date_time_offset_value',
                              odata.DateTimeOffsetValue.from_str, str)
    XMLATTR_Decimal = ('decimal_value', odata.DecimalValue.from_str, str)
    XMLATTR_Duration = ('duration_value', odata.DurationValue.from_str, str)
    XMLATTR_EnumMember = ('enum_member', None, None, list)
    XMLATTR_Float = ('float_value', odata.FloatValue.from_str, str)
    XMLATTR_Guid = ('guid_value', odata.GuidValue.from_str, str)
    XMLATTR_Int = ('int_value', odata.Int64Value.from_str, str)
    XMLATTR_String = ('string_value', odata.StringValue.from_str, str)
    XMLATTR_TimeOfDay = ('time_of_day_value', odata.TimeOfDayValue.from_str,
                         str)
    # dynamic expressions
    XMLATTR_AnnotationPath = ('annotation_path', path_expression_from_str, str)
    XMLATTR_NavigationPropertyPath = (
        'navigation_property_path', path_expression_from_str, str)
    XMLATTR_Path = ('path', path_expression_from_str, str)
    XMLATTR_PropertyPath = ('property_path', path_expression_from_str, str)
    XMLATTR_UrlRef = ('url_ref', URI.from_octets, str)


class GExpression(CSDLElement):

    """Abstract class for element expression constructs"""
    pass


class Annotation(
        ActionFunctionContent,
        AnnotedNavigationContent,
        ComplexTypeContent,
        EntityContainerContent,
        EntityTypeContent,
        EnumTypeContent,
        NavigationPropertyContent,
        ReferenceContent,
        SchemaContent,
        GInlineExpressionsMixin,
        CSDLElement):

    """Represents the Annotation element."""
    XMLNAME = (EDM_NAMESPACE, 'Annotation')

    XMLATTR_Target = ('term', validate_qualified_name, None)
    XMLATTR_Qualifier = ('qualifier', validate_simple_identifier, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        # no need to initialise the *Content classes
        self.term = None
        self.qualifier = None
        self.Annotation = []
        self.GExpression = []

    def get_children(self):
        for a in self.Annotation:
            yield a
        for e in self.GExpression:
            yield e
        for child in super(CSDLElement, self).get_children():
            yield child


class Annotated(CSDLElement):

    """Abstract class for elements that contain only annotations"""

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.Annotation = []

    def get_children(self):
        for a in self.Annotation:
            yield a
        for child in super(Annotated, self).get_children():
            yield child


class ConstantExpression(GExpression):
    XMLCONTENT = xml.ElementType.Mixed


class BinaryConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Binary')

    def get_value(self):
        return odata.BinaryValue.from_str(
            super(BinaryConstant, self).get_value())


class BoolConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Bool')

    def get_value(self):
        return odata.BooleanValue.from_str(
            super(BoolConstant, self).get_value())


class DateConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Date')

    def get_value(self):
        return odata.DateValue.from_str(
            super(DateConstant, self).get_value())


class DateTimeOffsetConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'DateTimeOffset')

    def get_value(self):
        return odata.DateTimeOffsetValue.from_str(
            super(DateTimeOffsetConstant, self).get_value())


class DecimalConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Decimal')

    def get_value(self):
        return odata.DecimalValue.from_str(
            super(DecimalConstant, self).get_value())


class DurationConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Duration')

    def get_value(self):
        return odata.DurationValue.from_str(
            super(DurationConstant, self).get_value())


class EnumMemberConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'EnumMember')

    def get_value(self):
        return [path_from_str(i) for i in
                super(EnumMemberConstant, self).get_value().split()]

    def set_value(self, value):
        if isinstance(value, list):
            super(EnumMemberConstant, self).set_value(
                " ".join(path_to_str(i) for i in value))
        elif is_text(value):
            super(EnumMemberConstant, self).set_value(value)
        else:
            raise ValueError("EnumMember expects str or list")


class FloatConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Float')

    def get_value(self):
        return odata.DoubleValue.from_str(
            super(FloatConstant, self).get_value())


class GuidConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Guid')

    def get_value(self):
        return odata.GuidValue.from_str(
            super(GuidConstant, self).get_value())


class IntConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'Int')

    def get_value(self):
        return odata.Int64Value.from_str(
            super(IntConstant, self).get_value())


class StringConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'String')

    def get_value(self):
        return odata.StringValue.from_str(
            super(StringConstant, self).get_value())


class TimeOfDayConstant(ConstantExpression):
    XMLNAME = (EDM_NAMESPACE, 'TimeOfDay')

    def get_value(self):
        return odata.TimeOfDayValue.from_str(
            super(TimeOfDayConstant, self).get_value())


class PathExpression(GExpression):
    XMLNAME = (EDM_NAMESPACE, 'Path')

    def get_value(self):
        return path_expression_from_str(
            super(PathExpression, self).get_value())


class AnnotationPath(PathExpression):
    XMLNAME = (EDM_NAMESPACE, 'AnnotationPath')


class AnnotatedExpression(GExpression):

    def __init__(self, parent):
        GExpression.__init__(self, parent)
        self.function = None
        self.Annotation = []
        self.GExpression = []   # different rules apply to num children

    def get_children(self):
        for a in self.Annotation:
            yield a
        for e in self.GExpression:
            yield e
        for child in super(AnnotatedExpression, self).get_children():
            yield child


class Apply(AnnotatedExpression):
    XMLNAME = (EDM_NAMESPACE, 'Apply')

    XMLATTR_Function = 'function'

    def __init__(self, parent):
        AnnotatedExpression.__init__(self, parent)
        self.function = None


class CastOrIsOfExpression(FacetsMixin, AnnotatedExpression):

    XMLATTR_Type = ('type_name', type_from_str, type_to_str)

    def __init__(self, parent):
        AnnotatedExpression.__init__(self, parent)
        FacetsMixin.__init__(self)
        self.type_name = None


class CastExpression(CastOrIsOfExpression):
    XMLNAME = (EDM_NAMESPACE, 'Cast')


class CollectionExpression(GExpression):
    XMLNAME = (EDM_NAMESPACE, 'Collection')

    def __init__(self, parent):
        GExpression.__init__(self, parent)
        self.GExpression = []

    def get_children(self):
        for e in self.GExpression:
            yield e
        for child in super(CollectionExpression, self).get_children():
            yield child


class IfExpression(AnnotatedExpression):
    XMLNAME = (EDM_NAMESPACE, 'If')

    def __init__(self, parent):
        AnnotatedExpression.__init__(self, parent)


class TwoChildrenExpression(AnnotatedExpression):
    pass


class EqExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Eq')


class NeExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Ne')


class GeExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Ge')


class GtExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Gt')


class LeExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Le')


class LtExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Lt')


class AndExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'And')


class OrExpression(TwoChildrenExpression):
    XMLNAME = (EDM_NAMESPACE, 'Or')


class OneChildExpression(AnnotatedExpression):
    pass


class NotExpression(OneChildExpression):
    XMLNAME = (EDM_NAMESPACE, 'Not')


class IsOfExpression(CastOrIsOfExpression):
    XMLNAME = (EDM_NAMESPACE, 'IsOf')


class LabeledElement(GInlineExpressionsMixin, AnnotatedExpression):
    XMLNAME = (EDM_NAMESPACE, 'LabeledElement')

    XMLATTR_Name = ('name', validate_simple_identifier, None)

    def __init__(self, parent):
        AnnotatedExpression.__init__(self, parent)
        self.name = None


class LabeledElementReference(GExpression):
    XMLNAME = (EDM_NAMESPACE, 'LabeledElementReference')

    def get_value(self):
        return validate_qualified_name(
            super(LabeledElementReference, self).get_value())

    def set_value(self, value):
        return super(LabeledElementReference, self).set_value(
            validate_qualified_name(value))


class NullExpression(GExpression, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Null')


class NavigationPropertyPath(PathExpression):
    XMLNAME = (EDM_NAMESPACE, 'NavigationPropertyPath')


# see above for PathExpression


class PropertyPathExpression(PathExpression):
    XMLNAME = (EDM_NAMESPACE, 'PropertyPath')


class RecordExpression(GExpression):
    XMLNAME = (EDM_NAMESPACE, 'Record')

    XMLATTR_Type = ('type_name', validate_qualified_name, None)

    def __init__(self, parent):
        GExpression.__init__(self, parent)
        self.type_name = None
        self.RecordContent = []

    def get_children(self):
        for rc in self.RecordContent:
            yield rc
        for child in super(CSDLElement, self).get_children():
            yield child


class PropertyValue(RecordContent, GInlineExpressionsMixin,
                    AnnotatedExpression):
    XMLNAME = (EDM_NAMESPACE, 'PropertyValue')

    XMLATTR_Property = ('property', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', validate_qualified_name, None)


class UrlRef(OneChildExpression):
    XMLNAME = (EDM_NAMESPACE, 'UrlRef')


RESERVED_ALIASES = ("Edm", "odata", "System", "Transient")


class Edmx(CSDLElement):

    """Represents the Edmx root element."""
    XMLNAME = (PACKAGING_NAMESPACE, 'Edmx')

    XMLATTR_Version = 'version'

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.version = "4.0"
        self.Reference = []
        self.DataServices = DataServices(self)
        # a name table containing all namespaces in this model
        self.entity_model = odata.EntityModel()

    def content_changed(self):
        # close the entity model
        if not self.DataServices._closed:
            raise odata.ModelError(
                "3.1 [edmx:Edmx] MUST contain a single direct child "
                "edmx:DataServices element")
        self.entity_model.close()

    def get_children(self):
        for child in self.Reference:
            yield child
        yield self.DataServices
        for child in CSDLElement.get_children(self):
            yield child

    def validate(self):
        if self.version != "4.0":
            raise odata.ModelError(
                "3.1.1 The edmx:Edmx element MUST provide the value "
                "4.0 for the Version attribute")
        if not self.entity_model.closed:
            raise odata.ModelError(
                "EntitModel is not closed\n"
                "3.1 [edmx.Edmx] MUST contain a single direct child "
                "edmx:DataServices element")
        super(Edmx, self).validate()
        been_there = set()
        for r in self.Reference:
            uri = str(r.resolve_uri(r.uri))
            if uri in been_there:
                raise odata.ModelError(
                    "3.3.1 two references MUST NOT specify the same URI")
            been_there.add(uri)


class DataServices(CSDLElement):
    XMLNAME = (PACKAGING_NAMESPACE, 'DataServices')

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.Schema = []
        self._closed = False

    def content_changed(self):
        if self._closed:
            raise odata.ModelError(
                "3.1 [edmx:Edmx] MUST contain a single direct child "
                "edmx:DataServices element")
        else:
            self._closed = True

    def get_children(self):
        for s in self.Schema:
            yield s
        for child in super(DataServices, self).get_children():
            yield child

    def validate(self):
        if not self.Schema:
            raise odata.ModelError(
                "3.2 The edmx:DataServices element MUST contain "
                "one or more edm:Schema elements")
        super(DataServices, self).validate()


class Reference(CSDLElement):
    XMLNAME = (PACKAGING_NAMESPACE, 'Reference')

    XMLATTR_Uri = ('uri', URI.from_octets, to_text)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.uri = None
        self.ref_model = None
        self.ReferenceContent = []

    def get_ref_model(self):
        if self.uri is None:
            raise odata.ModelError(
                "3.3.1 The edmx:Reference element MUST specify a "
                "Uri attribute")
        if self.ref_model is None:
            ref = self.resolve_uri(self.uri)
            ref_doc = CSDLDocument(base_uri=ref)
            ref_doc.read()
            ref_doc.validate()
            self.ref_model = ref_doc.root.entity_model
        return self.ref_model

    def get_children(self):
        for rc in self.ReferenceContent:
            yield rc
        for child in super(Reference, self).get_children():
            yield child

    def validate(self):
        got_child = False
        for rc in self.ReferenceContent:
            if isinstance(rc, (Include, IncludeAnnotations)):
                got_child = True
        if not got_child:
            raise odata.ModelError(
                "3.3 The edmx:Reference element MUST contain at least one "
                "edmx:Include or edmx:IncludeAnnotations child element")
        super(Reference, self).validate()


class Include(ReferenceContent, CSDLElement):
    XMLNAME = (PACKAGING_NAMESPACE, 'Include')

    XMLATTR_Namespace = ('namespace', validate_namespace, None)
    XMLATTR_Alias = ('alias', validate_simple_identifier, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.namespace = None
        self.alias = None

    def content_changed(self):
        if self.namespace is None:
            raise odata.ModelError(
                "3.4.1 The edmx:Include element MUST provide a Namespace "
                "value for the Namespace attribute")
        ref_model = self.parent.get_ref_model()
        try:
            ns = ref_model[self.namespace]
        except KeyError:
            raise odata.ModelError(
                "3.4.1 The value MUST match the namespace of a schema "
                "defined in the referenced CSDL document (%s)" %
                self.namespace)
        em = self.get_entity_model()
        if em is not None:
            try:
                if self.alias is not None:
                    if self.alias in RESERVED_ALIASES:
                        raise odata.ModelError(
                            "3.4.2 The Alias attribute MUST NOT use the "
                            "reserved values")
                    em[self.alias] = ns
            except odata.DuplicateNameError:
                raise odata.DuplicateNameError(
                    "3.4.2 a document MUST NOT assign the same alias to "
                    "different namespaces and MUST NOT specify an alias "
                    "with the same name as an in-scope namespace")
            try:
                ns.declare(em)
            except odata.DuplicateNameError:
                raise odata.DuplicateNameError(
                    "3.4.1 The same namespace MUST NOT be included "
                    "more than once")


class IncludeAnnotations(ReferenceContent, CSDLElement):
    XMLNAME = (PACKAGING_NAMESPACE, 'IncludeAnnotations')

    XMLATTR_TermNamespace = ('term_namespace', validate_namespace, None)
    XMLATTR_Qualifier = ('qualifier', validate_simple_identifier, None)
    XMLATTR_TargetNamespace = ('target_namespace', validate_namespace, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.term_namespace = None
        self.qualifier = None
        self.target_namespace = None


class Schema(CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'Schema')

    XMLATTR_Namespace = ('namespace', validate_namespace, None)
    XMLATTR_Alias = ('alias', validate_simple_identifier, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.namespace = None
        self.alias = None
        self.SchemaContent = []
        self._ns = None

    def get_schema_ns(self):
        if self.namespace is None:
            raise odata.ModelError("expected Namespace in Schema")
        if self._ns is None:
            self._ns = odata.Namespace()
            self._ns.name = self.namespace
            em = self.get_entity_model()
            self._ns.declare(em)
            if self.alias is not None:
                if self.alias in RESERVED_ALIASES:
                    raise odata.ModelError(
                        "The Alias attribute MUST NOT use the "
                        "reserved values")
                try:
                    em[self.alias] = self._ns
                except odata.DuplicateNameError:
                    raise odata.ModelError(
                        "3.4.2 a document MUST NOT specify an alias with "
                        "the same name as an in-scope namespace")
        return self._ns

    def content_changed(self):
        ns = self.get_schema_ns()
        # close this namespace
        ns.close()

    def get_children(self):
        for sc in self.SchemaContent:
            yield sc
        for child in super(Schema, self).get_children():
            yield child


class Type(CSDLElement):

    XMLATTR_Name = ('base_type', validate_simple_identifier, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.name = None


class DerivableType(Type):

    XMLATTR_BaseType = ('base_type', validate_qualified_name, None)
    XMLATTR_Abstract = ('abstract', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self, parent):
        Type.__init__(self, parent)
        self.base_type = None
        self.abstract = False


class ComplexType(SchemaContent, DerivableType):
    XMLNAME = (EDM_NAMESPACE, 'ComplexType')

    XMLATTR_OpenType = ('open_type', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self, parent):
        DerivableType.__init__(self, parent)
        self.open_type = False
        self.ComplexTypeContent = []

    def get_children(self):
        for cc in self.ComplexTypeContent:
            yield cc
        for child in super(ComplexType, self).get_children():
            yield child


class EntityType(SchemaContent, DerivableType):
    XMLNAME = (EDM_NAMESPACE, 'EntityType')

    XMLATTR_OpenType = ('open_type', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_HasStream = ('has_stream', xsi.boolean_from_str,
                         xsi.boolean_to_str)

    def __init__(self, parent):
        DerivableType.__init__(self, parent)
        self.open_type = False
        self.has_stream = False
        self.EntityTypeContent = []

    def get_children(self):
        for sc in self.EntityTypeContent:
            yield sc
        for child in super(EntityType, self).get_children():
            yield child


class Key(EntityTypeContent, CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'Key')

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.PropertyRef = []

    def get_children(self):
        for p in self.PropertyRef:
            yield p
        for child in super(Key, self).get_children():
            yield child


class PropertyRef(CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'PropertyRef')

    XMLATTR_Name = ('name', path_from_str, path_to_str)
    XMLATTR_Alias = ('alias', validate_simple_identifier, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.name = None
        self.alias = None


class PropertyFacetsMixin(object):

    XMLATTR_Unicode = ('unicode', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self):
        self.unicode = None


class CommonPropertyMixin(FacetsMixin, PropertyFacetsMixin):

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', type_from_str, type_to_str)
    XMLATTR_Nullable = ('nullable', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_DefaultValue = 'default_value'

    def __init__(self):
        FacetsMixin.__init__(self)
        PropertyFacetsMixin.__init__(self)
        self.name = None
        self.type_name = None
        self.nullable = True
        self.default_value = None


class Property(EntityTypeContent, CommonPropertyMixin, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Property')

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        CommonPropertyMixin.__init__(self)


class NavigationProperty(EntityTypeContent, CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'NavigationProperty')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', type_from_str, type_to_str)
    XMLATTR_Nullable = ('nullable', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_Partner = ('partner', path_from_str, path_to_str)
    XMLATTR_ContainsTarget = ('contains_target', xsi.boolean_from_str,
                              xsi.boolean_to_str)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.name = None
        self.type_name = None
        self.nullable = True
        self.partner = True
        self.contains_target = True
        self.NavigationPropertyContent = []

    def get_children(self):
        for npc in self.NavigationPropertyContent:
            yield npc
        for child in super(NavigationProperty, self).get_children():
            yield child


class ReferentialConstraint(Annotated):
    XMLNAME = (EDM_NAMESPACE, 'ReferentialConstraint')

    XMLATTR_Property = ('property', path_from_str, path_to_str)
    XMLATTR_ReferencedProperty = ('referenced_property', path_from_str,
                                  path_to_str)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        self.property = None
        self.referenced_property = None


class OnDelete(Annotated):
    XMLNAME = (EDM_NAMESPACE, 'OnDelete')

    XMLATTR_action = 'action'
    # enumeration: Cascade, None, SetDefault, SetNull

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        self.action = None


class TypeDefinition(SchemaContent, FacetsMixin, PropertyFacetsMixin,
                     Annotated):
    XMLNAME = (EDM_NAMESPACE, 'TypeDefinition')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_UnderlyingType = ('underlying_type', validate_qualified_name, None)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        FacetsMixin.__init__(self)
        PropertyFacetsMixin.__init__(self)
        self.name = None
        self.underlying_type = None     # must be a primitive type


class EnumType(SchemaContent, Type):
    XMLNAME = (EDM_NAMESPACE, 'EnumType')

    XMLATTR_IsFlags = ('is_flags', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_UnderlyingType = ('underlying_type', validate_qualified_name, None)

    def __init__(self, parent):
        Type.__init__(self, parent)
        self.is_flags = None
        self.underlying_type = None     # must be a primitive type
        self.EnumTypeContent = []

    def get_children(self):
        for etc in self.EnumTypeContent:
            yield etc
        for child in super(EnumType, self).get_children():
            yield child


class Member(EnumTypeContent, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Member')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Value = ('value', xsi.integer_from_str, xsi.integer_to_str)
    # long

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        self.name = None
        self.value = None


class ReturnType(FacetsMixin, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'ReturnType')

    XMLATTR_Type = ('type_name', type_from_str, type_to_str)
    XMLATTR_Nullable = ('nullable', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        FacetsMixin.__init__(self)
        self.type_name = None
        self.nullable = None


class ActionFunction(CSDLElement):

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.ActionFunctionContent = []
        self.ReturnType = None

    def get_children(self):
        for afc in self.ActionFunctionContent:
            yield afc
        if self.ReturnType:
            yield self.ReturnType
        for child in super(EnumType, self).get_children():
            yield child


class Parameter(ActionFunctionContent, FacetsMixin, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Parameter')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', type_from_str, type_to_str)
    XMLATTR_Nullable = ('nullable', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.name = None
        self.type_name = None
        self.nullable = None


class Action(SchemaContent, ActionFunction):
    XMLNAME = (EDM_NAMESPACE, 'Action')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_EntitySetPath = ('entity_set_path', path_from_str, path_to_str)
    XMLATTR_IsBound = ('is_bound', xsi.boolean_from_str, xsi.boolean_to_str)

    def __init__(self, parent):
        ActionFunction.__init__(self, parent)
        self.name = None
        self.entity_set_path = None
        self.is_bound = False


class Function(SchemaContent, ActionFunction):
    XMLNAME = (EDM_NAMESPACE, 'Function')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_EntitySetPath = ('entity_set_path', path_from_str, path_to_str)
    XMLATTR_IsBound = ('is_bound', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_IsComposable = ('is_composable', xsi.boolean_from_str,
                            xsi.boolean_to_str)

    def __init__(self, parent):
        ActionFunction.__init__(self, parent)
        # ReturnType is required
        self.ReturnType = ReturnType()
        self.name = None
        self.entity_set_path = None
        self.is_bound = False
        self.is_composable = False


class Term(SchemaContent, FacetsMixin, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Term')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', type_from_str, type_to_str)
    XMLATTR_BaseTerm = ('base_term', validate_qualified_name, None)
    XMLATTR_Nullable = ('nullable', xsi.boolean_from_str, xsi.boolean_to_str)
    XMLATTR_DefaultValue = 'default_value'
    XMLATTR_AppliesTo = 'applies_to'    # TODO: enumeration

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        self.name = None
        self.type_name = None
        self.base_term = None
        self.nullable = None
        self.default_value = None
        self.applies_to = None


class Annotations(SchemaContent, Annotated):
    XMLNAME = (EDM_NAMESPACE, 'Annotations')

    XMLATTR_Target = ('target', path_from_str, path_to_str)
    XMLATTR_Qualifier = ('qualifier', validate_simple_identifier, None)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        # at least one annotation required!
        self.target = None
        self.qualifier = None


class EntityContainer(SchemaContent, CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'EntityContainer')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Extends = ('extends', validate_qualified_name, None)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.name = None
        self.extends = None
        self.EntityContainerContent = []

    def get_children(self):
        for ec in self.EntityContainerContent:
            yield ec
        for child in super(EntityContainer, self).get_children():
            yield child


class AnnotatedNavigation(CSDLElement):

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.AnnotedNavigationContent = []

    def get_children(self):
        for ec in self.AnnotedNavigationContent:
            yield ec
        for child in super(EntityContainer, self).get_children():
            yield child


class EntitySet(EntityContainerContent, AnnotatedNavigation):
    XMLNAME = (EDM_NAMESPACE, 'EntitySet')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_EntityType = ('type_name', validate_qualified_name, None)
    XMLATTR_IncludeInServiceDocument = (
        'include_in_service_document', xsi.boolean_from_str,
        xsi.boolean_to_str)

    def __init__(self, parent):
        AnnotatedNavigation.__init__(self, parent)
        self.name = None
        self.type_name = None
        self.include_in_service_document = True


class NavigationPropertyBinding(AnnotedNavigationContent, CSDLElement):
    XMLNAME = (EDM_NAMESPACE, 'NavigationPropertyBinding')

    XMLATTR_Path = ('path', path_from_str, path_to_str)
    XMLATTR_Target = ('target', path_from_str, path_to_str)

    def __init__(self, parent):
        CSDLElement.__init__(self, parent)
        self.path = None
        self.target = None


class ActionFunctionImportMixin(object):

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_EntitySet = ('entity_set', path_from_str, path_to_str)
    XMLATTR_IncludeInServiceDocument = (
        'include_in_service_document', xsi.boolean_from_str,
        xsi.boolean_to_str)

    def __init__(self):
        self.name = None
        self.entity_set = None
        self.include_in_service_document = False


class ActionImport(EntityContainerContent, ActionFunctionImportMixin,
                   Annotated):
    XMLNAME = (EDM_NAMESPACE, 'ActionImport')

    XMLATTR_action = ('action', validate_qualified_name, None)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        ActionFunctionImportMixin.__init__(self)
        self.action = None


class FunctionImport(EntityContainerContent, ActionFunctionImportMixin,
                     Annotated):
    XMLNAME = (EDM_NAMESPACE, 'FunctionImport')

    XMLATTR_action = ('function', validate_qualified_name, None)

    def __init__(self, parent):
        Annotated.__init__(self, parent)
        ActionFunctionImportMixin.__init__(self)
        self.function = None


class Singleton(EntityContainerContent, AnnotedNavigationContent):
    XMLNAME = (EDM_NAMESPACE, 'Singleton')

    XMLATTR_Name = ('name', validate_simple_identifier, None)
    XMLATTR_Type = ('type_name', validate_qualified_name, None)

    def __init__(self, parent):
        AnnotatedNavigation.__init__(self, parent)
        self.name = None
        self.type_name = None


class CSDLDocument(xmlns.XMLNSDocument):

    """Represents a CSDL document."""

    class_map = {}

    def __init__(self, **args):
        xmlns.XMLNSDocument.__init__(self, **args)
        self.default_ns = EDM_NAMESPACE
        self.make_prefix(PACKAGING_NAMESPACE, 'edmx')
        self.make_prefix(EDM_NAMESPACE, '')

    @classmethod
    def get_element_class(cls, name):
        """Overridden to look up name in the class map"""
        eclass = CSDLDocument.class_map.get(
            name, CSDLDocument.class_map.get(
                (name[0], None), xmlns.XMLNSElement))
        return eclass

    def validate(self):
        """Checks CSDL constraints

        Raises :class:`~pyslet.odata4.model.ModelError` if an error is
        found.  The error message refers to the second of the
        specification that contains the violated constrain.

        Some constraints raise fatal validity errors during XML
        parsing."""
        if self.root is None or not isinstance(self.root, Edmx):
            raise odata.ModelError(
                "3.1 A CSDL document MUST contain a root edmx:Edmx element")
        self.root.validate()


xmlns.map_class_elements(CSDLDocument.class_map, globals())