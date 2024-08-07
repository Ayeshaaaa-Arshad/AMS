# Passing the context in the first base page in which header and footer is set so through context processor we can send context
def user_context(request):
    return {
        'user': request.user,
        'id':request.user.id,
        'role': request.user.groups.all().first()
    }
