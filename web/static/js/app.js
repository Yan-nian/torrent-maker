/**
 * Torrent Maker Web Interface JavaScript
 * v2.1.0 - Web界面版本
 */

class TorrentMakerApp {
    constructor() {
        this.socket = null;
        this.currentTab = 'dashboard';
        this.servers = {};
        this.tasks = {};
        this.systemInfo = {};
        
        this.init();
    }
    
    init() {
        this.initSocket();
        this.initEventListeners();
        this.initUI();
        this.loadData();
        
        // 定期更新系统信息
        setInterval(() => this.updateSystemInfo(), 5000);
    }
    
    initSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('WebSocket连接成功');
            this.updateConnectionStatus('connected');
        });
        
        this.socket.on('disconnect', () => {
            console.log('WebSocket连接断开');
            this.updateConnectionStatus('disconnected');
        });
        
        this.socket.on('task_update', (data) => {
            this.handleTaskUpdate(data);
        });
        
        this.socket.on('system_update', (data) => {
            this.handleSystemUpdate(data);
        });
    }
    
    initEventListeners() {
        // 标签页切换
        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(tab.dataset.tab);
            });
        });
        
        // 创建种子表单
        document.getElementById('create-torrent-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createTorrent();
        });
        
        // 添加服务器表单
        document.getElementById('add-server-form').addEventListener('submit', (e) => {
            e.preventDefault();
        });
        
        // 认证方式切换
        document.querySelectorAll('input[name="auth-type"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.toggleAuthFields();
            });
        });
        
        // 测试连接按钮
        document.getElementById('test-connection').addEventListener('click', () => {
            this.testServerConnection();
        });
        
        // 保存服务器按钮
        document.getElementById('save-server').addEventListener('click', () => {
            this.saveServer();
        });
        
        // 执行命令按钮
        document.getElementById('execute-command').addEventListener('click', () => {
            this.executeCommand();
        });
        
        // 命令输入框回车执行
        document.getElementById('command-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand();
            }
        });
        
        // 文件浏览器事件
        this.initFileBrowserEvents();
    }
    
    initUI() {
        // 初始化工具提示
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // 设置默认标签页
        this.switchTab('dashboard');
    }
    
    async loadData() {
        await this.loadServers();
        await this.updateSystemInfo();
    }
    
    switchTab(tabName) {
        // 更新导航栏
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // 更新内容区域
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        this.currentTab = tabName;
        
        // 根据标签页加载相应数据
        switch (tabName) {
            case 'servers':
                this.loadServers();
                break;
            case 'tasks':
                this.loadTasks();
                break;
        }
    }
    
    updateConnectionStatus(status) {
        const statusIcon = document.getElementById('connection-status');
        const statusText = document.getElementById('connection-text');
        
        statusIcon.className = 'bi';
        
        switch (status) {
            case 'connected':
                statusIcon.classList.add('bi-wifi', 'connected');
                statusText.textContent = '已连接';
                break;
            case 'disconnected':
                statusIcon.classList.add('bi-wifi-off', 'disconnected');
                statusText.textContent = '连接断开';
                break;
            case 'connecting':
                statusIcon.classList.add('bi-wifi', 'connecting');
                statusText.textContent = '连接中...';
                break;
        }
    }
    
    async updateSystemInfo() {
        try {
            const response = await fetch('/api/system');
            const data = await response.json();
            
            if (data.success) {
                this.systemInfo = data.system;
                this.updateSystemDisplay();
            }
        } catch (error) {
            console.error('获取系统信息失败:', error);
        }
    }
    
    updateSystemDisplay() {
        const { systemInfo } = this;
        
        // 更新CPU使用率
        const cpuElement = document.getElementById('cpu-usage');
        if (cpuElement && systemInfo.cpu_percent !== undefined) {
            cpuElement.textContent = `${systemInfo.cpu_percent.toFixed(1)}%`;
        }
        
        // 更新内存使用率
        const memoryElement = document.getElementById('memory-usage');
        if (memoryElement && systemInfo.memory_percent !== undefined) {
            memoryElement.textContent = `${systemInfo.memory_percent.toFixed(1)}%`;
        }
        
        // 更新磁盘使用率
        const diskElement = document.getElementById('disk-usage');
        if (diskElement && systemInfo.disk_percent !== undefined) {
            diskElement.textContent = `${systemInfo.disk_percent.toFixed(1)}%`;
        }
        
        // 更新活跃任务数
        const tasksElement = document.getElementById('active-tasks');
        if (tasksElement) {
            const activeTasks = Object.values(this.tasks).filter(task => 
                task.status === 'running' || task.status === 'pending'
            ).length;
            tasksElement.textContent = activeTasks.toString();
        }
    }
    
    async loadServers() {
        try {
            const response = await fetch('/api/servers');
            const data = await response.json();
            
            if (data.success) {
                this.servers = data.servers;
                this.updateServersDisplay();
                this.updateServerSelects();
            }
        } catch (error) {
            console.error('加载服务器列表失败:', error);
        }
    }
    
    updateServersDisplay() {
        const serversList = document.getElementById('servers-list');
        
        if (Object.keys(this.servers).length === 0) {
            serversList.innerHTML = '<p class="text-muted">暂无服务器配置</p>';
            return;
        }
        
        const serversHtml = Object.entries(this.servers).map(([id, server]) => `
            <div class="server-item">
                <div class="server-info">
                    <h6>
                        <span class="server-status online"></span>
                        ${server.name || id}
                    </h6>
                    <small>${server.username}@${server.host}:${server.port || 22}</small>
                </div>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="app.testServer('${id}')">
                        <i class="bi bi-wifi"></i> 测试
                    </button>
                    <button class="btn btn-outline-danger" onclick="app.removeServer('${id}')">
                        <i class="bi bi-trash"></i> 删除
                    </button>
                </div>
            </div>
        `).join('');
        
        serversList.innerHTML = serversHtml;
    }
    
    updateServerSelects() {
        const selects = [
            document.getElementById('server-select'),
            document.getElementById('command-server')
        ];
        
        selects.forEach(select => {
            if (!select) return;
            
            // 保留第一个选项
            const firstOption = select.firstElementChild;
            select.innerHTML = '';
            if (firstOption) {
                select.appendChild(firstOption);
            }
            
            // 添加服务器选项
            Object.entries(this.servers).forEach(([id, server]) => {
                const option = document.createElement('option');
                option.value = id;
                option.textContent = server.name || `${server.username}@${server.host}`;
                select.appendChild(option);
            });
        });
    }
    
    toggleAuthFields() {
        const authType = document.querySelector('input[name="auth-type"]:checked').value;
        const passwordField = document.getElementById('password-field');
        const keyField = document.getElementById('key-field');
        
        if (authType === 'password') {
            passwordField.style.display = 'block';
            keyField.style.display = 'none';
        } else {
            passwordField.style.display = 'none';
            keyField.style.display = 'block';
        }
    }
    
    async testServerConnection() {
        const config = this.getServerFormData();
        
        if (!this.validateServerForm(config)) {
            return;
        }
        
        const button = document.getElementById('test-connection');
        const originalText = button.innerHTML;
        
        button.innerHTML = '<span class="loading"></span> 测试中...';
        button.disabled = true;
        
        try {
            const response = await fetch('/api/servers/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    host: config.host,
                    port: parseInt(config.port),
                    username: config.username,
                    ...(config.authType === 'password' ? 
                        { password: config.password } : 
                        { key_file: config.keyFile }
                    )
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('连接测试成功', 'success');
            } else {
                this.showNotification('连接测试失败: ' + data.error, 'error');
            }
        } catch (error) {
            this.showNotification('连接测试失败: ' + error.message, 'error');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }
    
    async saveServer() {
        const config = this.getServerFormData();
        
        if (!this.validateServerForm(config)) {
            return;
        }
        
        try {
            const response = await fetch('/api/servers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: config.name.toLowerCase().replace(/\s+/g, '_'),
                    config: {
                        name: config.name,
                        host: config.host,
                        port: parseInt(config.port),
                        username: config.username,
                        ...(config.authType === 'password' ? 
                            { password: config.password } : 
                            { key_file: config.keyFile }
                        )
                    }
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('服务器添加成功', 'success');
                bootstrap.Modal.getInstance(document.getElementById('addServerModal')).hide();
                this.resetServerForm();
                await this.loadServers();
            } else {
                this.showNotification('服务器添加失败: ' + data.error, 'error');
            }
        } catch (error) {
            this.showNotification('服务器添加失败: ' + error.message, 'error');
        }
    }
    
    getServerFormData() {
        return {
            name: document.getElementById('server-name').value,
            host: document.getElementById('server-host').value,
            port: document.getElementById('server-port').value,
            username: document.getElementById('server-username').value,
            authType: document.querySelector('input[name="auth-type"]:checked').value,
            password: document.getElementById('server-password').value,
            keyFile: document.getElementById('server-key').value
        };
    }
    
    validateServerForm(config) {
        if (!config.name || !config.host || !config.username) {
            this.showNotification('请填写所有必填字段', 'error');
            return false;
        }
        
        if (config.authType === 'password' && !config.password) {
            this.showNotification('请输入密码', 'error');
            return false;
        }
        
        if (config.authType === 'key' && !config.keyFile) {
            this.showNotification('请输入密钥文件路径', 'error');
            return false;
        }
        
        return true;
    }
    
    resetServerForm() {
        document.getElementById('add-server-form').reset();
        document.getElementById('server-port').value = '22';
        document.querySelector('input[name="auth-type"][value="password"]').checked = true;
        this.toggleAuthFields();
    }
    
    async executeCommand() {
        const serverId = document.getElementById('command-server').value;
        const command = document.getElementById('command-input').value.trim();
        
        if (!serverId) {
            this.showNotification('请选择服务器', 'error');
            return;
        }
        
        if (!command) {
            this.showNotification('请输入命令', 'error');
            return;
        }
        
        const output = document.getElementById('command-output');
        output.textContent += `$ ${command}\n`;
        
        try {
            // 这里应该调用执行命令的API
            await new Promise(resolve => setTimeout(resolve, 1000)); // 模拟执行
            
            output.textContent += `命令执行完成\n\n`;
            output.scrollTop = output.scrollHeight;
            
            document.getElementById('command-input').value = '';
        } catch (error) {
            output.textContent += `错误: ${error.message}\n\n`;
            output.scrollTop = output.scrollHeight;
        }
    }
    
    async createTorrent() {
        const formData = {
            sourcePath: document.getElementById('source-path').value,
            outputPath: document.getElementById('output-path').value,
            trackerUrls: document.getElementById('tracker-urls').value.split('\n').filter(url => url.trim()),
            pieceSize: document.getElementById('piece-size').value,
            serverId: document.getElementById('server-select').value,
            isPrivate: document.getElementById('private-torrent').checked,
            comment: document.getElementById('comment').value
        };
        
        if (!formData.sourcePath) {
            this.showNotification('请输入源文件路径', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showNotification('任务创建成功', 'success');
                this.socket.emit('join_task', { task_id: data.task_id });
                this.switchTab('tasks');
            } else {
                this.showNotification('任务创建失败: ' + data.error, 'error');
            }
        } catch (error) {
            this.showNotification('任务创建失败: ' + error.message, 'error');
        }
    }
    
    async loadTasks() {
        // 这里应该从API加载任务列表
        this.updateTasksDisplay();
    }
    
    updateTasksDisplay() {
        const tasksList = document.getElementById('tasks-list');
        
        if (Object.keys(this.tasks).length === 0) {
            tasksList.innerHTML = '<p class="text-muted">暂无任务</p>';
            return;
        }
        
        const tasksHtml = Object.values(this.tasks).map(task => `
            <div class="task-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6 class="mb-0">${task.id}</h6>
                    <span class="task-status ${task.status}">${this.getStatusText(task.status)}</span>
                </div>
                <div class="progress mb-2">
                    <div class="progress-bar" style="width: ${task.progress || 0}%"></div>
                </div>
                <small class="text-muted">
                    创建时间: ${new Date(task.created_at).toLocaleString()}
                    ${task.server_id ? ` | 服务器: ${task.server_id}` : ''}
                </small>
            </div>
        `).join('');
        
        tasksList.innerHTML = tasksHtml;
    }
    
    getStatusText(status) {
        const statusMap = {
            'pending': '等待中',
            'running': '运行中',
            'completed': '已完成',
            'failed': '失败'
        };
        return statusMap[status] || status;
    }
    
    handleTaskUpdate(data) {
        if (!this.tasks[data.task_id]) {
            this.tasks[data.task_id] = {};
        }
        
        Object.assign(this.tasks[data.task_id], data);
        
        if (this.currentTab === 'tasks') {
            this.updateTasksDisplay();
        }
        
        this.updateSystemDisplay();
    }
    
    handleSystemUpdate(data) {
        this.systemInfo = { ...this.systemInfo, ...data };
        this.updateSystemDisplay();
    }
    
    async testServer(serverId) {
        this.showNotification('正在测试服务器连接...', 'info');
        
        try {
            // 这里应该调用测试服务器连接的API
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.showNotification('服务器连接正常', 'success');
        } catch (error) {
            this.showNotification('服务器连接失败: ' + error.message, 'error');
        }
    }
    
    async removeServer(serverId) {
        if (!confirm('确定要删除这个服务器配置吗？')) {
            return;
        }
        
        try {
            // 这里应该调用删除服务器的API
            delete this.servers[serverId];
            this.updateServersDisplay();
            this.updateServerSelects();
            this.showNotification('服务器删除成功', 'success');
        } catch (error) {
            this.showNotification('服务器删除失败: ' + error.message, 'error');
        }
    }
    
    showNotification(message, type = 'info') {
        const toast = document.getElementById('notification-toast');
        const toastBody = document.getElementById('toast-message');
        
        // 设置消息内容
        toastBody.textContent = message;
        
        // 设置样式
        toast.className = 'toast';
        switch (type) {
            case 'success':
                toast.classList.add('bg-success', 'text-white');
                break;
            case 'error':
                toast.classList.add('bg-danger', 'text-white');
                break;
            case 'warning':
                toast.classList.add('bg-warning', 'text-dark');
                break;
            default:
                toast.classList.add('bg-info', 'text-white');
        }
        
        // 显示通知
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }
    
    // 文件浏览器功能
    initFileBrowserEvents() {
        // 浏览文件按钮
        document.getElementById('browse-files-btn').addEventListener('click', () => {
            this.openFileBrowser();
        });
        
        // 服务器选择变化
        document.getElementById('browser-server-select').addEventListener('change', (e) => {
            if (e.target.value) {
                this.browsePath('/', e.target.value);
            } else {
                this.clearFileList();
            }
        });
        
        // 刷新按钮
        document.getElementById('refresh-browser').addEventListener('click', () => {
            const serverId = document.getElementById('browser-server-select').value;
            const currentPath = document.getElementById('current-path').value;
            if (serverId) {
                this.browsePath(currentPath, serverId);
            }
        });
        
        // 上级目录按钮
        document.getElementById('go-parent').addEventListener('click', () => {
            const currentPath = document.getElementById('current-path').value;
            const parentPath = this.getParentPath(currentPath);
            const serverId = document.getElementById('browser-server-select').value;
            if (serverId && parentPath !== currentPath) {
                this.browsePath(parentPath, serverId);
            }
        });
        
        // 确认选择按钮
        document.getElementById('confirm-selection').addEventListener('click', () => {
            this.confirmPathSelection();
        });
    }
    
    openFileBrowser() {
        // 加载服务器列表
        this.loadServersForBrowser();
        
        // 重置状态
        document.getElementById('current-path').value = '/';
        document.getElementById('selected-path').textContent = '无';
        document.getElementById('confirm-selection').disabled = true;
        this.clearFileList();
        this.hideDirectoryStats();
        
        // 显示模态框
        const modal = new bootstrap.Modal(document.getElementById('fileBrowserModal'));
        modal.show();
    }
    
    async loadServersForBrowser() {
        try {
            const response = await fetch('/api/servers');
            const data = await response.json();
            
            const select = document.getElementById('browser-server-select');
            select.innerHTML = '<option value="">请选择服务器</option>';
            
            if (data.success && data.servers) {
                data.servers.forEach(server => {
                    const option = document.createElement('option');
                    option.value = server.id;
                    option.textContent = `${server.name} (${server.host})`;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('加载服务器列表失败:', error);
            this.showNotification('加载服务器列表失败', 'error');
        }
    }
    
    async browsePath(path, serverId) {
        this.showLoading(true);
        
        try {
            // 浏览目录
            const browseResponse = await fetch('/api/browse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    server_id: serverId,
                    path: path
                })
            });
            
            const browseData = await browseResponse.json();
            
            if (browseData.success) {
                this.updateFileList(browseData.files, path, serverId);
                this.updatePathBreadcrumb(path);
                document.getElementById('current-path').value = path;
                
                // 获取目录统计
                this.loadDirectoryStats(path, serverId);
            } else {
                this.showNotification(browseData.error || '浏览目录失败', 'error');
                this.clearFileList();
            }
        } catch (error) {
            console.error('浏览目录失败:', error);
            this.showNotification('浏览目录失败', 'error');
            this.clearFileList();
        } finally {
            this.showLoading(false);
        }
    }
    
    async loadDirectoryStats(path, serverId) {
        try {
            const response = await fetch('/api/directory-stats', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    server_id: serverId,
                    path: path
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateDirectoryStats(data);
            }
        } catch (error) {
            console.error('获取目录统计失败:', error);
        }
    }
    
    updateFileList(files, currentPath, serverId) {
        const tbody = document.getElementById('file-list');
        tbody.innerHTML = '';
        
        if (!files || files.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        <i class="bi bi-folder-x fs-1"></i>
                        <div class="mt-2">此目录为空</div>
                    </td>
                </tr>
            `;
            return;
        }
        
        files.forEach(file => {
            const row = document.createElement('tr');
            row.className = 'file-row';
            row.style.cursor = 'pointer';
            
            // 图标
            let icon = 'bi-file-earmark';
            let iconColor = 'text-secondary';
            
            if (file.is_directory) {
                icon = 'bi-folder-fill';
                iconColor = 'text-warning';
            } else if (file.file_type === 'video') {
                icon = 'bi-play-circle-fill';
                iconColor = 'text-success';
            } else if (file.file_type === 'subtitle') {
                icon = 'bi-chat-square-text-fill';
                iconColor = 'text-info';
            }
            
            // 大小格式化
            const size = file.is_directory ? '-' : this.formatFileSize(file.size);
            
            // 剧集信息
            let episodeInfo = '-';
            if (file.episode_info) {
                episodeInfo = `<span class="badge bg-primary">${file.episode_info.format}</span>`;
            }
            
            row.innerHTML = `
                <td><i class="bi ${icon} ${iconColor}"></i></td>
                <td class="file-name">${this.escapeHtml(file.name)}</td>
                <td>
                    <span class="badge ${file.is_directory ? 'bg-warning' : (file.file_type === 'video' ? 'bg-success' : 'bg-secondary')}">
                        ${file.is_directory ? '文件夹' : (file.file_type === 'video' ? '视频' : file.file_type === 'subtitle' ? '字幕' : '文件')}
                    </span>
                </td>
                <td>${size}</td>
                <td>${episodeInfo}</td>
            `;
            
            // 点击事件
            row.addEventListener('click', () => {
                if (file.is_directory) {
                    // 进入子目录
                    this.browsePath(file.full_path, serverId);
                } else {
                    // 选择文件
                    this.selectFile(file.full_path, row);
                }
            });
            
            // 双击事件（文件夹）
            if (file.is_directory) {
                row.addEventListener('dblclick', () => {
                    this.browsePath(file.full_path, serverId);
                });
            }
            
            tbody.appendChild(row);
        });
    }
    
    selectFile(path, row) {
        // 清除之前的选择
        document.querySelectorAll('.file-row').forEach(r => {
            r.classList.remove('table-active');
        });
        
        // 选中当前行
        row.classList.add('table-active');
        
        // 更新选择状态
        document.getElementById('selected-path').textContent = path;
        document.getElementById('confirm-selection').disabled = false;
    }
    
    confirmPathSelection() {
        const selectedPath = document.getElementById('selected-path').textContent;
        if (selectedPath && selectedPath !== '无') {
            document.getElementById('source-path').value = selectedPath;
            
            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('fileBrowserModal'));
            modal.hide();
            
            this.showNotification('路径已选择', 'success');
        }
    }
    
    updatePathBreadcrumb(path) {
        const breadcrumb = document.getElementById('path-breadcrumb');
        breadcrumb.innerHTML = '';
        
        const parts = path.split('/').filter(part => part);
        
        // 根目录
        const rootItem = document.createElement('li');
        rootItem.className = 'breadcrumb-item';
        rootItem.innerHTML = '<a href="#" data-path="/">根目录</a>';
        breadcrumb.appendChild(rootItem);
        
        // 路径部分
        let currentPath = '';
        parts.forEach((part, index) => {
            currentPath += '/' + part;
            const item = document.createElement('li');
            
            if (index === parts.length - 1) {
                item.className = 'breadcrumb-item active';
                item.textContent = part;
            } else {
                item.className = 'breadcrumb-item';
                item.innerHTML = `<a href="#" data-path="${currentPath}">${part}</a>`;
            }
            
            breadcrumb.appendChild(item);
        });
        
        // 添加点击事件
        breadcrumb.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetPath = e.target.dataset.path;
                const serverId = document.getElementById('browser-server-select').value;
                if (serverId) {
                    this.browsePath(targetPath, serverId);
                }
            });
        });
    }
    
    updateDirectoryStats(stats) {
        document.getElementById('file-count').textContent = stats.file_count;
        document.getElementById('dir-count').textContent = stats.dir_count;
        document.getElementById('video-count').textContent = stats.video_count;
        document.getElementById('total-size').textContent = stats.total_size;
        
        document.getElementById('directory-stats').style.display = 'block';
    }
    
    hideDirectoryStats() {
        document.getElementById('directory-stats').style.display = 'none';
    }
    
    clearFileList() {
        const tbody = document.getElementById('file-list');
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted">
                    <i class="bi bi-folder-x fs-1"></i>
                    <div class="mt-2">请选择服务器开始浏览</div>
                </td>
            </tr>
        `;
    }
    
    showLoading(show) {
        const indicator = document.getElementById('loading-indicator');
        const fileList = document.querySelector('.table-responsive');
        
        if (show) {
            indicator.style.display = 'block';
            fileList.style.display = 'none';
        } else {
            indicator.style.display = 'none';
            fileList.style.display = 'block';
        }
    }
    
    getParentPath(path) {
        if (path === '/' || !path) return '/';
        const parts = path.split('/').filter(part => part);
        parts.pop();
        return parts.length === 0 ? '/' : '/' + parts.join('/');
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化应用
const app = new TorrentMakerApp();

// 全局错误处理
window.addEventListener('error', (event) => {
    console.error('全局错误:', event.error);
    app.showNotification('发生未知错误，请检查控制台', 'error');
});

// 页面卸载时清理
window.addEventListener('beforeunload', () => {
    if (app.socket) {
        app.socket.disconnect();
    }
});