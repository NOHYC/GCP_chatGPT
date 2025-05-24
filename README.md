# 🚀 Streamlit on GCP via Docker CI/CD

이 프로젝트는 **Streamlit 앱을 Docker 컨테이너로 패키징**하고,  
**GitHub Actions를 통해 DockerHub → GCP VM까지 자동 배포**하는 파이프라인을 구현합니다.

---

## 📦 프로젝트 구조

streamlit-docker-gcp-cicd/

├── app.py # Streamlit 앱

├── requirements.txt # Python 패키지 목록

├── Dockerfile # Docker 이미지 정의

└── .github/

└── workflows/

└── deploy.yml # GitHub Actions CI/CD 스크립트






## ⚙️ 자동 배포 흐름



1. `main` 브랜치에 코드 Push
2. GitHub Actions가 동작하여:
   - Docker 이미지 빌드
   - DockerHub에 푸시
   - GCP VM에 SSH 접속 후 컨테이너 실행

3. GCP 외부 IP에서 앱 확인 → `http://YOUR_GCP_IP`


#📍 GCP 설정 체크리스트
 GCP VM 생성 (Ubuntu 기반)

 도커 설치 및 usermod -aG docker 사용자명

 외부 IP 고정 또는 업데이트 시 GitHub Secret 갱신

 방화벽에서 포트 22(SSH), 80(HTTP) 허용


