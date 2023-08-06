import sqlalchemy
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import mapper

from fasvaorm.timebased_models import TimeBase

from fasvaorm import Base
__all__ = [
    'get_class_by_tablename',
    'init_timebased_model'
]


def get_class_by_tablename(table_fullname):
    """
    Return class reference mapped to table.

    Args:
        table_fullname (str):  The fullname of table

    Returns:
        None | class: The reference or None.

    """
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__table__') and c.__table__.fullname == table_fullname:
            return c


def init_timebased_model(name, model, timebase):
    """
    Initialize the time-based model.

    Args:
        name (str):             Name of the model
        model (Table):
        timebase (TimeBase|int):    The model time base

    Returns:

    """
    if isinstance(timebase, TimeBase):
        timebase = timebase.value

    model.timebase = timebase
    try:
        return type(name, (Base, model), {})
    except sqlalchemy.exc.InvalidRequestError:
        table = None
        # the table already exists. Get the model by the table
        for t in list(Base.metadata.tables.values()):
            if name.lower() in t.fullname:
                table = t
                break

        if table is not None:
            try:
                mapper(model, table)
                return model
            except ArgumentError:
                sqlalchemy.inspect(model)
