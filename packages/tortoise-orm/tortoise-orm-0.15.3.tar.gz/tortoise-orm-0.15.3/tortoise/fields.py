import datetime
import functools
import json
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Awaitable, Generic, Optional, Type, TypeVar, Union
from uuid import UUID, uuid4

import ciso8601
from pypika import Table

from tortoise.exceptions import ConfigurationError, NoValuesFetched, OperationalError

if TYPE_CHECKING:  # pragma: nocoverage
    from tortoise.models import Model
    from tortoise.queryset import QuerySet

MODEL = TypeVar("MODEL", bound="Model")

CASCADE = "CASCADE"
RESTRICT = "RESTRICT"
SET_NULL = "SET NULL"
SET_DEFAULT = "SET DEFAULT"

# Doing this we can replace json dumps/loads with different implementations
JSON_DUMPS = functools.partial(json.dumps, separators=(",", ":"))
JSON_LOADS = json.loads


class _FieldMeta(type):
    def __new__(mcs, name, bases, attrs):
        if len(bases) > 1 and bases[0] is Field:
            # Instantiate class with only the 1st base class (should be Field)
            cls = type.__new__(mcs, name, (bases[0],), attrs)  # type: Type[Field]
            # All other base classes are our meta types, we store them in class attributes
            cls.field_type = bases[1] if len(bases) == 2 else bases[1:]
            return cls
        return type.__new__(mcs, name, bases, attrs)


class Field(metaclass=_FieldMeta):
    """
    Base Field type.

    :param source_field:
        Name of the field in the database schema.

        Defaults to ``None``, which makes Tortoise
        use the same name as the attribute the field is assigned to.
    :param generated:
        A flag indicating that this field is read-only and its value is generated in database.

        You typically don’t need to specify this if you created the schema through Tortoise.

        Defaults to ``False``, except for integer Primary Keys.
    :param pk:
        ``True`` if field is Primary Key.

        Defaults to ``False``.
    :param null:
        Whether the field is nullable.

        Defaults to ``False``.
    :param default:
        A default value for the field.

        This can also be a callable for lazy or mutable defaults.

        Defaults to ``None``, which has no effect unless the field is nullable.
    :param unique:
        Require that values for the field are unique.

        Defaults to ``False``, except for Primary Keys.
    :param index:
        Set to ``True`` to create a B-Tree index for this field.

        Defaults to ``False``, except for Primary Keys.
    :param description:
        Human readable description of the field.

        This field is leveraged to generate comment messages for each database columns.
        This also allows consumers to build automated documentation tooling based on the
        declarative model api.

        Defaults to ``None``.
    """

    # Field_type is a readonly property for the instance, it is set by _FieldMeta
    field_type: Type[Any] = None  # type: ignore
    indexable: bool = True
    skip_to_python_if_native = False

    __slots__ = (
        "source_field",
        "generated",
        "pk",
        "default",
        "null",
        "unique",
        "index",
        "model_field_name",
        "model",
        "reference",
        "description",
    )
    has_db_field = True

    # This method is just to make IDE/Linters happy
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(
        self,
        source_field: Optional[str] = None,
        generated: bool = False,
        pk: bool = False,
        null: bool = False,
        default: Any = None,
        unique: bool = False,
        index: bool = False,
        description: Optional[str] = None,
        reference: Optional[str] = None,
        model: "Optional[Model]" = None,
        **kwargs,
    ) -> None:
        if not self.indexable and (unique or index):
            raise ConfigurationError(f"{self.__class__.__name__} can't be indexed")

        self.source_field = source_field
        self.generated = generated
        self.pk = pk
        self.default = default
        self.null = null
        self.unique = unique
        self.index = index
        self.description = description

        self.model_field_name = ""
        self.model = model
        self.reference = reference

    def to_db_value(self, value: Any, instance) -> Any:
        if value is None or isinstance(value, self.field_type):
            return value
        return self.field_type(value)  # pylint: disable=E1102

    def to_python_value(self, value: Any) -> Any:
        if value is None or isinstance(value, self.field_type):
            return value
        return self.field_type(value)  # pylint: disable=E1102

    @property
    def required(self) -> bool:
        """
        Should a value be provided for this field when building model instances?

        For reference, this is only True if the field has no default value,
        is not nullable and is not generated.
        """
        return self.default is None and not self.null and not self.generated


class IntField(Field, int):
    """
    Integer field. (32-bit signed)

    ``pk`` (bool):
        True if field is Primary Key.
    """

    def __init__(self, pk: bool = False, **kwargs) -> None:
        if pk:
            kwargs["generated"] = bool(kwargs.get("generated", True))
        super().__init__(pk=pk, **kwargs)


class BigIntField(Field, int):
    """
    Big integer field. (64-bit signed)

    ``pk`` (bool):
        True if field is Primary Key.
    """

    def __init__(self, pk: bool = False, **kwargs) -> None:
        if pk:
            kwargs["generated"] = bool(kwargs.get("generated", True))
        super().__init__(pk=pk, **kwargs)


class SmallIntField(Field, int):
    """
    Small integer field. (16-bit signed)

    ``pk`` (bool):
        True if field is Primary Key.
    """

    __slots__ = ()

    def __init__(self, pk: bool = False, **kwargs) -> None:
        if pk:
            kwargs["generated"] = bool(kwargs.get("generated", True))
        super().__init__(pk=pk, **kwargs)


class CharField(Field, str):  # type: ignore
    """
    Character field.

    You must provide the following:

    ``max_length`` (int):
        Maximum length of the field in characters.
    """

    __slots__ = ("max_length",)

    def __init__(self, max_length: int, **kwargs) -> None:
        if int(max_length) < 1:
            raise ConfigurationError("'max_length' must be >= 1")
        self.max_length = int(max_length)
        super().__init__(**kwargs)


class TextField(Field, str):  # type: ignore
    """
    Large Text field.
    """

    __slots__ = ()
    indexable = False


class BooleanField(Field):
    """
    Boolean field.
    """

    __slots__ = ()

    # Bool is not subclassable, so we specify type here
    field_type = bool


class DecimalField(Field, Decimal):
    """
    Accurate decimal field.

    You must provide the following:

    ``max_digits`` (int):
        Max digits of significance of the decimal field.
    ``decimal_places`` (int):
        How many of those signifigant digits is after the decimal point.
    """

    __slots__ = ("max_digits", "decimal_places")

    def __init__(self, max_digits: int, decimal_places: int, **kwargs) -> None:
        if int(max_digits) < 1:
            raise ConfigurationError("'max_digits' must be >= 1")
        if int(decimal_places) < 0:
            raise ConfigurationError("'decimal_places' must be >= 0")
        super().__init__(**kwargs)
        self.max_digits = max_digits
        self.decimal_places = decimal_places


class DatetimeField(Field, datetime.datetime):
    """
    Datetime field.

    ``auto_now`` and ``auto_now_add`` is exclusive.
    You can opt to set neither or only ONE of them.

    ``auto_now`` (bool):
        Always set to ``datetime.utcnow()`` on save.
    ``auto_now_add`` (bool):
        Set to ``datetime.utcnow()`` on first save only.
    """

    __slots__ = ("auto_now", "auto_now_add")
    skip_to_python_if_native = True

    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, **kwargs) -> None:
        if auto_now_add and auto_now:
            raise ConfigurationError("You can choose only 'auto_now' or 'auto_now_add'")
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_python_value(self, value: Any) -> Optional[datetime.datetime]:
        if value is None or isinstance(value, datetime.datetime):
            return value
        return ciso8601.parse_datetime(value)

    def to_db_value(
        self, value: Optional[datetime.datetime], instance
    ) -> Optional[datetime.datetime]:
        if hasattr(instance, "_saved_in_db"):
            # Only do this if it is a Model instance, not class. Test for guaranteed instance var
            if self.auto_now:
                value = datetime.datetime.utcnow()
                setattr(instance, self.model_field_name, value)
            if self.auto_now_add and getattr(instance, self.model_field_name) is None:
                value = datetime.datetime.utcnow()
                setattr(instance, self.model_field_name, value)
        return value


class DateField(Field, datetime.date):
    """
    Date field.
    """

    __slots__ = ()
    skip_to_python_if_native = True

    def to_python_value(self, value: Any) -> Optional[datetime.date]:
        if value is None or isinstance(value, datetime.date):
            return value
        return ciso8601.parse_datetime(value).date()


class TimeDeltaField(Field, datetime.timedelta):
    """
    A field for storing time differences.
    """

    __slots__ = ()

    def to_python_value(self, value: Any) -> Optional[datetime.timedelta]:
        if value is None or isinstance(value, datetime.timedelta):
            return value
        return datetime.timedelta(microseconds=value)

    def to_db_value(self, value: Optional[datetime.timedelta], instance) -> Optional[int]:
        if value is None:
            return None
        return (value.days * 86400000000) + (value.seconds * 1000000) + value.microseconds


class FloatField(Field, float):
    """
    Float (double) field.
    """

    __slots__ = ()


class JSONField(Field, dict, list):  # type: ignore
    """
    JSON field.

    This field can store dictionaries or lists of any JSON-compliant structure.

    ``encoder``:
        The JSON encoder. The default is recommended.
    ``decoder``:
        The JSON decoder. The default is recommended.
    """

    __slots__ = ("encoder", "decoder")
    indexable = False

    def __init__(self, encoder=JSON_DUMPS, decoder=JSON_LOADS, **kwargs) -> None:
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def to_db_value(self, value: Optional[Union[dict, list]], instance) -> Optional[str]:
        if value is None:
            return None
        return self.encoder(value)

    def to_python_value(
        self, value: Optional[Union[str, dict, list]]
    ) -> Optional[Union[dict, list]]:
        if value is None or isinstance(value, (dict, list)):
            return value
        return self.decoder(value)


class UUIDField(Field, UUID):
    """
    UUID Field

    This field can store uuid value.

    If used as a primary key, it will auto-generate a UUID4 by default.
    """

    def __init__(self, **kwargs) -> None:
        if kwargs.get("pk", False):
            if "default" not in kwargs:
                kwargs["default"] = uuid4
        super().__init__(**kwargs)

    def to_db_value(self, value: Any, instance) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    def to_python_value(self, value: Any) -> Optional[UUID]:
        if value is None or isinstance(value, UUID):
            return value
        return UUID(value)


ForeignKeyNullableRelation = Union[Awaitable[Optional[MODEL]], Optional[MODEL]]
"""
Type hint for the result of accessing the :class:`.ForeignKeyField` field in the model
when obtained model can be nullable.
"""

ForeignKeyRelation = Union[Awaitable[MODEL], MODEL]
"""
Type hint for the result of accessing the :class:`.ForeignKeyField` field in the model.
"""


class ForeignKeyField(Field):
    """
    ForeignKey relation field.

    This field represents a foreign key relation to another model.

    You must provide the following:

    ``model_name``:
        The name of the related model in a :samp:`'{app}.{model}'` format.

    The following is optional:

    ``related_name``:
        The attribute name on the related model to reverse resolve the foreign key.
    ``on_delete``:
        One of:
            ``field.CASCADE``:
                Indicate that the model should be cascade deleted if related model gets deleted.
            ``field.RESTRICT``:
                Indicate that the related model delete will be restricted as long as a
                foreign key points to it.
            ``field.SET_NULL``:
                Resets the field to NULL in case the related model gets deleted.
                Can only be set if field has ``null=True`` set.
            ``field.SET_DEFAULT``:
                Resets the field to ``default`` value in case the related model gets deleted.
                Can only be set is field has a ``default`` set.
    """

    __slots__ = (
        "field_type",
        # type will be set later, so we need a slot to be able to write it
        "model_name",
        "related_name",
        "on_delete",
    )
    has_db_field = False

    def __init__(
        self, model_name: str, related_name: Optional[str] = None, on_delete=CASCADE, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        # self.field_type: "Type[Model]" = None  # type: ignore
        if len(model_name.split(".")) != 2:
            raise ConfigurationError('Foreign key accepts model name in format "app.Model"')
        self.model_name = model_name
        self.related_name = related_name
        if on_delete not in {CASCADE, RESTRICT, SET_NULL}:
            raise ConfigurationError("on_delete can only be CASCADE, RESTRICT or SET_NULL")
        if on_delete == SET_NULL and not bool(kwargs.get("null")):
            raise ConfigurationError("If on_delete is SET_NULL, then field must have null=True set")
        self.on_delete = on_delete

    # we need this for IDEs so that they don't say that the field is not awaitable
    def __await__(self):  # pragma: nocoverage
        ...  # pylint: disable=W0104


OneToOneNullableRelation = Union[Awaitable[Optional[MODEL]], Optional[MODEL]]
"""
Type hint for the result of accessing the :class:`.OneToOneField` field in the model
when obtained model can be nullable.
"""

OneToOneRelation = Union[Awaitable[MODEL], MODEL]
"""
Type hint for the result of accessing the :class:`.OneToOneField` field in the model.
"""


class OneToOneField(Field):
    """
    OneToOne relation field.

    This field represents a one to one relation to another model.

    You must provide the following:

    ``model_name``:
        The name of the related model in a :samp:`'{app}.{model}'` format.

    The following is optional:

    ``related_name``:
        The attribute name on the related model to reverse resolve the one to one relation.
    ``on_delete``:
        One of:
            ``field.CASCADE``:
                Indicate that the model should be cascade deleted if related model gets deleted.
            ``field.RESTRICT``:
                Indicate that the related model delete will be restricted as long as a
                one to one relation points to it.
            ``field.SET_NULL``:
                Resets the field to NULL in case the related model gets deleted.
                Can only be set if field has ``null=True`` set.
            ``field.SET_DEFAULT``:
                Resets the field to ``default`` value in case the related model gets deleted.
                Can only be set is field has a ``default`` set.
    """

    __slots__ = (
        "field_type",
        # type will be set later, so we need a slot to be able to write it
        "model_name",
        "related_name",
        "on_delete",
    )
    has_db_field = False

    def __init__(
        self, model_name: str, related_name: Optional[str] = None, on_delete=CASCADE, **kwargs
    ) -> None:
        kwargs["unique"] = True
        super().__init__(**kwargs)
        # self.field_type: "Type[Model]" = None  # type: ignore
        if len(model_name.split(".")) != 2:
            raise ConfigurationError('OneToOneField accepts model name in format "app.Model"')
        self.model_name = model_name
        self.related_name = related_name
        if on_delete not in {CASCADE, RESTRICT, SET_NULL}:
            raise ConfigurationError("on_delete can only be CASCADE, RESTRICT or SET_NULL")
        if on_delete == SET_NULL and not bool(kwargs.get("null")):
            raise ConfigurationError("If on_delete is SET_NULL, then field must have null=True set")
        self.on_delete = on_delete

    # we need this for IDEs so that they don't say that the field is not awaitable
    def __await__(self):
        ...  # pylint: disable=W0104


class ManyToManyFieldInstance(Field):
    __slots__ = (
        "field_type",  # Here we need type to be able to set dyamically
        "model_name",
        "related_name",
        "forward_key",
        "backward_key",
        "through",
        "_generated",
    )
    has_db_field = False

    def __init__(
        self,
        model_name: str,
        through: Optional[str] = None,
        forward_key: Optional[str] = None,
        backward_key: str = "",
        related_name: str = "",
        field_type: "Type[Model]" = None,  # type: ignore
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.field_type = field_type
        if len(model_name.split(".")) != 2:
            raise ConfigurationError('Foreign key accepts model name in format "app.Model"')
        self.model_name = model_name
        self.related_name = related_name
        self.forward_key = forward_key or f"{model_name.split('.')[1].lower()}_id"
        self.backward_key = backward_key
        self.through = through
        self._generated = False


def ManyToManyField(
    model_name: str,
    through: Optional[str] = None,
    forward_key: Optional[str] = None,
    backward_key: str = "",
    related_name: str = "",
    **kwargs,
) -> "ManyToManyRelation":
    """
        ManyToMany relation field.

        This field represents a many-to-many between this model and another model.

        See :ref:`many_to_many` for usage information.

        You must provide the following:

        ``model_name``:
            The name of the related model in a :samp:`'{app}.{model}'` format.

        The following is optional:

        ``through``:
            The DB table that represents the trough table.
            The default is normally safe.
        ``forward_key``:
            The forward lookup key on the through table.
            The default is normally safe.
        ``backward_key``:
            The backward lookup key on the through table.
            The default is normally safe.
        ``related_name``:
            The attribute name on the related model to reverse resolve the many to many.
        """

    return ManyToManyFieldInstance(  # type: ignore
        model_name, through, forward_key, backward_key, related_name, **kwargs
    )


class BackwardFKRelation(Field):
    __slots__ = ("field_type", "relation_field")  # Here we need type to be able to set dyamically
    has_db_field = False

    def __init__(
        self, field_type: "Type[Model]", relation_field: str, null: bool, description: Optional[str]
    ) -> None:
        super().__init__(null=null)
        self.field_type = field_type
        self.relation_field = relation_field
        self.description = description


class BackwardOneToOneRelation(BackwardFKRelation):
    pass


class ReverseRelation(Generic[MODEL]):
    """
    Relation container for :class:`.ForeignKeyField`.
    """

    __slots__ = (
        "model",
        "relation_field",
        "instance",
        "_fetched",
        "_custom_query",
        "related_objects",
    )

    def __init__(self, model, relation_field: str, instance) -> None:
        self.model = model
        self.relation_field = relation_field
        self.instance = instance
        self._fetched = False
        self._custom_query = False
        self.related_objects: list = []

    @property
    def _query(self):
        if not self.instance._saved_in_db:
            raise OperationalError(
                "This objects hasn't been instanced, call .save() before calling related queries"
            )
        return self.model.filter(**{self.relation_field: self.instance.pk})

    def __contains__(self, item) -> bool:
        if not self._fetched:
            raise NoValuesFetched(
                "No values were fetched for this relation, first use .fetch_related()"
            )
        return item in self.related_objects

    def __iter__(self):
        if not self._fetched:
            raise NoValuesFetched(
                "No values were fetched for this relation, first use .fetch_related()"
            )
        return self.related_objects.__iter__()

    def __len__(self) -> int:
        if not self._fetched:
            raise NoValuesFetched(
                "No values were fetched for this relation, first use .fetch_related()"
            )
        return len(self.related_objects)

    def __bool__(self) -> bool:
        if not self._fetched:
            raise NoValuesFetched(
                "No values were fetched for this relation, first use .fetch_related()"
            )
        return bool(self.related_objects)

    def __getitem__(self, item):
        if not self._fetched:
            raise NoValuesFetched(
                "No values were fetched for this relation, first use .fetch_related()"
            )
        return self.related_objects[item]

    def __await__(self):
        return self._query.__await__()

    async def __aiter__(self):
        if not self._fetched:
            self.related_objects = await self
            self._fetched = True

        for val in self.related_objects:
            yield val

    def filter(self, *args, **kwargs) -> "QuerySet[MODEL]":
        """
        Returns QuerySet with related elements filtered by args/kwargs.
        """
        return self._query.filter(*args, **kwargs)

    def all(self) -> "QuerySet[MODEL]":
        """
        Returns QuerySet with all related elements.
        """
        return self._query

    def order_by(self, *args, **kwargs) -> "QuerySet[MODEL]":
        """
        Returns QuerySet related elements in order.
        """
        return self._query.order_by(*args, **kwargs)

    def limit(self, *args, **kwargs) -> "QuerySet[MODEL]":
        """
        Returns a QuerySet with at most «limit» related elements.
        """
        return self._query.limit(*args, **kwargs)

    def offset(self, *args, **kwargs) -> "QuerySet[MODEL]":
        """
        Returns aQuerySet with all related elements offset by «offset».
        """
        return self._query.offset(*args, **kwargs)

    def _set_result_for_query(self, sequence) -> None:
        self._fetched = True
        self.related_objects = sequence


class ManyToManyRelation(ReverseRelation[MODEL]):
    """
    Many to many relation container for :class:`.ManyToManyField`.
    """

    __slots__ = ("field", "model", "instance")

    def __init__(self, model, instance, m2m_field: ManyToManyFieldInstance) -> None:
        super().__init__(model, m2m_field.related_name, instance)
        self.field = m2m_field
        self.model = m2m_field.field_type
        self.instance = instance

    async def add(self, *instances, using_db=None) -> None:
        """
        Adds one or more of ``instances`` to the relation.

        If it is already added, it will be silently ignored.
        """
        if not instances:
            return
        if not self.instance._saved_in_db:
            raise OperationalError(f"You should first call .save() on {self.instance}")
        db = using_db if using_db else self.model._meta.db
        pk_formatting_func = type(self.instance)._meta.pk.to_db_value
        related_pk_formatting_func = type(instances[0])._meta.pk.to_db_value
        through_table = Table(self.field.through)
        select_query = (
            db.query_class.from_(through_table)
            .where(
                getattr(through_table, self.field.backward_key)
                == pk_formatting_func(self.instance.pk, self.instance)
            )
            .select(self.field.backward_key, self.field.forward_key)
        )
        query = db.query_class.into(through_table).columns(
            getattr(through_table, self.field.forward_key),
            getattr(through_table, self.field.backward_key),
        )

        if len(instances) == 1:
            criterion = getattr(
                through_table, self.field.forward_key
            ) == related_pk_formatting_func(instances[0].pk, instances[0])
        else:
            criterion = getattr(through_table, self.field.forward_key).isin(
                [related_pk_formatting_func(i.pk, i) for i in instances]
            )

        select_query = select_query.where(criterion)

        # TODO: This is highly inefficient. Should use UNIQUE index by default.
        #  And optionally allow duplicates.
        already_existing_relations_raw = await db.execute_query(str(select_query))
        already_existing_relations = {
            (
                pk_formatting_func(r[self.field.backward_key], self.instance),
                related_pk_formatting_func(r[self.field.forward_key], self.instance),
            )
            for r in already_existing_relations_raw
        }

        insert_is_required = False
        for instance_to_add in instances:
            if not instance_to_add._saved_in_db:
                raise OperationalError(f"You should first call .save() on {instance_to_add}")
            pk_f = related_pk_formatting_func(instance_to_add.pk, instance_to_add)
            pk_b = pk_formatting_func(self.instance.pk, self.instance)
            if (pk_b, pk_f) in already_existing_relations:
                continue
            query = query.insert(pk_f, pk_b)
            insert_is_required = True
        if insert_is_required:
            await db.execute_query(str(query))

    async def clear(self, using_db=None) -> None:
        """
        Clears ALL relations.
        """
        db = using_db if using_db else self.model._meta.db
        through_table = Table(self.field.through)
        pk_formatting_func = type(self.instance)._meta.pk.to_db_value
        query = (
            db.query_class.from_(through_table)
            .where(
                getattr(through_table, self.field.backward_key)
                == pk_formatting_func(self.instance.pk, self.instance)
            )
            .delete()
        )
        await db.execute_query(str(query))

    async def remove(self, *instances, using_db=None) -> None:
        """
        Removes one or more of ``instances`` from the relation.
        """
        db = using_db if using_db else self.model._meta.db
        if not instances:
            raise OperationalError("remove() called on no instances")
        through_table = Table(self.field.through)
        pk_formatting_func = type(self.instance)._meta.pk.to_db_value
        related_pk_formatting_func = type(instances[0])._meta.pk.to_db_value

        if len(instances) == 1:
            condition = (
                getattr(through_table, self.field.forward_key)
                == related_pk_formatting_func(instances[0].pk, instances[0])
            ) & (
                getattr(through_table, self.field.backward_key)
                == pk_formatting_func(self.instance.pk, self.instance)
            )
        else:
            condition = (
                getattr(through_table, self.field.backward_key)
                == pk_formatting_func(self.instance.pk, self.instance)
            ) & (
                getattr(through_table, self.field.forward_key).isin(
                    [related_pk_formatting_func(i.pk, i) for i in instances]
                )
            )
        query = db.query_class.from_(through_table).where(condition).delete()
        await db.execute_query(str(query))
