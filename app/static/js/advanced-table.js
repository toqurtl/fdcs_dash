/**
 * 고급 테이블 컴포넌트
 * - 페이지네이션
 * - 검색 및 필터링 
 * - 정렬
 * - 대용량 데이터 지원
 */

class AdvancedTable {
    constructor(containerId, tableName, options = {}) {
        this.containerId = containerId;
        this.tableName = tableName;
        this.container = $('#' + containerId);
        
        // 기본 옵션
        this.options = {
            perPage: 50,
            showSearch: true,
            showFilters: true,
            showPagination: true,
            ...options
        };
        
        // 상태 관리
        this.state = {
            currentPage: 1,
            perPage: this.options.perPage,
            searchColumn: null,
            searchValue: '',
            sortColumn: null,
            sortDirection: 'ASC',
            data: [],
            columns: [],
            pagination: {},
            loading: false
        };
        
        this.init();
    }
    
    async init() {
        this.render();
        await this.loadData();
    }
    
    render() {
        const html = `
            <div class="advanced-table-container">
                <!-- 검색 및 필터 영역 -->
                <div class="table-controls mb-3">
                    <div class="row">
                        <div class="col-md-6">
                            ${this.options.showSearch ? this.renderSearchForm() : ''}
                        </div>
                        <div class="col-md-6">
                            <div class="float-right">
                                <select class="form-control form-control-sm d-inline-block" 
                                        style="width: auto;" id="${this.containerId}_perPage">
                                    <option value="25">25개씩</option>
                                    <option value="50" selected>50개씩</option>
                                    <option value="100">100개씩</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 테이블 영역 -->
                <div class="table-responsive">
                    <table class="table table-striped table-hover" id="${this.containerId}_table">
                        <thead id="${this.containerId}_thead"></thead>
                        <tbody id="${this.containerId}_tbody">
                            <tr>
                                <td colspan="100%" class="text-center">
                                    <i class="fas fa-spinner fa-spin"></i> 데이터를 불러오는 중...
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <!-- 페이지네이션 영역 -->
                ${this.options.showPagination ? '<div id="' + this.containerId + '_pagination"></div>' : ''}
                
                <!-- 정보 영역 -->
                <div class="table-info mt-2">
                    <small class="text-muted" id="${this.containerId}_info"></small>
                </div>
            </div>
        `;
        
        this.container.html(html);
        this.bindEvents();
    }
    
    renderSearchForm() {
        return `
            <div class="form-inline">
                <select class="form-control form-control-sm mr-2" id="${this.containerId}_searchColumn">
                    <option value="">검색 컬럼 선택</option>
                </select>
                <input type="text" class="form-control form-control-sm mr-2" 
                       placeholder="검색어 입력" id="${this.containerId}_searchValue">
                <button type="button" class="btn btn-sm btn-primary mr-2" id="${this.containerId}_searchBtn">
                    <i class="fas fa-search"></i> 검색
                </button>
                <button type="button" class="btn btn-sm btn-secondary" id="${this.containerId}_resetBtn">
                    <i class="fas fa-undo"></i> 초기화
                </button>
            </div>
        `;
    }
    
    bindEvents() {
        const self = this;
        
        // 페이지당 항목 수 변경
        $(`#${this.containerId}_perPage`).on('change', function() {
            self.state.perPage = parseInt($(this).val());
            self.state.currentPage = 1;
            self.loadData();
        });
        
        // 검색 버튼
        $(`#${this.containerId}_searchBtn`).on('click', function() {
            self.search();
        });
        
        // 검색어 엔터키
        $(`#${this.containerId}_searchValue`).on('keypress', function(e) {
            if (e.which === 13) {
                self.search();
            }
        });
        
        // 초기화 버튼
        $(`#${this.containerId}_resetBtn`).on('click', function() {
            self.reset();
        });
    }
    
    async loadData() {
        if (this.state.loading) return;
        
        this.state.loading = true;
        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                page: this.state.currentPage,
                per_page: this.state.perPage
            });
            
            if (this.state.searchColumn && this.state.searchValue) {
                params.append('search_column', this.state.searchColumn);
                params.append('search_value', this.state.searchValue);
            }
            
            if (this.state.sortColumn) {
                params.append('sort_column', this.state.sortColumn);
                params.append('sort_direction', this.state.sortDirection);
            }
            
            const response = await fetch(`/api/table/${this.tableName}?${params}`);
            const result = await response.json();
            
            if (result.success) {
                this.state.data = result.data.data;
                this.state.columns = result.data.columns;
                this.state.pagination = result.data.pagination;
                
                this.renderTable();
                this.renderPagination();
                this.renderInfo();
                this.populateSearchColumns();
            } else {
                throw new Error(result.error);
            }
            
        } catch (error) {
            console.error('데이터 로드 실패:', error);
            this.showError('데이터를 불러오는데 실패했습니다: ' + error.message);
        } finally {
            this.state.loading = false;
        }
    }
    
    renderTable() {
        // 테이블 헤더 렌더링
        let headerHtml = '<tr>';
        this.state.columns.forEach(column => {
            const sortIcon = this.getSortIcon(column.key);
            const sortClass = column.sortable ? 'sortable' : '';
            
            headerHtml += `
                <th class="${sortClass}" data-column="${column.key}">
                    ${column.label}
                    ${column.sortable ? sortIcon : ''}
                </th>
            `;
        });
        headerHtml += '</tr>';
        
        $(`#${this.containerId}_thead`).html(headerHtml);
        
        // 정렬 이벤트 바인딩
        $(`#${this.containerId}_thead th.sortable`).on('click', (e) => {
            const column = $(e.currentTarget).data('column');
            this.sort(column);
        });
        
        // 테이블 바디 렌더링
        let bodyHtml = '';
        if (this.state.data.length === 0) {
            bodyHtml = `
                <tr>
                    <td colspan="${this.state.columns.length}" class="text-center text-muted">
                        데이터가 없습니다.
                    </td>
                </tr>
            `;
        } else {
            this.state.data.forEach(row => {
                bodyHtml += '<tr>';
                this.state.columns.forEach(column => {
                    const value = row[column.key];
                    const formattedValue = this.formatValue(value, column.type);
                    bodyHtml += `<td>${formattedValue}</td>`;
                });
                bodyHtml += '</tr>';
            });
        }
        
        $(`#${this.containerId}_tbody`).html(bodyHtml);
    }
    
    renderPagination() {
        if (!this.options.showPagination) return;
        
        const p = this.state.pagination;
        if (p.total_pages <= 1) {
            $(`#${this.containerId}_pagination`).html('');
            return;
        }
        
        let html = '<nav><ul class="pagination pagination-sm justify-content-center">';
        
        // 이전 페이지
        html += `
            <li class="page-item ${!p.has_prev ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${p.current_page - 1}">이전</a>
            </li>
        `;
        
        // 페이지 번호들
        const startPage = Math.max(1, p.current_page - 2);
        const endPage = Math.min(p.total_pages, p.current_page + 2);
        
        if (startPage > 1) {
            html += '<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>';
            if (startPage > 2) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const active = i === p.current_page ? 'active' : '';
            html += `<li class="page-item ${active}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
        }
        
        if (endPage < p.total_pages) {
            if (endPage < p.total_pages - 1) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
            html += `<li class="page-item"><a class="page-link" href="#" data-page="${p.total_pages}">${p.total_pages}</a></li>`;
        }
        
        // 다음 페이지
        html += `
            <li class="page-item ${!p.has_next ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${p.current_page + 1}">다음</a>
            </li>
        `;
        
        html += '</ul></nav>';
        
        $(`#${this.containerId}_pagination`).html(html);
        
        // 페이지네이션 이벤트 바인딩
        $(`#${this.containerId}_pagination a.page-link`).on('click', (e) => {
            e.preventDefault();
            const page = parseInt($(e.currentTarget).data('page'));
            if (page && page !== this.state.currentPage) {
                this.goToPage(page);
            }
        });
    }
    
    renderInfo() {
        const p = this.state.pagination;
        const start = (p.current_page - 1) * p.per_page + 1;
        const end = Math.min(p.current_page * p.per_page, p.total_count);
        
        const info = `총 ${p.total_count.toLocaleString()}건 중 ${start.toLocaleString()}-${end.toLocaleString()}건 표시`;
        $(`#${this.containerId}_info`).text(info);
    }
    
    populateSearchColumns() {
        const searchColumnSelect = $(`#${this.containerId}_searchColumn`);
        searchColumnSelect.empty().append('<option value="">검색 컬럼 선택</option>');
        
        this.state.columns.forEach(column => {
            if (column.searchable) {
                searchColumnSelect.append(`<option value="${column.key}">${column.label}</option>`);
            }
        });
    }
    
    getSortIcon(columnKey) {
        if (this.state.sortColumn === columnKey) {
            return this.state.sortDirection === 'ASC' 
                ? '<i class="fas fa-sort-up ml-1"></i>'
                : '<i class="fas fa-sort-down ml-1"></i>';
        }
        return '<i class="fas fa-sort ml-1 text-muted"></i>';
    }
    
    formatValue(value, type) {
        if (value === null || value === undefined) return '-';
        
        switch (type) {
            case 'currency':
                return Number(value).toLocaleString() + '원';
            case 'number':
                return Number(value).toLocaleString();
            case 'date':
                return new Date(value).toLocaleDateString('ko-KR');
            case 'datetime':
                return new Date(value).toLocaleString('ko-KR');
            case 'status':
                return this.getStatusBadge(value);
            case 'email':
                return `<a href="mailto:${value}">${value}</a>`;
            default:
                return String(value);
        }
    }
    
    getStatusBadge(status) {
        const statusConfig = {
            'pending': { label: '대기중', class: 'warning' },
            'processing': { label: '처리중', class: 'info' },
            'shipped': { label: '배송중', class: 'primary' },
            'delivered': { label: '배송완료', class: 'success' },
            'cancelled': { label: '취소됨', class: 'danger' },
            'returned': { label: '반품됨', class: 'secondary' }
        };
        
        const config = statusConfig[status] || { label: status, class: 'light' };
        return `<span class="badge badge-${config.class}">${config.label}</span>`;
    }
    
    showLoading() {
        $(`#${this.containerId}_tbody`).html(`
            <tr>
                <td colspan="${this.state.columns.length || 100}" class="text-center">
                    <i class="fas fa-spinner fa-spin"></i> 데이터를 불러오는 중...
                </td>
            </tr>
        `);
    }
    
    showError(message) {
        $(`#${this.containerId}_tbody`).html(`
            <tr>
                <td colspan="${this.state.columns.length || 100}" class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </td>
            </tr>
        `);
    }
    
    search() {
        this.state.searchColumn = $(`#${this.containerId}_searchColumn`).val();
        this.state.searchValue = $(`#${this.containerId}_searchValue`).val().trim();
        this.state.currentPage = 1;
        this.loadData();
    }
    
    reset() {
        this.state.searchColumn = null;
        this.state.searchValue = '';
        this.state.currentPage = 1;
        this.state.sortColumn = null;
        this.state.sortDirection = 'ASC';
        
        $(`#${this.containerId}_searchColumn`).val('');
        $(`#${this.containerId}_searchValue`).val('');
        
        this.loadData();
    }
    
    sort(column) {
        if (this.state.sortColumn === column) {
            this.state.sortDirection = this.state.sortDirection === 'ASC' ? 'DESC' : 'ASC';
        } else {
            this.state.sortColumn = column;
            this.state.sortDirection = 'ASC';
        }
        
        this.state.currentPage = 1;
        this.loadData();
    }
    
    goToPage(page) {
        if (page < 1 || page > this.state.pagination.total_pages) return;
        
        this.state.currentPage = page;
        this.loadData();
    }
    
    refresh() {
        this.loadData();
    }
}

// CSS 추가
const tableCSS = `
<style>
.advanced-table-container .sortable {
    cursor: pointer;
    user-select: none;
}

.advanced-table-container .sortable:hover {
    background-color: #f8f9fa;
}

.advanced-table-container .table th {
    border-top: none;
    font-weight: 600;
}

.advanced-table-container .pagination {
    margin-bottom: 0;
}

.advanced-table-container .badge {
    font-size: 0.75em;
}
</style>
`;

$('head').append(tableCSS);