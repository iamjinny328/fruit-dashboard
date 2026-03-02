"""
구글 드라이브 자동 업로드 모듈
- 수집된 Excel 파일을 구글 드라이브에 자동 업로드
- 팀원들과 공유 가능한 폴더에 저장
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API 권한 범위
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveUploader:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """
        구글 드라이브 업로더 초기화
        
        Args:
            credentials_file: OAuth 2.0 인증 파일 경로
            token_file: 인증 토큰 저장 파일 경로
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """구글 드라이브 인증"""
        creds = None
        
        # 기존 토큰 파일 확인
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # 토큰이 없거나 유효하지 않으면 새로 인증
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 토큰 갱신 중...")
                creds.refresh(Request())
            else:
                print("🔐 구글 드라이브 인증 시작...")
                print("⚠️  브라우저가 열리면 구글 계정으로 로그인하세요!")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # 토큰 저장
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
            print("✅ 인증 완료!")
        
        self.service = build('drive', 'v3', credentials=creds)
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """
        구글 드라이브에 폴더 생성
        
        Args:
            folder_name: 생성할 폴더 이름
            parent_folder_id: 상위 폴더 ID (None이면 루트)
        
        Returns:
            생성된 폴더 ID
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"📁 폴더 생성: {folder.get('name')}")
        print(f"🔗 공유 링크: {folder.get('webViewLink')}")
        
        return folder.get('id')
    
    def find_folder(self, folder_name):
        """
        폴더 검색
        
        Args:
            folder_name: 검색할 폴더 이름
        
        Returns:
            폴더 ID (없으면 None)
        """
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        return files[0]['id'] if files else None
    
    def upload_file(self, file_path, folder_id=None, share_with_anyone=False):
        """
        파일 업로드
        
        Args:
            file_path: 업로드할 파일 경로
            folder_id: 업로드할 폴더 ID (None이면 루트)
            share_with_anyone: True면 링크 있는 사람 누구나 접근 가능
        
        Returns:
            업로드된 파일 정보 (ID, 웹 링크)
        """
        file_name = os.path.basename(file_path)
        
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, resumable=True)
        
        print(f"📤 업로드 중: {file_name}...")
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink, size'
        ).execute()
        
        file_id = file.get('id')
        
        # 공유 설정
        if share_with_anyone:
            self.service.permissions().create(
                fileId=file_id,
                body={
                    'type': 'anyone',
                    'role': 'reader'  # 읽기 전용
                }
            ).execute()
            print(f"🔓 공유 설정: 링크 있는 사람 누구나 접근 가능")
        
        print(f"✅ 업로드 완료: {file.get('name')} ({file.get('size')} bytes)")
        print(f"🔗 웹 링크: {file.get('webViewLink')}")
        
        return {
            'id': file_id,
            'name': file.get('name'),
            'webViewLink': file.get('webViewLink')
        }
    
    def list_files(self, folder_id=None, max_results=10):
        """
        파일 목록 조회
        
        Args:
            folder_id: 조회할 폴더 ID (None이면 루트)
            max_results: 최대 결과 수
        
        Returns:
            파일 목록
        """
        query = "trashed=false"
        if folder_id:
            query = f"'{folder_id}' in parents and trashed=false"
        
        results = self.service.files().list(
            q=query,
            pageSize=max_results,
            fields='files(id, name, modifiedTime, size, webViewLink)',
            orderBy='modifiedTime desc'
        ).execute()
        
        return results.get('files', [])
    
    def download_file(self, file_id, save_path):
        """
        파일 다운로드
        
        Args:
            file_id: 다운로드할 파일 ID
            save_path: 저장 경로
        """
        request = self.service.files().get_media(fileId=file_id)
        
        import io
        from googleapiclient.http import MediaIoBaseDownload
        
        fh = io.FileIO(save_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"📥 다운로드 진행: {int(status.progress() * 100)}%")
        
        print(f"✅ 다운로드 완료: {save_path}")


# 사용 예시
if __name__ == "__main__":
    # 업로더 초기화
    uploader = GoogleDriveUploader()
    
    # 폴더 생성 (최초 1회만)
    folder_id = uploader.find_folder('과일가격수집_데이터')
    if not folder_id:
        folder_id = uploader.create_folder('과일가격수집_데이터')
    
    # 파일 업로드 테스트
    # uploader.upload_file('다중사이트_20260204_1821.xlsx', folder_id, share_with_anyone=True)
    
    # 파일 목록 조회
    files = uploader.list_files(folder_id)
    print("\n📂 업로드된 파일:")
    for f in files:
        print(f"  - {f.get('name')} ({f.get('size')} bytes) - {f.get('modifiedTime')}")
