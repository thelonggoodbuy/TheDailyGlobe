from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.database.repositories.comments import BaseCommentsRepository
from src.main.config.settings import Settings
from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.presentation.schemas.comments import CreateCommentRequestData, CommentSchema, CommentResponseData
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

        # print('***--->')
        # print('create_comment_schema')
        # print(create_comment_schema)
        # print('token')
        # print(token)
        # print('user_obj')
        # print(user_obj)
        # print('***--->')

        # user_obj = await self.token_service.get_user_by_token(token)
        if user_obj.is_valid:
            comment_entity = await self.comment_repository.create_comment(create_comment_schema, user_obj.id)
        # print('+++comment_entity+++')
        # print(comment_entity)
        # print(comment_entity.to_dict())
        # print('********************')
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