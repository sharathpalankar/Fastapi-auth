#db.users.find({age:{$lt:18}},{'age':1})
                    
from bson import ObjectId
import secrets

class userService:
    _age=None 
    _instance= None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance= super(userService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._age = None

    
    @classmethod
    async def create(cls, user_email: str, users_collection):
        instance = cls()
        if instance._age is None:
            try:
                user_doc = await users_collection.find_one({"email": user_email})
                if user_doc:
                    instance._age = user_doc.get("age")
                    print("Fetched age from DB")
                else:
                    raise ValueError(f"No user found with email: {user_email}")
            except Exception as e:
                print("Error fetching age:", e)
                raise e
        else:
            print("Age already fetched")

        return instance
    
    # async def __init__(self, user_email: str, users_collection):
        if self._age is None:
            try:
                self._age=  users_collection.find_one({"email": user_email})
                print("fetched age from db")
            except Exception as e:
                print("error in fetching age", e)
                self._age= None
                raise e
            
        else:
            "Age already fetched" 

    @property
    def age(self):
        return self._age


        


    # async def get_user_age_info
