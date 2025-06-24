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
});