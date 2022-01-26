from .BaseTestCase import BaseTestCase
from .UserModelTest import UserModelTestCase

from Users.tests import (UserTestCase, SkillTestCase, UserSkillTestCase,
                         ExternalProjectTestCase, UserEducationTestCase,
                         LoginRegistrationTestCase)


from Projects.tests import (ProjectsTestCase,UserProjectTestCase,
                            RoleTestCase, ShowcaseTestCase,
                            MessageTestCase,ProjectTagTestCase)