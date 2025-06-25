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
            loading: false,
            advancedFilters: [], // 고급 검색 필터들
            filterCounter: 0 // 필터 ID 카운터
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
            <!-- 기본 검색 -->
            <div class="form-inline mb-2">
                <select class="form-control form-control-sm mr-2" id="${this.containerId}_searchColumn">
                    <option value="">검색 컬럼 선택</option>
                </select>
                <input type="text" class="form-control form-control-sm mr-2" 
                       placeholder="검색어 입력" id="${this.containerId}_searchValue">
                <button type="button" class="btn btn-sm btn-primary mr-2" id="${this.containerId}_searchBtn">
                    <i class="fas fa-search"></i> 검색
                </button>
                <button type="button" class="btn btn-sm btn-secondary mr-2" id="${this.containerId}_resetBtn">
                    <i class="fas fa-undo"></i> 초기화
                </button>
            </div>
            
            <!-- 고급 검색 아코디언 -->
            <div class="card card-outline card-primary">
                <div class="card-header p-2">
                    <a class="btn btn-link btn-sm p-0" data-toggle="collapse" href="#${this.containerId}_advancedSearch" 
                       role="button" aria-expanded="false" aria-controls="${this.containerId}_advancedSearch">
                        <i class="fas fa-filter"></i> 고급 검색 (복합 조건)
                        <i class="fas fa-chevron-down float-right mt-1"></i>
                    </a>
                </div>
                <div class="collapse" id="${this.containerId}_advancedSearch">
                    <div class="card-body p-3">
                        <div id="${this.containerId}_advancedFilters">
                            <!-- 동적으로 생성될 필터들 -->
                        </div>
                        <div class="mt-3">
                            <button type="button" class="btn btn-sm btn-success mr-2" id="${this.containerId}_addFilter">
                                <i class="fas fa-plus"></i> 조건 추가
                            </button>
                            <button type="button" class="btn btn-sm btn-primary mr-2" id="${this.containerId}_applyAdvanced">
                                <i class="fas fa-search"></i> 복합 검색 실행
                            </button>
                            <button type="button" class="btn btn-sm btn-secondary" id="${this.containerId}_clearAdvanced">
                                <i class="fas fa-trash"></i> 모든 조건 삭제
                            </button>
                        </div>
                    </div>
                </div>
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
        
        // 고급 검색 이벤트들
        $(`#${this.containerId}_addFilter`).on('click', function() {
            self.addAdvancedFilter();
        });
        
        $(`#${this.containerId}_applyAdvanced`).on('click', function() {
            self.applyAdvancedSearch();
        });
        
        $(`#${this.containerId}_clearAdvanced`).on('click', function() {
            self.clearAdvancedFilters();
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
            
            // 고급 검색 필터들 추가
            if (this.state.advancedFilters.length > 0) {
                params.append('advanced_filters', JSON.stringify(this.state.advancedFilters));
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
                this.renderAdvancedFilters();
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
        this.state.advancedFilters = [];
        this.state.filterCounter = 0;
        
        $(`#${this.containerId}_searchColumn`).val('');
        $(`#${this.containerId}_searchValue`).val('');
        
        this.renderAdvancedFilters();
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
    
    // 고급 검색 관련 메서드들
    addAdvancedFilter() {
        const filterId = ++this.state.filterCounter;
        const filter = {
            id: filterId,
            column: '',
            operator: 'contains',
            value: '',
            logic: 'AND'
        };
        
        this.state.advancedFilters.push(filter);
        this.renderAdvancedFilters();
    }
    
    renderAdvancedFilters() {
        const container = $(`#${this.containerId}_advancedFilters`);
        
        if (this.state.advancedFilters.length === 0) {
            container.html(`
                <div class="text-muted text-center py-3">
                    <i class="fas fa-info-circle"></i>
                    아직 추가된 검색 조건이 없습니다. "조건 추가" 버튼을 클릭해 주세요.
                </div>
            `);
            return;
        }
        
        let html = '';
        this.state.advancedFilters.forEach((filter, index) => {
            html += this.renderSingleFilter(filter, index);
        });
        
        container.html(html);
        
        // 필터 이벤트 바인딩
        this.bindFilterEvents();
    }
    
    renderSingleFilter(filter, index) {
        const logicDisplay = index === 0 ? '' : `
            <div class="col-md-1 text-center">
                <select class="form-control form-control-sm" data-filter-id="${filter.id}" data-field="logic">
                    <option value="AND" ${filter.logic === 'AND' ? 'selected' : ''}>AND</option>
                    <option value="OR" ${filter.logic === 'OR' ? 'selected' : ''}>OR</option>
                </select>
            </div>
        `;
        
        return `
            <div class="row mb-2 filter-row" data-filter-id="${filter.id}">
                ${logicDisplay}
                <div class="col-md-3">
                    <select class="form-control form-control-sm" data-filter-id="${filter.id}" data-field="column">
                        <option value="">컬럼 선택</option>
                        ${this.getColumnOptions(filter.column)}
                    </select>
                </div>
                <div class="col-md-2">
                    <select class="form-control form-control-sm" data-filter-id="${filter.id}" data-field="operator">
                        <option value="contains" ${filter.operator === 'contains' ? 'selected' : ''}>포함</option>
                        <option value="equals" ${filter.operator === 'equals' ? 'selected' : ''}>같음</option>
                        <option value="not_equals" ${filter.operator === 'not_equals' ? 'selected' : ''}>다름</option>
                        <option value="starts_with" ${filter.operator === 'starts_with' ? 'selected' : ''}>시작</option>
                        <option value="ends_with" ${filter.operator === 'ends_with' ? 'selected' : ''}>끝남</option>
                        <option value="greater_than" ${filter.operator === 'greater_than' ? 'selected' : ''}>초과</option>
                        <option value="less_than" ${filter.operator === 'less_than' ? 'selected' : ''}>미만</option>
                        <option value="is_null" ${filter.operator === 'is_null' ? 'selected' : ''}>NULL</option>
                        <option value="is_not_null" ${filter.operator === 'is_not_null' ? 'selected' : ''}>NOT NULL</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <input type="text" class="form-control form-control-sm" 
                           placeholder="검색값" 
                           value="${filter.value}"
                           data-filter-id="${filter.id}" 
                           data-field="value"
                           ${filter.operator === 'is_null' || filter.operator === 'is_not_null' ? 'disabled' : ''}>
                </div>
                <div class="col-md-1">
                    <button type="button" class="btn btn-sm btn-danger" data-filter-id="${filter.id}" data-action="remove">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }
    
    getColumnOptions(selectedColumn) {
        let options = '';
        this.state.columns.forEach(column => {
            if (column.searchable) {
                const selected = column.key === selectedColumn ? 'selected' : '';
                options += `<option value="${column.key}" ${selected}>${column.label}</option>`;
            }
        });
        return options;
    }
    
    bindFilterEvents() {
        const self = this;
        
        // 필터 값 변경 이벤트
        $(`#${this.containerId}_advancedFilters`).off('change').on('change', 'select, input', function() {
            const filterId = parseInt($(this).data('filter-id'));
            const field = $(this).data('field');
            const value = $(this).val();
            
            const filter = self.state.advancedFilters.find(f => f.id === filterId);
            if (filter) {
                filter[field] = value;
                
                // operator가 is_null이나 is_not_null이면 value 입력창 비활성화
                if (field === 'operator') {
                    const valueInput = $(`input[data-filter-id="${filterId}"][data-field="value"]`);
                    if (value === 'is_null' || value === 'is_not_null') {
                        valueInput.prop('disabled', true).val('');
                        filter.value = '';
                    } else {
                        valueInput.prop('disabled', false);
                    }
                }
            }
        });
        
        // 필터 삭제 이벤트
        $(`#${this.containerId}_advancedFilters`).off('click').on('click', 'button[data-action="remove"]', function() {
            const filterId = parseInt($(this).data('filter-id'));
            self.removeAdvancedFilter(filterId);
        });
    }
    
    removeAdvancedFilter(filterId) {
        this.state.advancedFilters = this.state.advancedFilters.filter(f => f.id !== filterId);
        this.renderAdvancedFilters();
    }
    
    applyAdvancedSearch() {
        // 유효한 필터만 남기기
        this.state.advancedFilters = this.state.advancedFilters.filter(filter => 
            filter.column && (
                filter.operator === 'is_null' || 
                filter.operator === 'is_not_null' || 
                filter.value.trim()
            )
        );
        
        if (this.state.advancedFilters.length === 0) {
            alert('적어도 하나의 유효한 검색 조건을 입력해주세요.');
            return;
        }
        
        // 기본 검색 초기화
        this.state.searchColumn = null;
        this.state.searchValue = '';
        $(`#${this.containerId}_searchColumn`).val('');
        $(`#${this.containerId}_searchValue`).val('');
        
        this.state.currentPage = 1;
        this.loadData();
    }
    
    clearAdvancedFilters() {
        this.state.advancedFilters = [];
        this.state.filterCounter = 0;
        this.renderAdvancedFilters();
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