from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.database.repositories.comments import BaseCommentsRepository
from src.main.config.settings import Settings
from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.presentation.schemas.comments import CreateCommentRequestData,\
                                                CommentSchema, \
                                                CommentResponseData, \
                                                AllCommentRequestData, \
                                                CommentListrIteamSchema

from src.application.interfaces.services import ITokenService






class CreateCommentInteractor(BaseInteractor):

    def __init__(self,
                db_session: IDatabaseSession,
                comment_repository: BaseCommentsRepository,
                settings: Settings,
                token_service: ITokenService):
        
        self.db_session = db_session
        self.comment_repository = comment_repository
        self.settings = settings
        self.token_service = token_service


    async def __call__(self, 
                       create_comment_schema: CreateCommentRequestData,
                       token: str) -> CommentResponseData:
        
        user_obj = await self.token_service.get_user_by_token(token.credentials)
        if user_obj.is_valid:
            comment_entity = await self.comment_repository.create_comment(create_comment_schema, user_obj.id)
            comment_obj = CommentSchema(is_sender=True, user_email=user_obj.user_email, **comment_entity.to_dict())
            
            result = CommentResponseData(
                error=False,
                message="",
                data=comment_obj
            )
        else:
            result = CommentResponseData(
                error=True,
                message=user_obj.error_text,
                data=None
            )

        return result
    

class ShowCommentInteractor(BaseInteractor):
    def __init__(self,
                db_session: IDatabaseSession,
                comment_repository: BaseCommentsRepository,
                settings: Settings,
                token_service: ITokenService):
        
        self.db_session = db_session
        self.comment_repository = comment_repository
        self.settings = settings
        self.token_service = token_service

    async def __call__(self, 
                       create_comment_schema: AllCommentRequestData,
                       token: str) -> CommentResponseData:

        user_obj = await self.token_service.get_user_by_token(token.credentials)
        if user_obj.is_valid:
            
            comment_entity = await self.comment_repository.return_all_comments(create_comment_schema, user_obj.id)
            comment_list = []
            for comment_obj in comment_entity:
                if comment_obj.user_id == user_obj.id:
                    comment = CommentListrIteamSchema(id=comment_obj.id, 
                                  text=comment_obj.text, 
                                  is_sender=True,
                                  user_email=comment_obj.user.email
                                  )
                else:
                    comment = CommentListrIteamSchema(id=comment_obj.id, 
                                  text=comment_obj.text, 
                                  is_sender=False,
                                  user_email=comment_obj.user.email
                                  )
                comment_list.append(comment)

                print('=================================')
                print(comment_list)
                print('=================================')

            result = CommentResponseData(error=False, message="", data=comment_list)
        else:
            result = CommentResponseData(
                error=True,
                message=user_obj.error_text,
                data=None
            )



        return result