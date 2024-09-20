from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

import db
from db.entities.general import DbUser
from db.errors import UniqueError
from utils.util import get_obj_attrs

load_dotenv()

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

class CrudModel:
    def __init__(self, DbClass, TError, TErrorCode, name_field="nama", actions={}, setters={}):
        self.DbClass = DbClass
        self.TError = TError
        self.TErrorCode = TErrorCode
        self.name_field = name_field
        self.actions = actions
        self.setters = setters
        self.create_setters(setters)

    def commit(self):
        try:
            db.commit()
        except IntegrityError as ex:
            self.parse_error(ex)
            raise
        
    def get_required_role_action(self, action):
        if not self.actions or action not in self.actions:
            raise NotImplementedError()
        return self.actions[action]

    def require_role_action(self, actor, action):
        required_role = self.get_required_role_action(action)
        if required_role:
            return self.validate_actor_role(actor, required_role)
    
    def get_required_role_setter(self, field):
        if not self.setters or field not in self.setters:
            raise NotImplementedError()
        return self.setters[field]

    def require_role_setter(self, actor, field):
        required_role = self.get_required_role_setter(field)
        if required_role:
            return self.validate_actor_role(actor, required_role)

    def create_setters(self, setters):
        for field, _required_role in setters.items():
            def f(db_obj, value, actor=None, required_role=None, field=field):
                print(field, value)
                return self.set_field(field, db_obj, value, actor=actor, required_role=_required_role or required_role)
            f.name = f"set_{field}"
            setattr(self, f.name, f)
            f.name = f"CrudModel.{f.name}"

    def get_by_id(self, id, actor=None, required_role=None):
        required_role = required_role or self.get_required_role_action("get")
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        db_obj = db.session.query(self.DbClass).filter(self.DbClass.id == id).scalar()
        if not db_obj:
            raise self.TError(self.TErrorCode.NOT_FOUND)
        return db_obj

    def get(self, id, actor=None, required_role=None):
        return self.get_by_id(id, actor=actor, required_role=required_role)

    def get_by_field_silent(self, field, value, actor=None, required_role=None):
        required_role = required_role or self.get_required_role_action("get")
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        return db.session.query(self.DbClass).filter(
            self.DbClass[field] == value
        ).scalar()

    def get_by_field(self, field, value, actor=None, required_role=None):
        db_obj = self.get_by_field_silent(field, value, actor=actor, required_role=required_role)
        if not db_obj:
            raise self.TError(self.TErrorCode.NOT_FOUND)
        return db_obj
    
    def validate_actor_role(self, actor_role, role):
        return DbUser.validator().validate_actor_role(actor_role, role)

    def fetch(self, query=None, actor=None, required_role=None, execute=True):
        required_role = required_role or self.get_required_role_action("fetch")
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        db_query = db.session.query(self.DbClass)
        args = []
        if hasattr(self.DbClass, "enabled"):
            args.append(self.DbClass.enabled.desc())
        if hasattr(self.DbClass, "verified"):
            args.append(self.DbClass.verified.desc())
        if hasattr(self.DbClass, self.name_field):
            args.append(getattr(self.DbClass, self.name_field).desc())
        db_query = db_query.order_by(*args)
        if query:
            for k, v in get_obj_attrs(query).items():
                if v is not None and k not in ("limit", "offset"):
                    db_query = db_query.filter(getattr(self.DbClass, k) == v)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        if execute:
            return db_query.all()
        return db_query

    def set_field(self, field, db_obj, value, actor=None, required_role=None):
        print("set", field, value)
        required_role = required_role or self.get_required_role_setter(field)
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        if hasattr(db_obj, "role"):
            self.validate_actor_role(actor, db_obj.role)
        if field == "role":
            self.validate_actor_role(actor, value)
        setattr(db_obj, field, value)
        db.session.add(db_obj)

    def create(self, form, actor=None, required_role=None):
        required_role = required_role or self.get_required_role_action("create")
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        if hasattr(form, "role"):
            self.validate_actor_role(actor, form.role)
        
        db_obj = self.DbClass()
        for k, v in get_obj_attrs(form).items():
            if v is not None:
                setattr(db_obj, k, v)

        db.session.add(db_obj)
        return db_obj

    def delete(self, db_obj, actor=None, required_role=None):
        required_role = required_role or self.get_required_role_action("delete")
        if required_role is not None:
            self.validate_actor_role(actor, required_role)
        if hasattr(db_obj, "role"):
            self.validate_actor_role(actor, db_obj.role)
        if hasattr(db_obj, "verified") and db_obj.verified:
            raise self.TError(self.TErrorCode.CANNOT_DELETE_VERIFIED)
        db.session.delete(db_obj)
