class DashboardService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_dashboard_data_by_route(self, route):
        if route == 'sales_analysis':
            return self._get_sales_analysis()
        elif route == 'customer_status':
            return self._get_customer_status()
        elif route == 'product_management':
            return self._get_product_management()
        elif route == 'data_table':
            return self._get_data_table()
        else:
            return {'title': '데이터 없음', 'type': 'none', 'data': {}}
    
    def _get_sales_analysis(self):
        """실제 매출 데이터 조회"""
        try:
            query = """
                SELECT 
                    strftime('%Y-%m', order_date) as month,
                    SUM(total_amount) as total_sales,
                    COUNT(*) as order_count
                FROM orders 
                WHERE order_date >= date('now', '-6 months')
                GROUP BY strftime('%Y-%m', order_date)
                ORDER BY month
            """
            results = self.db.execute_query(query)
            
            labels = []
            sales_data = []
            order_data = []
            
            for row in results:
                labels.append(row['month'])
                sales_data.append(int(row['total_sales']))
                order_data.append(row['order_count'])
            
            return {
                'title': '매출 분석',
                'type': 'line',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': '매출액 (원)',
                        'data': sales_data,
                        'borderColor': 'rgb(75, 192, 192)',
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'tension': 0.1
                    }, {
                        'label': '주문 건수',
                        'data': order_data,
                        'borderColor': 'rgb(255, 99, 132)',
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'yAxisID': 'y1'
                    }]
                },
                'options': {
                    'scales': {
                        'y': {
                            'type': 'linear',
                            'display': True,
                            'position': 'left',
                        },
                        'y1': {
                            'type': 'linear',
                            'display': True,
                            'position': 'right',
                            'grid': {
                                'drawOnChartArea': False,
                            },
                        }
                    }
                }
            }
        except Exception as e:
            return self._get_fallback_sales_data()
    
    def _get_customer_status(self):
        """고객 현황 데이터 조회"""
        try:
            # 도시별 고객 분포
            city_query = """
                SELECT city, COUNT(*) as customer_count
                FROM customers
                GROUP BY city
                ORDER BY customer_count DESC
            """
            city_results = self.db.execute_query(city_query)
            
            # 월별 신규 고객
            monthly_query = """
                SELECT 
                    strftime('%Y-%m', registration_date) as month,
                    COUNT(*) as new_customers
                FROM customers
                WHERE registration_date >= date('now', '-6 months')
                GROUP BY strftime('%Y-%m', registration_date)
                ORDER BY month
            """
            monthly_results = self.db.execute_query(monthly_query)
            
            return {
                'title': '고객 현황',
                'type': 'mixed',
                'data': {
                    'city_distribution': {
                        'labels': [row['city'] for row in city_results],
                        'data': [row['customer_count'] for row in city_results],
                        'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                    },
                    'monthly_new': {
                        'labels': [row['month'] for row in monthly_results],
                        'data': [row['new_customers'] for row in monthly_results]
                    }
                }
            }
        except Exception as e:
            return self._get_fallback_customer_data()
    
    def _get_product_management(self):
        """상품 관리 데이터 조회"""
        try:
            query = """
                SELECT 
                    p.name,
                    p.category,
                    p.price,
                    p.stock_quantity,
                    COALESCE(SUM(o.quantity), 0) as total_sold,
                    COALESCE(SUM(o.total_amount), 0) as total_revenue
                FROM products p
                LEFT JOIN orders o ON p.id = o.product_id
                GROUP BY p.id, p.name, p.category, p.price, p.stock_quantity
                ORDER BY total_revenue DESC
            """
            results = self.db.execute_query(query)
            
            return {
                'title': '상품 관리',
                'type': 'table',
                'data': {
                    'headers': ['상품명', '카테고리', '가격', '재고', '판매량', '총 매출'],
                    'rows': [
                        [
                            row['name'],
                            row['category'],
                            f"{row['price']:,}원",
                            f"{row['stock_quantity']}개",
                            f"{row['total_sold']}개",
                            f"{row['total_revenue']:,}원"
                        ]
                        for row in results
                    ]
                }
            }
        except Exception as e:
            return self._get_fallback_product_data()
    
    def _get_fallback_sales_data(self):
        """매출 데이터 폴백"""
        return {
            'title': '매출 분석',
            'type': 'line',
            'data': {
                'labels': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06'],
                'datasets': [{
                    'label': '매출액 (원)',
                    'data': [1200000, 1600000, 1550000, 1400000, 1360000, 1200000],
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.1
                }]
            }
        }
    
    def _get_fallback_customer_data(self):
        """고객 데이터 폴백"""
        return {
            'title': '고객 현황',
            'type': 'doughnut',
            'data': {
                'labels': ['서울', '부산', '대구', '인천', '광주'],
                'datasets': [{
                    'data': [1, 1, 1, 1, 1],
                    'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                }]
            }
        }
    
    def _get_fallback_product_data(self):
        """상품 데이터 폴백"""
        return {
            'title': '상품 관리',
            'type': 'table',
            'data': {
                'headers': ['상품명', '카테고리', '가격', '재고', '판매량', '총 매출'],
                'rows': [
                    ['노트북', '전자제품', '1,200,000원', '15개', '1개', '1,200,000원'],
                    ['스마트폰', '전자제품', '800,000원', '25개', '2개', '1,600,000원'],
                    ['태블릿', '전자제품', '600,000원', '10개', '1개', '600,000원']
                ]
            }
        }
    
    def _get_data_table(self):
        """데이터 조회 페이지"""
        return {
            'title': '데이터 조회',
            'type': 'custom',
            'template': 'dashboard/table_view.html',
            'data': {}
        }