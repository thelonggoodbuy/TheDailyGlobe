from sqlalchemy import func

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity,\
                                                        ArticleWithPlainTextSectionEntity,\
                                                        ArticleWithVideoSectionEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseArticleRepository

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy import desc, union_all

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
                                                ArticlesFeedTopStoriesRequestSchema, \
                                                SearchSchema,\
                                                PopularArticleForSearchItem,\
                                                RelatedStoriesResponseSchema


from src.domain.entities.articles.articles_entities import ArticleEntity
from sqlalchemy.orm import selectinload
from sqlalchemy import update
from datetime import datetime, timedelta, timezone

import time



class ArticleAlchemyRepository(BaseArticleRepository, IAlchemyRepository):
    async def save_section_with_image(self, 
                                    article_id,
                                    text,
                                    index_number_in_article,
                                    image):
        
        new_article_sections_slide_show = ArticleSectionSlideShowEntity(article_id=article_id, 
                                                                        text=text, 
                                                                        index_number_in_article=index_number_in_article, 
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
       

    async def return_most_popular_articles(self, article_most_popular_request_schema: ArticlesFeedTopStoriesRequestSchema) -> ArticleFeedResponseSchema:
        
        offset_value = article_most_popular_request_schema.pagination_length * article_most_popular_request_schema.current_pagination_position
        current_date = datetime.now(timezone.utc)

        query = (
        select(ArticleEntity)
        .options(selectinload(ArticleEntity.category))
        .filter(ArticleEntity.publication_date >= current_date - timedelta(days=28))
        .order_by(desc(ArticleEntity.viewing))
        .offset(offset_value)
        .limit(article_most_popular_request_schema.pagination_length)
        )
        article_rows = await self._session.execute(query)
        article_objects = article_rows.scalars().all()

        total_articles_query = (
        select(func.count(ArticleEntity.id))
        .filter(ArticleEntity.publication_date >= current_date - timedelta(days=28))
        )
        total_articles = (await self._session.execute(total_articles_query)).scalar()

        is_last_page = (offset_value + article_most_popular_request_schema.pagination_length) >= total_articles

        article_list = []
        for article_obj in article_objects:

            article = PopularArticleForSearchItem(
                # category_title=article_obj.category.title,
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                publication_date=str(article_obj.publication_date),
                # is_premium=article_obj.is_premium,
                viewing=article_obj.viewing
            )
            article_list.append(article.model_dump(by_alias=True))

        response = ArticleFeedResponseSchema(error=False, 
                                            message='', 
                                            data={"content": article_list, "last": is_last_page})
        return response
       


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
            key=lambda x: (x["indexNumberInArticle"], priority[x["sectionType"]])
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

        for slide in query_sections_with_slide_show_objects:
            if slide.id == get_slideshow_schema.article_section_with_slideshow_id:
                is_opened_status = True
            else:
                is_opened_status = False
            slide = SingleSlideSchema(
                id=slide.id,
                text=slide.text,
                image=slide.image,
                is_opened=is_opened_status,
                author=slide.author
            )
            result_list.append(slide.model_dump(by_alias=True))

        result = SlideShowResponseSchema(error=False, message="", data=result_list)
        return result
        
    async def get_video_section_by_id(self, section_video_id):
        query = (
            select(ArticleWithVideoSectionEntity)
            .filter(ArticleWithVideoSectionEntity.id == section_video_id)
            .options(joinedload(ArticleWithVideoSectionEntity.article).joinedload(ArticleEntity.category))
        )
        query_row = await self._session.execute(query)
        query_sections_with_slide_show_objects = query_row.scalars().first()

        return query_sections_with_slide_show_objects

    async def search_in_article_title(self, search_schema: SearchSchema):
        similarity_threshold = 0.05
        term = search_schema.text

        start_time = time.time()

        title_similarity = func.similarity(ArticleEntity.title, term)
        lead_similarity = func.similarity(ArticleEntity.lead, term)
        plain_text_similarity = func.max(func.similarity(ArticleWithPlainTextSectionEntity.text, term))
        slide_show_similarity = func.max(func.similarity(ArticleSectionSlideShowEntity.text, term))

        # Вычисляем максимальное значение "релевантности"
        relevance = func.greatest(
            title_similarity,
            lead_similarity,
            plain_text_similarity,
            slide_show_similarity
        )

        # Основной запрос
        query = (
            select(
                ArticleEntity,
                relevance.label("relevance")
            )
            .join(
                ArticleWithPlainTextSectionEntity,
                ArticleEntity.id == ArticleWithPlainTextSectionEntity.article_id,
                isouter=True
            )
            .join(
                ArticleSectionSlideShowEntity,
                ArticleEntity.id == ArticleSectionSlideShowEntity.article_id,
                isouter=True
            )
            .where(
                func.greatest(
                    title_similarity,
                    lead_similarity,
                    func.coalesce(func.similarity(ArticleWithPlainTextSectionEntity.text, term), 0),
                    func.coalesce(func.similarity(ArticleSectionSlideShowEntity.text, term), 0)
                ) > similarity_threshold
            )
            .group_by(ArticleEntity.id)
            .order_by(relevance.desc())
            .limit(10)
        )

        query_row = await self._session.execute(query)
        result = query_row.scalars().all()
        
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.5f} seconds")

        return result 
    

    async def return_related_stories(self, article_id: int):
        query = (
            select(ArticleEntity)
            .filter(ArticleEntity.id == article_id)
        )
        query_rows = await self._session.execute(query)
        article = query_rows.scalars().first()

        print('===>Category id:<===')
        print(article.category_id)
        print('====================')



        query = (select(ArticleEntity)
            .filter(ArticleEntity.category_id == article.category_id, ArticleEntity.id != article_id)
            .order_by(desc(ArticleEntity.viewing))
            .limit(3)
            )
        


        article_rows = await self._session.execute(query)
        article_objects = article_rows.scalars().all()


        article_list = []
        for article_obj in article_objects:
            article = PopularArticleForSearchItem(
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                publication_date=str(article_obj.publication_date),
                viewing=article_obj.viewing
            )
            article_list.append(article.model_dump(by_alias=True))

        response = RelatedStoriesResponseSchema(error=False, 
                                            message='', 
                                            data=article_list)
        return response

