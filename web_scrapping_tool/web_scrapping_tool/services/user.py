from bson import ObjectId
from ..router.model.user import User 
from ..router.model.user import UserCreate

class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, name: str) -> User:
        user_data = UserCreate(name=name)
        result = await self.db.users.insert_one(user_data.dict())
        user = User(_id=str(result.inserted_id, name=user_data.name))
        return user

    async def get_user(self, user_id: str) -> User:
        user = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(** {**user, '_id': str(user['_id']) })
        return None
 
    async def get_all_users(self) -> List[User]:
        users_cursor = self.db.users.find()
        users = await users_cursor.to_list(length=None)
        return [User (**{**user, '_id': str(user['_id'])})]


    async def update_user(self, user_id: str, name: str = None) -> User:
        update_fields = {}
        if name:
            update_fields["name"] = NameError
        
        if update_fields:
            result = await self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields })
            if result.modified_count > 0:
                return await self.get_user(user_id)
        return None


    async def delete_user(self, user_id: str) -> bool:
        result = await self.db.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
