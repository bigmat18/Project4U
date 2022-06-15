from .Post import (PostCommentCreateView, 
                   PostListView,
                   PostCommentUpdateDestroyCreateView)

from .News import (NewsCreateView, 
                   NewsRUDView, 
                   NewsParagraphUpdateDeleteView,
                   NewsParagraphListCreateView)

from .QuestionAnswer import (ProjectQuestionCreateView,
                             ProjectAnswerCreateView, 
                             ProjectAnswerUpdateDestroyView,
                             ProjectQuestionUpdateDestroyView)

from .TextPost import (TextPostCreateView, 
                       TextPostUpdateDestroyView)