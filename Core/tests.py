from .BaseTestCase import BaseTestCase

from Users.tests.Auth import LoginRegistrationTestCase
from Users.tests.User import UsersTestCase
from Users.tests.Skill import SkillTestCase, UserSkillTestCase
from Users.tests.ExternalProject import ExternalProjectTestCase
from Users.tests.UserEducation import UserEducationTestCase

from Projects.tests.Project import ProjectsTestCase
from Projects.tests.Role import RoleTestCase
from Projects.tests.UserProject import UserProjectTestCase