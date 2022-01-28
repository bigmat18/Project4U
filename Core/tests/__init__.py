from .BaseTestCase import BaseTestCase
from .ConstraintsTestCase import ConstraintsTestCase
from .AbstractFileTestCase import AbstractFileTestCase

from Users.tests import (UserTestCase, SkillTestCase, UserSkillTestCase,
                         ExternalProjectTestCase, UserEducationTestCase,
                         LoginRegistrationTestCase)


from Projects.tests import (ProjectsTestCase,UserProjectTestCase,
                            RoleTestCase, ShowcaseTestCase,
                            MessageTestCase,ProjectTagTestCase)