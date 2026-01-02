# 📦 Kakao REST API Test Automation

카카오 메시지 API를 활용한 서비스 통합 시나리오 및 예외 케이스(Negative Test) 자동화 테스트 프로젝트입니다.  
Python의 `unittest`와 `Postman`을 사용하여 API의 신뢰성을 검증합니다.

---

## 🚀 Project Overview

본 프로젝트는 카카오 REST API의 주요 기능을 체인(Chain) 형태로 엮은 통합 시나리오 테스트와, 다양한 에러 상황을 가정한 부정 테스트(Negative Test)를 포함합니다. 
실제 서비스 환경에서 발생할 수 있는 데이터 규격 오류 및 인증 문제를 자동화된 스크립트로 검증하는 데 목적이 있습니다.

---

## 🛠 Tech Stack

- **Language:** Python
- **Test Framwork:** unittest
- **Library:** Requests, Unittest
- **Tool:** Postman (Collection & Environment)
- **Configuration:** JSON 기반 환경 설정 관리

---

## 📂 Project Structure

```text
kakao-rest-api-test-automation/
├── tests/
│   └── kakao_rest_api_test.py   # Python Unittest 스크립트
├── postman/
│   ├── kakao_test.json          # Postman Collection v2.1
│   └── kakao_env.json           # Postman Environment
├── config.sample.json           # 환경 설정 샘플 파일
└── README.md                    # 프로젝트 가이드
```

---

## 🧪 Test Scenarios
### 1. Test_01: Positive Flow (통합 시나리오)
비즈니스 로직의 연속성을 검증하기 위한 시나리오입니다.
- Step 1. 액세스 토큰 유효성 검증: 현재 사용 중인 토큰의 유효 기간 및 App ID 확인
- Step 2. 나에게 메시지 전송: 커머스 템플릿(Commerce Template)을 활용한 카카오톡 메시지 발송
- Step 3. 사용자 정보 조회: 전송 완료 후 내 계정 정보(닉네임 등)를 조회하여 최종 응답 확인
### 2. Test_02: Negative Flow (예외 케이스)
API의 견고함을 검증하기 위한 부정 테스트 케이스입니다.
- TC-01 (401): 유효하지 않은 토큰(Invalid Token) 사용 시 에러코드 확인
- TC-02 (404): 잘못된 URL 엔드포인트 접근 시 에러코드 확인
- TC-03 (400): 필수 파라미터(template_object) 누락 시 에러코드 확인
- TC-04 (400): JSON 문법 오류(Syntax Error)가 포함된 데이터 전송 시 에러코드 확인

---

## 🛠️ 설정 및 실행 방법 (Setup & Execution)
### Configuration
config.sample.json 파일을 복사하여 config.json을 생성합니다.
카카오 개발자 센터에서 발급받은 access_token을 입력합니다.
주의: config.json은 보안을 위해 git 추적에서 제외되어 있습니다.

### Execution (Python)
테스트 실행 및 결과 확인
```Bash
python kakao_rest_api_test.py
```

### Execution (Postman)
- postman/ 폴더 내의 Collection과 Environment JSON 파일을 Postman에 Import 합니다.
- 우측 상단 환경 설정에서 Import한 환경 변수(Environment)를 선택합니다.
- accessToken 변수 값에 본인의 카카오 API 토큰을 입력하고 저장합니다.
- Collection 내의 개별 Request를 순서대로 선택하여 실행(Send)하고, 하단에 응답 결과를 확인합니다.
