from math import ceil

class TableService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_table_data(self, table_name, page=1, per_page=50, search_column=None, search_value=None, sort_column=None, sort_direction='ASC'):
        """
        테이블 데이터를 페이지네이션과 검색 기능과 함께 조회
        
        Args:
            table_name: 테이블 명
            page: 페이지 번호 (1부터 시작)
            per_page: 페이지당 항목 수
            search_column: 검색할 컬럼명
            search_value: 검색값
            sort_column: 정렬할 컬럼명
            sort_direction: 정렬 방향 (ASC/DESC)
        """
        try:
            # 기본 쿼리 구성
            base_query = self._get_base_query(table_name)
            count_query = self._get_count_query(table_name)
            
            # WHERE 절 추가
            where_clause = ""
            params = []
            
            if search_column and search_value:
                where_clause = f" WHERE {search_column} LIKE ?"
                params.append(f"%{search_value}%")
            
            # ORDER BY 절 추가
            order_clause = ""
            if sort_column:
                order_clause = f" ORDER BY {sort_column} {sort_direction}"
            
            # 전체 개수 조회
            total_count_query = count_query + where_clause
            total_count = self.db.execute_query(total_count_query, params)[0]['count']
            
            # 페이지네이션 계산
            offset = (page - 1) * per_page
            total_pages = ceil(total_count / per_page)
            
            # LIMIT/OFFSET 절 추가
            limit_clause = f" LIMIT ? OFFSET ?"
            params.extend([per_page, offset])
            
            # 최종 쿼리 실행
            final_query = base_query + where_clause + order_clause + limit_clause
            data = self.db.execute_query(final_query, params)
            
            # 컬럼 정보 조회
            columns = self._get_table_columns(table_name)
            
            return {
                'data': data,
                'pagination': {
                    'current_page': page,
                    'per_page': per_page,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_prev': page > 1,
                    'has_next': page < total_pages
                },
                'columns': columns,
                'search': {
                    'column': search_column,
                    'value': search_value
                },
                'sort': {
                    'column': sort_column,
                    'direction': sort_direction
                }
            }
            
        except Exception as e:
            raise Exception(f"테이블 데이터 조회 실패: {str(e)}")
    
    def _get_base_query(self, table_name):
        """테이블별 기본 쿼리 반환"""
        if table_name == 'orders_view':
            return """
                SELECT 
                    o.id,
                    c.name as customer_name,
                    c.city as customer_city,
                    p.name as product_name,
                    p.category as product_category,
                    o.quantity,
                    o.unit_price,
                    o.total_amount,
                    o.order_date,
                    o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                JOIN products p ON o.product_id = p.id
            """
        elif table_name == 'customers':
            return "SELECT id, name, email, phone, city, registration_date FROM customers"
        elif table_name == 'products':
            return "SELECT id, name, category, price, stock_quantity, created_at FROM products"
        else:
            return f"SELECT * FROM {table_name}"
    
    def _get_count_query(self, table_name):
        """전체 개수 조회 쿼리 반환"""
        if table_name == 'orders_view':
            return """
                SELECT COUNT(*) as count
                FROM orders o
                JOIN customers c ON o.customer_id = c.id
                JOIN products p ON o.product_id = p.id
            """
        else:
            return f"SELECT COUNT(*) as count FROM {table_name}"
    
    def _get_table_columns(self, table_name):
        """테이블 컬럼 정보 반환"""
        column_configs = {
            'orders_view': [
                {'key': 'id', 'label': 'ID', 'type': 'number', 'searchable': True, 'sortable': True},
                {'key': 'customer_name', 'label': '고객명', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'customer_city', 'label': '지역', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'product_name', 'label': '상품명', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'product_category', 'label': '카테고리', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'quantity', 'label': '수량', 'type': 'number', 'searchable': True, 'sortable': True},
                {'key': 'unit_price', 'label': '단가', 'type': 'currency', 'searchable': True, 'sortable': True},
                {'key': 'total_amount', 'label': '총액', 'type': 'currency', 'searchable': True, 'sortable': True},
                {'key': 'order_date', 'label': '주문일', 'type': 'date', 'searchable': True, 'sortable': True},
                {'key': 'status', 'label': '상태', 'type': 'status', 'searchable': True, 'sortable': True}
            ],
            'customers': [
                {'key': 'id', 'label': 'ID', 'type': 'number', 'searchable': True, 'sortable': True},
                {'key': 'name', 'label': '이름', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'email', 'label': '이메일', 'type': 'email', 'searchable': True, 'sortable': True},
                {'key': 'phone', 'label': '전화번호', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'city', 'label': '지역', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'registration_date', 'label': '가입일', 'type': 'date', 'searchable': True, 'sortable': True}
            ],
            'products': [
                {'key': 'id', 'label': 'ID', 'type': 'number', 'searchable': True, 'sortable': True},
                {'key': 'name', 'label': '상품명', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'category', 'label': '카테고리', 'type': 'text', 'searchable': True, 'sortable': True},
                {'key': 'price', 'label': '가격', 'type': 'currency', 'searchable': True, 'sortable': True},
                {'key': 'stock_quantity', 'label': '재고', 'type': 'number', 'searchable': True, 'sortable': True},
                {'key': 'created_at', 'label': '등록일', 'type': 'datetime', 'searchable': True, 'sortable': True}
            ]
        }
        
        return column_configs.get(table_name, [])
    
    def get_filter_options(self, table_name, column_name):
        """특정 컬럼의 필터 옵션 조회 (DISTINCT 값들)"""
        try:
            if table_name == 'orders_view':
                if column_name == 'customer_city':
                    query = "SELECT DISTINCT c.city as value FROM orders o JOIN customers c ON o.customer_id = c.id ORDER BY c.city"
                elif column_name == 'product_category':
                    query = "SELECT DISTINCT p.category as value FROM orders o JOIN products p ON o.product_id = p.id ORDER BY p.category"
                elif column_name == 'status':
                    query = "SELECT DISTINCT status as value FROM orders ORDER BY status"
                else:
                    return []
            else:
                query = f"SELECT DISTINCT {column_name} as value FROM {table_name} WHERE {column_name} IS NOT NULL ORDER BY {column_name}"
            
            results = self.db.execute_query(query)
            return [row['value'] for row in results]
            
        except Exception as e:
            return []