from .Post import (PostCommentCreateView, 
                   PostListView,
                   PostCommentUpdateDestroyCreateView)

from .News import (NewsCreateView, 
                   NewsRUDView)

from .NewsParagraph import (NewsParagraphListCreateView,
                            NewsParagraphUpdateDeleteView)

from .QuestionAnswer import (ProjectQuestionCreateView,
                             ProjectAnswerCreateView, 
                             ProjectAnswerUpdateDestroyView,
                             ProjectQuestionUpdateDestroyView)

from .TextPost import (TextPostCreateView, 
                       TextPostUpdateDestroyView)