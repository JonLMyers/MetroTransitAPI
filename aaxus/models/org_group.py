from mongoengine import *
from aaxus.models.user import User

class OrgGroup(Document):
    name = StringField(max_length=50, required=True, unique=True)
    description = StringField(max_length=256*8)
    members = ListField(ReferenceField(User))
    administrators = ListField(ReferenceField(User))
    #active_tickets = ListField(StringField(max_length=256))
    #closed_tickets = ListField(max_legth=256)

    meta = {'allow_inheritance': True}

    def add_admin(self, admin):
        for user in self.administrators:
            if user == admin:
                return False
        self.administrators.append(admin)

    def remove_admin(self, admin):
        for user in self.members:
            if user == admin:
                self.administrators.remove(admin)
                return True
        return False

    def add_member(self, member):
        for user in self.members:
            if user == member:
                return False
        self.members.append(member)

    def remove_member(self, member):
        for user in self.members:
            if user == member:
                self.members.remove(member)
                return True
        return False

    def is_admin(self, name):
        for admin in self.administrators:
            if admin.username == name:
                return True
        return False
    
    @classmethod
    def find_by_name(self, org_name):
        for org_group in OrgGroup.objects(name = org_name):
            return org_group
        return False