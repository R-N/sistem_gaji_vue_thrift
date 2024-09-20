from rpc.gen.user.management.services import TUserManagementService
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.user.structs.ttypes import TUser
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode
import types
from models import models

class TCrudServiceHandler:
    def __init__(self, model, TClass, actions={}, setters={}, require_role=False):
        self.auth_model = models['auth']
        self.model = models[model]
        self.actions = actions
        self.setters = setters
        self.TClass = TClass
        self.require_role = require_role
        self.create_setters(setters)
        self.create_actions(actions)
    
    def get_required_role_action(self, action):
        if not self.actions or action not in self.actions:
            raise NotImplementedError()
        return self.actions[action]

    def require_role_action(self, auth_token, action):
        required_role = self.get_required_role_action(action)
        if required_role:
            return self.auth_model.require_role(auth_token, required_role)
        else:
            return self.auth_model.decode_auth(auth_token)
    
    def get_required_role_setter(self, field):
        if not self.setters or field not in self.setters:
            raise NotImplementedError()
        return self.setters[field]

    def require_role_setter(self, auth_token, field):
        required_role = self.get_required_role_setter(field)
        if required_role:
            return self.auth_model.require_role(auth_token, required_role)
        else:
            return self.auth_model.decode_auth(auth_token)

    def create_setters(self, setters):
        for field, required_role in setters.items():
            def f(auth_token, id, value, field=field):
                print(field, value)
                return self.set_field(field, auth_token, id, value, required_role=required_role)
            f.name = f"set_{field}"
            setattr(self, f.name, f)
            f.name = f"TCrudServiceHandler.{f.name}"

    def create_actions(self, actions):
        for action, required_role in actions.items():
            f = types.MethodType(getattr(TCrudServiceHandler, action), self)
            # def f(*args, **kwargs):
            #     return getattr(TCrudServiceHandler, action)(self, *args, **kwargs)
            # f.name = action
            setattr(self, action, f)
            # f.name = f"TCrudServiceHandler.{f.name}"

    def fetch(self, auth_token, query=None):
        actor = self.require_role_action(auth_token, "fetch")
        db_objs = self.model.fetch(query, actor=actor)
        return [o.fill(self.TClass()) for o in db_objs]

    def get(self, auth_token, id):
        actor = self.require_role_action(auth_token, "get")
        db_obj = self.model.get(id)
        return db_obj.fill(self.TClass())

    def create(self, auth_token, form):
        actor = self.require_role_action(auth_token, "create")
        db_obj = self.model.create(form, actor=actor)
        self.model.commit()
        obj = db_obj.fill(self.TClass())
        return obj
    
    def set_field(self, field, auth_token, id, value, required_role=None):
        print("set", field, value)
        if required_role is not None:
            actor = self.auth_model.require_role(auth_token, required_role)
        else:
            actor = self.require_role_setter(auth_token, field)
        db_obj = self.model.get(id, actor=actor)
        f = getattr(self.model, f"set_{field}")
        f(db_obj, value, actor=actor)
        self.model.commit()

    def delete(self, auth_token, id):
        actor = self.require_role_action(auth_token, "delete")
        db_obj = self.model.get(id, actor=actor)
        self.model.delete(db_obj, actor=actor)
        self.model.commit()
