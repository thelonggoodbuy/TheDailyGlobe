from abc import ABC, abstractmethod
from src.application.interfaces.repositories import IAlchemyRepository, BaseCommentsRepository
from src.infrastructure.database.tables.comments import CommentEntity
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload



class CommentsAlchemyRepository(BaseCommentsRepository, IAlchemyRepository):

    async def create_comment(self, new_article_sections_slide_show, user_id):
        new_comment = CommentEntity(text=new_article_sections_slide_show.text,
                                    user_id=user_id,
                                    article_id=new_article_sections_slide_show.article_id)
        self._session.add(new_comment)
        await self._session.commit()
        await self._session.refresh(new_comment)

        return new_comment
    


    async def return_all_comments(self, create_comment_schema, user_id):
        query = select(CommentEntity).options(selectinload(CommentEntity.user))\
                                    .filter(CommentEntity.article_id==create_comment_schema.article_id)\
                                    .order_by(desc(CommentEntity.id))
        comments_rows = await self._session.execute(query)
        comments = comments_rows.scalars().all()

        return comments