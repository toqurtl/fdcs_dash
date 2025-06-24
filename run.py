import os
import sys

# 현재 스크립트의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
os.chdir(current_dir)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print(f"🚀 서버 시작 중... (현재 디렉토리: {os.getcwd()})")
    print(f"📁 템플릿 폴더: {os.path.join(current_dir, 'templates')}")
    app.run(debug=True, host='0.0.0.0', port=5000)