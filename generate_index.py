#!/usr/bin/env python3
import os
import json
from datetime import datetime

def find_html_files():
    html_files = []
    for root, dirs, files in os.walk('.'):
        # 忽略隐藏文件夹
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path)
                size = os.path.getsize(full_path)
                html_files.append({
                    'name': file,
                    'path': rel_path,
                    'size': size,
                    'folder': os.path.dirname(rel_path) if os.path.dirname(rel_path) != '.' else '根目录'
                })
    return sorted(html_files, key=lambda x: x['path'])

def generate_index(html_files):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面导航 - 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .page-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
        .page-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
        .page-card:hover {{ background: #f5f5f5; }}
        .page-card a {{ text-decoration: none; color: #0366d6; font-size: 16px; }}
        .page-info {{ font-size: 12px; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>📁 仓库页面导航</h1>
    <p>共找到 {len(html_files)} 个HTML页面（自动生成）</p>
    
    <div class="page-list">
''')
        
        for page in html_files:
            f.write(f'''
        <div class="page-card">
            <a href="{page['path']}">{page['name']}</a>
            <div class="page-info">
                路径: {page['folder']}<br>
                大小: {page['size']} bytes
            </div>
        </div>
''')
        
        f.write(f'''
    </div>
    <footer style="margin-top: 40px; color: #666; font-size: 12px;">
        最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </footer>
</body>
</html>
''')

if __name__ == '__main__':
    html_files = find_html_files()
    generate_index(html_files)
    print(f"已生成索引，包含 {len(html_files)} 个页面")