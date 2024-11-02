from abc import ABC, abstractmethod
from src.application.interfaces.repositories import IAlchemyRepository
from src.infrastructure.database.tables.comments import CommentEntity





class BaseCommentsRepository(ABC):
    @abstractmethod
    async def create_comment():
        raise NotImplementedError
    


class CommentsAlchemyRepository(BaseCommentsRepository, IAlchemyRepository):
    async def create_comment(self, new_article_sections_slide_show, user_id):
        print('--->user id in repositpry<----')
        print(user_id)
        print('------------------------------')
        new_comment = CommentEntity(text=new_article_sections_slide_show.text,
                                    user_id=user_id,
                                    article_id=new_article_sections_slide_show.article_id)
        self._session.add(new_comment)
        
        await self._session.commit()
        await self._session.refresh(new_comment)

        return new_comment