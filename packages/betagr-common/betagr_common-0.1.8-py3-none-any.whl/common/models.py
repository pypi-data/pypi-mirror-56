import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


class SSO:
    metadata = sa.MetaData()

    def __init__(self):
        self.user = self.user()
        self.group = self.group()
        self.permission = self.permission()
        self.user_group = self.user_group()
        self.group_permission = self.group_permission()
        self.session = self.session()

    @classmethod
    def user(cls):
        tb_user = sa.Table(
            'tb_user', cls.metadata,
            sa.Column('user_id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String(40), nullable=False, unique=True),
            sa.Column('password', sa.String(255), nullable=False))

        return tb_user

    @classmethod
    def group(cls):
        tb_group = sa.Table(
            'tb_group', cls.metadata,
            sa.Column('group_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False, unique=True))

        return tb_group

    @classmethod
    def permission(cls):
        tb_permission = sa.Table(
            'tb_permission', cls.metadata,
            sa.Column('permission_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False, unique=True))

        return tb_permission

    @classmethod
    def user_group(cls):
        tb_user_group = sa.Table(
            'tb_user_group', cls.metadata,
            sa.Column('user_id', sa.Integer, sa.ForeignKey('tb_user.user_id')),
            sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.group_id')))

        return tb_user_group

    @classmethod
    def group_permission(cls):
        tb_group_permission = sa.Table(
            'tb_group_permission', cls.metadata,
            sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.group_id')),
            sa.Column('permission_id', sa.Integer, sa.ForeignKey('tb_permission.permission_id')))

        return tb_group_permission

    @classmethod
    def session(cls):
        tb_session = sa.Table(
            'tb_session', cls.metadata,
            sa.Column('session_id', UUID(as_uuid=True), nullable=False, unique=True),
            sa.Column('user_id', sa.Integer, nullable=False, unique=True))

        return tb_session


class Parser:
    metadata = sa.MetaData()

    def __init__(self):
        self.link = self.link()
        self.real_team = self.real_team()
        self.team = self.team()

    @classmethod
    def link(cls):
        tb_link = sa.Table(
            'tb_link', cls.metadata,
            sa.Column('link_id', sa.Integer, primary_key=True),
            sa.Column('site_name', sa.String(25), nullable=False),
            sa.Column('link', sa.String(100), nullable=False, unique=True),
            sa.Column('created_on', sa.DateTime(), nullable=False),
            sa.Column('attributes', sa.JSON, nullable=False))

        return tb_link

    @classmethod
    def real_team(cls):
        tb_real_team = sa.Table(
            'tb_real_team', cls.metadata,
            sa.Column('real_team_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(80), nullable=False, unique=True),
            sa.Column('created_on', sa.DateTime(), nullable=False))

        return tb_real_team

    @classmethod
    def team(cls):
        tb_team = sa.Table(
            'tb_team', cls.metadata,
            sa.Column('team_id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(80), nullable=False),
            sa.Column('created_on', sa.DateTime(), nullable=False),
            sa.Column('site_name', sa.String(25), nullable=False),
            sa.Column('real_team_id', sa.Integer, sa.ForeignKey('tb_real_team.real_team_id')),
            sa.Column('link_id', sa.Integer, sa.ForeignKey('tb_link.link_id')))

        return tb_team
