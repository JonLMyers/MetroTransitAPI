from mongoengine import *
from aaxus.models.user import User
from aaxus.models.org_group import OrgGroup

class Organization(Document):
    name = StringField(max_length=50, required=True, unique=True)
    join_token = StringField(max_length=256, unique=True)
    org_groups = ListField(ReferenceField(OrgGroup))
    members = ListField(ReferenceField(User))
    administrators = ListField(ReferenceField(User))

    meta = {'allow_inheritance': True}

    def add_org_group(self, group):
        for org_group in org_groups:
            print (org_group)
            if org_groups == group:
                return False
        self.org_groups.append(group)

    def remove_org_group(self, group):
        for org_group in self.org_groups:
            if org_group == group:
                self.org_groups.remove(group)
                return True
        return False

    def add_admin(self, admin):
        for user in self.administrators:
            if user == admin:
                return False
        self.administrators.append(admin)

    def remove_admin(self, admin):
        for user in self.administrators:
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

    def is_member(self, member):
        for user in self.members:
            if user == member:
                return True
        return False

    def find_org_group_by_name(self, org_name):
        for group in self.org_groups:
            if group.name == org_name:
                return group

    def find_all_org_groups(self):
        groups = []
        for group in self.org_groups:
            groups.append(group)
        return groups

    @classmethod
    def find_by_name(self, org_name):
        for org in Organization.objects(name = org_name):
            return org
        return False

    @classmethod
    def find_all(self):
        orgs = []
        for org in Organization.objects():
            orgs.append(org.name)
        return orgs
