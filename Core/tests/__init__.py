from .BaseTestCase import BaseTestCase
from .ConstraintsTestCase import ConstraintsTestCase
from .AbstractFileTestCase import AbstractFileTestCase
from .ProjectModelTestCase import ProjectModelTestCase
from .ShowcaseModelTestCase import ShowcaseModelTestCase

from Users.tests import (UserTestCase, 
                         SkillTestCase, 
                         UserSkillTestCase,
                         ExternalProjectTestCase,
                         UserEducationTestCase,
                         LoginRegistrationTestCase)


from Projects.tests import (ProjectsTestCase,
                            UserProjectTestCase,
                            RoleTestCase, 
                            ShowcaseTestCase,
                            MessageTestCase,
                            ProjectTagTestCase,
                            EventTestCase, 
                            PollTestCase)

from Community.tests import (NewsTestCase,
                             NewsParagraphTestCase)