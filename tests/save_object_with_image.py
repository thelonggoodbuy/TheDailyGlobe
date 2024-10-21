from sqlalchemy.ext.asyncio import async_sessionmaker
import os
from sqlalchemy.ext.asyncio import create_async_engine
from src.infrastructure.database.tables.articles import ArticleSectionSlideShowEntity, ArticleEntity
from sqlalchemy import select

ASYNCSQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://maxim:12345qwert@admin_db:5432/db_admin"

engine = create_async_engine(ASYNCSQLALCHEMY_DATABASE_URL)





async def save_test_obj_with_photo(article_id, text, intex_number_in_article, image):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        print('===>saving image procedure<===')
        print(image)
        query = (
                select(ArticleEntity)
                .filter(ArticleEntity.id == int(article_id)).limit(1)
            )
        result = await session.execute(query)
        article = result.scalars().one()

        article_section = ArticleSectionSlideShowEntity(text='some text',
                                                        intex_number_in_article=1,
                                                        image=image)
        article_section.article = article
        print('==============================')
        session.add(article_section)
        await session.commit()

        # with open(
        #     f"media/external_storage/{message_from_socket.photo}", "rb"
        # ) as photo:
        #     message.photo = photo
        #     session.add(message)
        #     await session.commit()
        # os.remove(f"media/external_storage/{message_from_socket.photo}")

        
    return article_section