from app.domain.models.business import BusinessCategory, BusinessContent

class SqlBusinessRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_categories(self):
        try:
            categories_query = """
                SELECT id, name, description, order_num, created_at 
                FROM business_categories 
                ORDER BY order_num
            """
            category_rows = self.db.execute_query(categories_query)
            
            categories = []
            for row in category_rows:
                category = BusinessCategory(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    order=row['order_num'],
                    created_at=row['created_at']
                )
                
                contents_query = """
                    SELECT id, category_id, name, route, icon, order_num, is_active, created_at
                    FROM business_contents 
                    WHERE category_id = ? AND is_active = 1
                    ORDER BY order_num
                """
                content_rows = self.db.execute_query(contents_query, (category.id,))
                
                category.contents = [
                    BusinessContent(
                        id=content_row['id'],
                        category_id=content_row['category_id'],
                        name=content_row['name'],
                        route=content_row['route'],
                        icon=content_row['icon'],
                        order=content_row['order_num'],
                        is_active=bool(content_row['is_active']),
                        created_at=content_row['created_at']
                    )
                    for content_row in content_rows
                ]
                
                categories.append(category)
            
            return categories
            
        except Exception as e:
            raise Exception(f"데이터베이스 오류: {str(e)}")