$(document).ready(function() {
    // 사이드바 콘텐츠 클릭 이벤트
    $('.content-link').on('click', function(e) {
        e.preventDefault();
        
        var route = $(this).data('route');
        loadDashboardContent(route);
        
        // 활성 상태 변경
        $('.content-link').removeClass('active');
        $(this).addClass('active');
    });
    
    function loadDashboardContent(route) {
        $('#dynamic-content').html('<div class="text-center"><i class="fas fa-spinner fa-spin"></i> 로딩 중...</div>');
        
        $.ajax({
            url: '/api/dashboard-data/' + route,
            method: 'GET',
            success: function(data) {
                renderDashboardContent(data);
            },
            error: function() {
                $('#dynamic-content').html('<div class="alert alert-danger">데이터를 불러오는데 실패했습니다.</div>');
            }
        });
    }
    
    function renderDashboardContent(data) {
        if (data.type === 'custom' || data.title === '데이터 조회') {
            // 데이터 조회 페이지 렌더링
            renderDataTablePage();
            return;
        }
        
        var html = '<div class="col-12"><div class="card"><div class="card-header"><h3 class="card-title">' 
                  + data.title + '</h3></div><div class="card-body">';
        
        if (data.type === 'table') {
            html += renderTable(data.data);
        } else if (data.type === 'mixed') {
            html += renderMixedContent(data.data);
        } else if (data.type !== 'none') {
            html += '<canvas id="dynamicChart" style="min-height: 300px; height: 300px; max-height: 300px; max-width: 100%;"></canvas>';
        } else {
            html += '<p>표시할 데이터가 없습니다.</p>';
        }
        
        html += '</div></div></div>';
        
        $('#dynamic-content').html(html);
        
        if (data.type === 'mixed') {
            renderMixedCharts(data.data);
        } else if (data.type !== 'table' && data.type !== 'none' && data.type !== 'mixed') {
            renderChart(data);
        }
    }
    
    function renderDataTablePage() {
        var html = `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-database"></i> 대용량 데이터 조회 시스템
                        </h3>
                    </div>
                    <div class="card-body">
                        <p class="text-muted mb-4">검색, 정렬, 페이지네이션을 지원하는 고급 테이블 시스템입니다.</p>
                        
                        <!-- 테이블 선택 카드들 -->
                        <div class="row mb-4">
                            <div class="col-md-4">
                                <div class="card table-card" data-table="orders_view" style="cursor: pointer;">
                                    <div class="card-body text-center">
                                        <i class="fas fa-shopping-cart fa-3x text-primary mb-3"></i>
                                        <h5>주문 현황</h5>
                                        <p class="text-muted">고객별 주문 내역과 상품 정보</p>
                                        <span class="badge badge-primary" id="orders_count">로딩중...</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card table-card" data-table="customers" style="cursor: pointer;">
                                    <div class="card-body text-center">
                                        <i class="fas fa-users fa-3x text-success mb-3"></i>
                                        <h5>고객 관리</h5>
                                        <p class="text-muted">고객 정보 및 지역별 분포</p>
                                        <span class="badge badge-success" id="customers_count">로딩중...</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card table-card" data-table="products" style="cursor: pointer;">
                                    <div class="card-body text-center">
                                        <i class="fas fa-box fa-3x text-warning mb-3"></i>
                                        <h5>상품 목록</h5>
                                        <p class="text-muted">상품 정보 및 재고 현황</p>
                                        <span class="badge badge-warning" id="products_count">로딩중...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 테이블 컨테이너 -->
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">
                                    <i class="fas fa-table"></i> 
                                    <span id="current-table-title">테이블을 선택해주세요</span>
                                </h3>
                                <div class="card-tools">
                                    <button type="button" class="btn btn-sm btn-primary" id="refresh-table" style="display: none;">
                                        <i class="fas fa-sync-alt"></i> 새로고침
                                    </button>
                                </div>
                            </div>
                            <div class="card-body">
                                <div id="table-container">
                                    <div class="text-center text-muted py-5">
                                        <i class="fas fa-table fa-3x mb-3"></i>
                                        <h5>조회할 테이블을 선택해주세요</h5>
                                        <p>위의 카드를 클릭하여 데이터를 조회할 수 있습니다.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 통계 정보 -->
                        <div class="row mt-3" id="stats-section" style="display: none;">
                            <div class="col-md-3">
                                <div class="small-box bg-info">
                                    <div class="inner">
                                        <h3 id="stat-total">0</h3>
                                        <p>총 데이터</p>
                                    </div>
                                    <div class="icon">
                                        <i class="fas fa-database"></i>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="small-box bg-success">
                                    <div class="inner">
                                        <h3 id="stat-pages">0</h3>
                                        <p>총 페이지</p>
                                    </div>
                                    <div class="icon">
                                        <i class="fas fa-copy"></i>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="small-box bg-warning">
                                    <div class="inner">
                                        <h3 id="stat-current">0</h3>
                                        <p>현재 페이지</p>
                                    </div>
                                    <div class="icon">
                                        <i class="fas fa-bookmark"></i>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="small-box bg-danger">
                                    <div class="inner">
                                        <h3 id="stat-showing">0</h3>
                                        <p>표시 중</p>
                                    </div>
                                    <div class="icon">
                                        <i class="fas fa-eye"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $('#dynamic-content').html(html);
        
        // 데이터 테이블 기능 초기화
        initDataTableFeatures();
    }
    
    function renderTable(tableData) {
        var html = '<table class="table table-striped"><thead><tr>';
        
        tableData.headers.forEach(function(header) {
            html += '<th>' + header + '</th>';
        });
        
        html += '</tr></thead><tbody>';
        
        tableData.rows.forEach(function(row) {
            html += '<tr>';
            row.forEach(function(cell) {
                html += '<td>' + cell + '</td>';
            });
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        
        return html;
    }
    
    function renderMixedContent(data) {
        var html = '<div class="row">';
        html += '<div class="col-md-6"><canvas id="cityChart" style="min-height: 250px; height: 250px;"></canvas></div>';
        html += '<div class="col-md-6"><canvas id="monthlyChart" style="min-height: 250px; height: 250px;"></canvas></div>';
        html += '</div>';
        return html;
    }
    
    function renderMixedCharts(data) {
        // 도시별 고객 분포 차트
        if (data.city_distribution) {
            var cityCtx = document.getElementById('cityChart').getContext('2d');
            new Chart(cityCtx, {
                type: 'doughnut',
                data: {
                    labels: data.city_distribution.labels,
                    datasets: [{
                        data: data.city_distribution.data,
                        backgroundColor: data.city_distribution.backgroundColor
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '지역별 고객 분포'
                        }
                    }
                }
            });
        }
        
        // 월별 신규 고객 차트
        if (data.monthly_new) {
            var monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
            new Chart(monthlyCtx, {
                type: 'bar',
                data: {
                    labels: data.monthly_new.labels,
                    datasets: [{
                        label: '신규 고객',
                        data: data.monthly_new.data,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '월별 신규 고객'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
    
    function renderChart(data) {
        var ctx = document.getElementById('dynamicChart').getContext('2d');
        
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        };
        
        // 차트 타입에 따른 옵션 설정
        if (data.type === 'line' || data.type === 'bar') {
            options.scales = {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString() + '원';
                        }
                    }
                }
            };
            
            // 듀얼 축 지원 (매출 분석용)
            if (data.options && data.options.scales) {
                options.scales = data.options.scales;
            }
        }
        
        new Chart(ctx, {
            type: data.type,
            data: data.data,
            options: options
        });
    }
    
    function initDataTableFeatures() {
        let currentTable = null;
        
        // 테이블 선택 카드 클릭 이벤트
        $(document).off('click', '.table-card').on('click', '.table-card', function() {
            const tableName = $(this).data('table');
            selectTable(tableName);
        });
        
        // 새로고침 버튼
        $(document).off('click', '#refresh-table').on('click', '#refresh-table', function() {
            if (currentTable) {
                currentTable.refresh();
            }
        });
        
        function selectTable(tableName) {
            // 카드 활성화 상태 변경
            $('.table-card').removeClass('border-primary');
            $(`.table-card[data-table="${tableName}"]`).addClass('border-primary');
            
            // 테이블 제목 변경
            const titles = {
                'orders_view': '주문 현황',
                'customers': '고객 관리', 
                'products': '상품 목록'
            };
            $('#current-table-title').text(titles[tableName] || tableName);
            
            // 새로고침 버튼 표시
            $('#refresh-table').show();
            
            // 기존 테이블 제거
            if (currentTable) {
                currentTable = null;
            }
            
            // 새 테이블 생성
            $('#table-container').html('<div id="advanced-table"></div>');
            currentTable = new AdvancedTable('advanced-table', tableName, {
                perPage: 50,
                showSearch: true,
                showFilters: true,
                showPagination: true
            });
            
            // 통계 섹션 표시
            $('#stats-section').show();
            
            // 테이블 데이터 로드 완료 후 통계 업데이트
            setTimeout(function() {
                updateStats(currentTable);
            }, 1000);
        }
        
        function updateStats(table) {
            if (table && table.state.pagination) {
                const p = table.state.pagination;
                $('#stat-total').text(p.total_count.toLocaleString());
                $('#stat-pages').text(p.total_pages.toLocaleString());
                $('#stat-current').text(p.current_page.toLocaleString());
                
                const start = (p.current_page - 1) * p.per_page + 1;
                const end = Math.min(p.current_page * p.per_page, p.total_count);
                $('#stat-showing').text(`${start}-${end}`);
            }
        }
        
        // 초기 데이터 카운트 로드
        loadTableCounts();
        
        function loadTableCounts() {
            const tables = ['orders_view', 'customers', 'products'];
            
            tables.forEach(table => {
                $.get(`/api/table/${table}?per_page=1`, function(response) {
                    if (response.success) {
                        const count = response.data.pagination.total_count;
                        const countElement = table === 'orders_view' ? '#orders_count' : `#${table}_count`;
                        $(countElement).text(`${count.toLocaleString()}건`);
                    }
                }).fail(function() {
                    const countElement = table === 'orders_view' ? '#orders_count' : `#${table}_count`;
                    $(countElement).text('오류');
                });
            });
        }
    }
});