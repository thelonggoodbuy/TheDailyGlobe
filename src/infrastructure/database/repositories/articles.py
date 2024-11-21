from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.infrastructure.database.tables.articles import CategortyTable
from src.domain.entities.users.users_entities import UserEntity
from sqlalchemy import func

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity,\
                                                        ArticleWithPlainTextSectionEntity,\
                                                        ArticleWithVideoSectionEntity


from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy import desc

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticleItem, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema, \
                                                GetSlideshowRequestSchema, \
                                                SlideShowResponseSchema,\
                                                SingleSlideSchema, \
                                                ArticleSectionPlainTextSchema, \
                                                ArticleSectionSlideShowSchema, \
                                                ArticleWithVideoSectionSchema, \
                                                ArticleDetailSchema, \
                                                VideoArticlSections, \
                                                ArticlesFeedTopStoriesRequestSchema, \
                                                SearchSchema


from src.domain.entities.articles.articles_entities import ArticleEntity
from src.infrastructure.database.tables.articles import ArticleTable
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from datetime import datetime, timedelta, timezone
from babel.dates import format_datetime


# # TODO -> application interfaces
class BaseArticleRepository(ABC):
    @abstractmethod
    async def save_section_with_image():
        raise NotImplementedError
    @abstractmethod
    async def return_article_feed():
        raise NotImplementedError


class ArticleAlchemyRepository(BaseArticleRepository, IAlchemyRepository):
    async def save_section_with_image(self, 
                                    article_id,
                                    text,
                                    intex_number_in_article,
                                    image):
        
        new_article_sections_slide_show = ArticleSectionSlideShowEntity(article_id=article_id, 
                                                                        text=text, 
                                                                        intex_number_in_article=intex_number_in_article, 
                                                                        image=image, 
                                                                        section_type='article_section_with_slide_show')
        self._session.add(new_article_sections_slide_show)
        return self._session
    
    async def return_article_feed(self, article_feed_request_schema: ArticlesFeedRequestSchema) -> ArticleFeedResponseSchema:

        offset_value = article_feed_request_schema.pagination_length * article_feed_request_schema.current_pagination_position


        query = (
        select(ArticleEntity)
        .options(selectinload(ArticleEntity.category))
        .filter(ArticleEntity.category_id == article_feed_request_schema.category_id)
        .order_by(ArticleEntity.id)
        .offset(offset_value)
        .limit(article_feed_request_schema.pagination_length)
    )
        article_rows = await self._session.execute(query)
        article_objects = article_rows.scalars().all()


        total_articles_query = (
        select(func.count(ArticleEntity.id))
        .filter(ArticleEntity.category_id == article_feed_request_schema.category_id)
        )
        total_articles = (await self._session.execute(total_articles_query)).scalar()

        is_last_page = (offset_value + article_feed_request_schema.pagination_length) >= total_articles

        article_list = []
        for article_obj in article_objects:
            article = ArticleItem(
                category_title=article_obj.category.title,
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                publication_date=str(article_obj.publication_date),
                is_premium=article_obj.is_premium
            )
            article_list.append(article.model_dump(by_alias=True))

        response = ArticleFeedResponseSchema(error=False, 
                                            message='', 
                                            data={"content": article_list, "last": is_last_page})
        return response
    
    # ===================================================================================================================


    async def return_top_stories_article_feed(self, article_feed_top_stories_request_schema: ArticlesFeedTopStoriesRequestSchema) -> ArticleFeedResponseSchema:

        offset_value = article_feed_top_stories_request_schema.pagination_length * article_feed_top_stories_request_schema.current_pagination_position
        current_date = datetime.now(timezone.utc)


        query = (
        select(ArticleEntity)
        .options(selectinload(ArticleEntity.category))
        .filter(ArticleEntity.publication_date >= current_date - timedelta(days=28))
        .order_by(desc(ArticleEntity.viewing))
        .offset(offset_value)
        .limit(article_feed_top_stories_request_schema.pagination_length)
        )
        article_rows = await self._session.execute(query)
        article_objects = article_rows.scalars().all()

        total_articles_query = (
        select(func.count(ArticleEntity.id))
        .filter(ArticleEntity.publication_date >= current_date - timedelta(days=28))
        )
        total_articles = (await self._session.execute(total_articles_query)).scalar()

        is_last_page = (offset_value + article_feed_top_stories_request_schema.pagination_length) >= total_articles

        article_list = []
        for article_obj in article_objects:
            print('+++')
            # print(f"{article_obj.id}: ")
            print(article_obj.viewing)
            print(article_obj)
            print('+++')
            article = ArticleItem(
                category_title=article_obj.category.title,
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                publication_date=str(article_obj.publication_date),
                is_premium=article_obj.is_premium,
                viewing=article_obj.viewing
            )
            article_list.append(article.model_dump(by_alias=True))

        response = ArticleFeedResponseSchema(error=False, 
                                            message='', 
                                            data={"content": article_list, "last": is_last_page})
        return response
    


    # ===================================================================================================================
    

    async def return_detail_article(self, get_detail_article_schema: ArticlesDetailRequestSchema) -> ArticlesDetailResponseSchema:
        query = select(ArticleEntity)\
                                    .options(selectinload(ArticleEntity.category)).filter(ArticleEntity.id == get_detail_article_schema.article_id)
        article_rows = await self._session.execute(query)
        article_object = article_rows.scalars().first()
        article_dict = ArticleDetailSchema(is_demo=False,
                                        id=article_object.id,
                                        title=article_object.title,
                                        main_image=article_object.main_image,
                                        category_id=article_object.category_id,
                                        lead=article_object.lead,
                                        author=article_object.author,
                                        publication_date=str(article_object.publication_date),
                                        category_title=article_object.category.title,
                                        article_sections=[],
                                        is_premium=article_object.is_premium,
                                        viewing=article_object.viewing)


        sections_list = []

        query_sections_with_plain_text_query = select(ArticleWithPlainTextSectionEntity).filter(ArticleWithPlainTextSectionEntity.article_id == article_object.id)
        query_sections_with_plain_text_rows = await self._session.execute(query_sections_with_plain_text_query)
        query_sections_with_plain_text_objects = query_sections_with_plain_text_rows.scalars().all()

        query_sections_with_slide_show_query = select(ArticleSectionSlideShowEntity).filter(ArticleSectionSlideShowEntity.article_id == article_object.id)
        query_sections_with_slide_show_rows = await self._session.execute(query_sections_with_slide_show_query)
        query_sections_with_slide_show_objects = query_sections_with_slide_show_rows.scalars().all()

        query_sections_with_video_query = select(ArticleWithVideoSectionEntity).filter(ArticleWithVideoSectionEntity.article_id == article_object.id)
        query_sections_with_video_rows = await self._session.execute(query_sections_with_video_query)
        query_sections_with_video_objects = query_sections_with_video_rows.scalars().all()

        sections_list_objects = query_sections_with_plain_text_objects +\
                            query_sections_with_slide_show_objects +\
                            query_sections_with_video_objects

        for article_section in sections_list_objects:
            match article_section.section_type:
                case 'article_sections_with_plain_text':
                    section = ArticleSectionPlainTextSchema(**article_section.to_dict())
                    section.section_type = 'plainText'
                    sections_list.append(section.model_dump(by_alias=True))
                case 'article_section_with_slide_show':
                    section = ArticleSectionSlideShowSchema(**article_section.to_dict())
                    section.section_type = 'slideShow'
                    sections_list.append(section.model_dump(by_alias=True))
                case 'article_section_with_video':
                    section = ArticleWithVideoSectionSchema(**article_section.to_dict())
                    section.section_type = 'video'
                    sections_list.append(section.model_dump(by_alias=True))

        priority = {
            "plainText": 1,
            "slideShow": 2,
            "video": 3,
        }

        sorted_list = sorted(
            sections_list, 
            # key=lambda x: (x.intex_number_in_article, priority[x.section_type])
            key=lambda x: (x["intexNumberInArticle"], priority[x["sectionType"]])
        )

        article_dict.article_sections = sorted_list
        response = ArticlesDetailResponseSchema(error=False, message='', data=article_dict)
        return response
    

    async def update_reading_status(self, article_id: int):

        article = (
        update(ArticleEntity)
        .where(ArticleEntity.id == article_id)
        .values(viewing=ArticleEntity.viewing + 1)
        )
        await self._session.execute(article)
        await self._session.commit()

        return True
    


    async def return_slideshow(self, get_slideshow_schema: GetSlideshowRequestSchema) -> SlideShowResponseSchema:
        
        query_sections_with_slide_show_query = select(ArticleSectionSlideShowEntity).filter(ArticleSectionSlideShowEntity.article_id == get_slideshow_schema.article_id)
        query_sections_with_slide_show_rows = await self._session.execute(query_sections_with_slide_show_query)
        query_sections_with_slide_show_objects = query_sections_with_slide_show_rows.scalars().all()

        result_list = []
        print('--->get_slideshow_schema.article_section_with_slideshow_id:<---')
        print(get_slideshow_schema.article_section_with_slideshow_id)
        print(type(get_slideshow_schema.article_section_with_slideshow_id))
        print('--------------------------------------------------------------')



        for slide in query_sections_with_slide_show_objects:
            print('***')
            print('slide.id')
            print(slide.id)
            print(type(slide.id))
            print('***')
            if slide.id == get_slideshow_schema.article_section_with_slideshow_id:
                print('#1')
                is_opened_status = True
            else:
                print('#2')
                is_opened_status = False
            slide = SingleSlideSchema(
                id=slide.id,
                text=slide.text,
                image=slide.image,
                is_opened=is_opened_status,
                author=slide.author
            )
            print('slide result:')
            print(slide)
            result_list.append(slide.model_dump(by_alias=True))

        

        print('--->result_list<---')
        print(result_list)
        print('------------------')        

        result = SlideShowResponseSchema(error=False, message="", data=result_list)
        print('--->result_schema<---')
        print(result)
        print('------------------')
        return result
        

    async def get_video_section_by_id(self, section_video_id):
        print('==============get==vide====repository=================')
        # query = select(ArticleWithVideoSectionEntity).filter(ArticleWithVideoSectionEntity.id == section_video_id)
        query = (
            select(ArticleWithVideoSectionEntity)
            .filter(ArticleWithVideoSectionEntity.id == section_video_id)
            .options(joinedload(ArticleWithVideoSectionEntity.article).joinedload(ArticleEntity.category))
        )
        query_row = await self._session.execute(query)
        query_sections_with_slide_show_objects = query_row.scalars().first()

        return query_sections_with_slide_show_objects



    async def search_in_article_title(self, search_schema: SearchSchema):
        print('====HEre repository!!!')
        print(search_schema.text)
        # similatiry_threshold = 0.01
        similatiry_threshold = 0.1
        term = search_schema.text

        # Work but only with complete word
        # query = select(ArticleEntity).filter(func.similarity(ArticleEntity.title, term) > similatiry_threshold)

        # work but not correct
        # query = select(ArticleEntity, func.similarity(ArticleEntity.title, term)).where(ArticleEntity.title.bool_op('%')(term))

        # with two fields
        self._session.execute(func.set_limit(0.1))
        columns = func.coalesce(ArticleEntity.title, '').concat(func.coalesce(ArticleEntity.lead, ''))
        columns = columns.self_group()
        query = select(ArticleEntity.title, ArticleEntity.lead, func.similarity(columns, term)).where(columns.bool_op('%')(term),)
        print('---query---')
        print(str(query))
        print('-----------')
        # result = await self._session.query(ArticleEntity).filter(func.similarity(ArticleEntity.title, search_schema.text) > similatiry_threshold)
        query_row = await self._session.execute(query)
        result = query_row.scalars().all()
        print('Repository result:')
        print(result)
        print('=================')
        return result 