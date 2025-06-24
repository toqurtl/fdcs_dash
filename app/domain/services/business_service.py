from app.domain.models.business import BusinessCategory, BusinessContent

class BusinessService:
    def __init__(self, business_repository):
        self.repository = business_repository
    
    def get_all_categories(self):
        try:
            return self.repository.get_all_categories()
        except Exception:
            return self._get_default_categories()
    
    def _get_default_categories(self):
        categories = []
        
        category1 = BusinessCategory(
            id=1, 
            name="영업관리", 
            description="영업 관련 업무", 
            order=1
        )
        category1.contents = [
            BusinessContent(id=1, category_id=1, name="매출현황", route="sales", icon="fas fa-chart-line", order=1),
            BusinessContent(id=2, category_id=1, name="고객분석", route="customers", icon="fas fa-users", order=2)
        ]
        
        category2 = BusinessCategory(
            id=2, 
            name="재무관리", 
            description="재무 관련 업무", 
            order=2
        )
        category2.contents = [
            BusinessContent(id=3, category_id=2, name="수익분석", route="profit", icon="fas fa-dollar-sign", order=1),
            BusinessContent(id=4, category_id=2, name="비용관리", route="expenses", icon="fas fa-receipt", order=2)
        ]
        
        categories.extend([category1, category2])
        return categories