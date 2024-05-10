

def category_schema(category):
    return {
        'id': category.id,
        'title': category.title,
        'parent': {
            'id': category.parent.id,
            'title': category.parent.title,
            'parent': {
                'id': category.parent.parent.id,
                'title': category.parent.parent.title,
                "parent": None
            }
        }
    }
