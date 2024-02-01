from Models.User import User

def add_user_service(req):
    try:
        User(name=req['name'],client_id=req['id'],favorite_description=[],profile=[]).save()
        return "Save successful"
    except Exception as e:
        return f"Save operation failed : {e}"
    
def delete_user_service(req):
    try:
        user_to_delete=User.nodes.get(client_id=req['id'])
        user_to_delete.delete()
        return "Successful deletion!"
    except Exception as e:
        return f"Delete operation failed: {e}"
        