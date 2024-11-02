from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.infrastructure.database.tables.articles import CategortyTable
from src.domain.entities.users.users_entities import UserEntity

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity,\
                                                        ArticleWithPlainTextSectionEntity,\
                                                        ArticleWithVideoSectionEntity


from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash

from sqlalchemy import select

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
                                                VideoArticlSections


from src.domain.entities.articles.articles_entities import ArticleEntity
from sqlalchemy.orm import selectinload

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
        # response = ArticleFeedResponseSchema(articles=[])
        print('=====article_objects=====')
        print(article_objects)
        print(type(article_objects))
        print('=========================')
        article_list = []
        for article_obj in article_objects:
            # print('====>article_obj.publication_date<======')
            # print(article_obj.publication_date)
            # print(type(article_obj.publication_date))
            # print('========================================')
            article = ArticleItem(
                category_title=article_obj.category.title,
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                # publication_date=(format_datetime(article_obj.publication_date, format='MMMM dd, yyyy', locale='uk')).capitalize()
                publication_date=str(article_obj.publication_date)
            )
            article_list.append(article.model_dump(by_alias=True))

        print('===>article_list<===')
        print(article_list)
        print(type(article_list))
        print('====================')

        response = ArticleFeedResponseSchema(error=False, message='', data=article_list)
        
        # print('===>REPOSITORY===DATA<===')
        # print(response)
        # print('=========================')
        
        return response
    

    async def return_detail_article(self, get_detail_article_schema: ArticlesDetailRequestSchema) -> ArticlesDetailResponseSchema:
        print('REPOSITORY WORK!!!')
        query = select(ArticleEntity)\
                                    .options(selectinload(ArticleEntity.category)).filter(ArticleEntity.id == get_detail_article_schema.article_id)
        article_rows = await self._session.execute(query)
        article_object = article_rows.scalars().first()
        # article_dict = article_object.to_dict()
        article_dict = ArticleDetailSchema(id=article_object.id,
                                        title=article_object.title,
                                        main_image=article_object.main_image,
                                        category_id=article_object.category_id,
                                        lead=article_object.lead,
                                        author=article_object.author,
                                        publication_date=str(article_object.publication_date),
                                        category_title=article_object.category.title,
                                        article_sections=[])
        # article_dict['category_title'] = article_object.category.title

        print('==================article_dict=====================')
        print(article_dict)
        print('===================================================')

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
            # sections_list.append(article_section.to_dict())
            match article_section.section_type:
                case 'article_sections_with_plain_text':
                    # print("======article_section.to_dict()========")
                    # print(article_section.to_dict())
                    # print("=======================================")
                    section = ArticleSectionPlainTextSchema(**article_section.to_dict())
                    sections_list.append(section.model_dump(by_alias=True))
                case 'article_section_with_slide_show':
                    section = ArticleSectionSlideShowSchema(**article_section.to_dict())
                    sections_list.append(section.model_dump(by_alias=True))
                case 'article_section_with_video':
                    section = ArticleWithVideoSectionSchema(**article_section.to_dict())
                    sections_list.append(section.model_dump(by_alias=True))

        priority = {
            "article_sections_with_plain_text": 1,
            "article_section_with_slide_show": 2,
            "article_section_with_video": 3,
        }

        # print("=====sections_list=====")
        # print(sections_list)
        # print("=======================")

        sorted_list = sorted(
            sections_list, 
            # key=lambda x: (x.intex_number_in_article, priority[x.section_type])
            key=lambda x: (x["intexNumberInArticle"], priority[x["sectionType"]])
        )

        # sorted_formated_list = list(map(lambda x: x.model_dump(by_alias=True), sorted_list))
        sorted_formated_list = []
        import pprint
        # print('=======SECTION List===========')
        # pprint.pprint(sorted_list)
        # print('==============================')
        # article_dict['article_sections'] = sorted_list
        article_dict.article_sections = sorted_list

        print('=======SECTION List===========')
        pprint.pprint(article_dict)
        print('==============================')

        response = ArticlesDetailResponseSchema(error=False, message='', data=article_dict.model_dump(by_alias=True))
        print('===============================================')
        print(response)
        print('===============================================')
        return response
    

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
            print(print(slide.id))
            print(type(slide.id))
            print('***')
            if slide.id == get_slideshow_schema.article_section_with_slideshow_id:
                is_opened_status = True
            else:
                is_opened_status = False
            slide = SingleSlideSchema(
                id=slide.id,
                text=slide.text,
                image=slide.image,
                is_opened=is_opened_status
            )
            result_list.append(slide.model_dump(by_alias=True))
        result = SlideShowResponseSchema(error=False, message="", data=result_list)
        return result
        

    async def get_video_section_by_id(self, section_video_id):
        query = select(ArticleWithVideoSectionEntity).filter(ArticleWithVideoSectionEntity.id == section_video_id)
        query_row = await self._session.execute(query)
        query_sections_with_slide_show_objects = query_row.scalars().first()

        return query_sections_with_slide_show_objects