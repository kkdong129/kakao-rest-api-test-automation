import unittest
import requests
import json
import os

class Kakao_Test_Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            cls.config = json.load(f)

    def setUp(self):
        self.access_token = self.config['kakao_api']['access_token']
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }


class Test_01_Kakao_POSITIVE_API(Kakao_Test_Base):
    def test_TC_01_send_me_commerce_message(self):
        """[Scenario] 토큰 검증부터 나에게 메시지 전송, 사용자 정보 조회까지 통합 시나리오"""

        print(f"\n{'=' * 60}")
        print(f" 시작: KAKAO API TEST (Positive Flow)")
        print(f"{'=' * 60}")

        # Step 1: 토큰 정보 가져오기
        info_url = "https://kapi.kakao.com/v1/user/access_token_info"
        info_res = requests.get(info_url, headers=self.headers)

        self.assertEqual(info_res.status_code, 200)
        info_json = info_res.json()
        print(f"▶ Step 1. 액세스 토큰 유효성 검증 완료")
        print(f"  - App ID: {info_json.get('id')}")
        print(f"  - Expires In: {info_json.get('expires_in')} sec")

        # Step 2: 나에게 메시지 보내기
        msg_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        commerce_data = self.config['test_data']['commerce_template']

        # 버튼 리스트 생성 로직
        commerce_buttons = [
            {
                "title": btn['title'],
                "link": {"web_url": btn['web_url'], "mobile_web_url": btn['mobile_web_url']}
            } for btn in commerce_data['buttons']
        ]

        template_object = {
            "object_type": "commerce",
            "content": {
                "title": commerce_data['title'],
                "image_url": commerce_data['links']['image_url'],
                "link": {
                    "web_url": commerce_data['links']['web_url'],
                    "mobile_web_url": commerce_data['links']['mobile_web_url']
                }
            },
            "commerce": {
                "regular_price": 68900,
                "discount_price": 49700,
                "discount_rate": 27
            },
            "buttons": commerce_buttons
        }

        payload = {"template_object": json.dumps(template_object)}
        msg_res = requests.post(msg_url, headers=self.headers, data=payload)

        self.assertEqual(msg_res.status_code, 200)
        self.assertEqual(msg_res.json().get('result_code'), 0)
        print(f"▶ Step 2. 나에게 커머스 메시지 전송 완료")
        print(f"  - 상품명: {commerce_data['title']}")
        print(f"  - 버튼 개수: {len(commerce_buttons)}")

        # Step 3: 사용자 정보 가져오기
        user_url = "https://kapi.kakao.com/v2/user/me"
        user_res = requests.get(user_url, headers=self.headers)

        self.assertEqual(user_res.status_code, 200)
        user_json = user_res.json()
        nickname = user_json.get('properties', {}).get('nickname')

        self.assertIsNotNone(nickname)
        print(f"▶ Step 3. 사용자 정보 조회 및 검증 완료")
        print(f"  - 사용자 닉네임: {nickname}")
        print(f"  - 회원 고유번호(ID): {user_json.get('id')}")

        print(f"{'=' * 60}")


class Test_02_Kakao_NEGATIVE_API(Kakao_Test_Base):
    def setUp(self):
        super().setUp()
        self.neg_data = self.config['test_data']['negative_test_data']

    def test_TC_01_invalid_token_failure(self):
        print(f"\n{'=' * 60}")
        print(f" 시작: KAKAO API TEST (Nagative Flow)")
        print(f"{'=' * 60}")

        """[Negative] 유효하지 않은 토큰 사용 시 401 에러 검증"""
        self.invalid_headers = {
            "Authorization": "Bearer INVALID_TOKEN_12345",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        url = "https://kapi.kakao.com/v1/user/access_token_info"
        response = requests.get(url, headers=self.invalid_headers)

        res_json = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(res_json.get('code'), -401)

        # 상세 에러 정보 출력
        print(f"\n[TC-01] 유효하지 않은 토큰 검증 성공")
        print(f"  - HTTP Status: {response.status_code}")
        print(f"  - Kakao Error Code: {res_json.get('code')}")
        print(f"  - Kakao Message: {res_json.get('msg')}")

    def test_TC_02_invalid_url_path_failure(self):
        """[Negative] 잘못된 URL 경로 접근 시 404 에러 검증"""
        invalid_url = "https://kapi.kakao.com/v2/user/mes"
        response = requests.get(invalid_url, headers=self.headers)

        self.assertEqual(response.status_code, 404)

        # 404의 경우 카카오가 JSON 바디를 주지 않을 수 있으므로 체크 후 출력
        print(f"\n[TC-02] 잘못된 URL 경로 차단 검증 성공")
        print(f"  - HTTP Status: {response.status_code}")
        if response.text:
            print(f"  - Response: {response.text}")

    def test_TC_03_missing_parameter_failure(self):
        """[Negative] 필수 파라미터(template_object) 누락 시 에러 검증"""
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        response = requests.post(url, headers=self.headers, data={})

        res_json = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(res_json.get('code'), -2)

        print(f"\n[TC-03] 필수 파라미터 누락 검증 성공")
        print(f"  - HTTP Status: {response.status_code}")
        print(f"  - Kakao Error Code: {res_json.get('code')}")
        print(f"  - Kakao Message: {res_json.get('msg')}")

    def test_TC_04_invalid_json_format_failure(self):
        """[Negative] 잘못된 JSON 형식 전송 시 에러 검증"""
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        payload = {"template_object": self.neg_data['invalid_json_format']}
        response = requests.post(url, headers=self.headers, data=payload)

        res_json = response.json()
        self.assertEqual(response.status_code, 400)

        print(f"\n[TC-04] 데이터 규격 오류 검증 성공")
        print(f"  - HTTP Status: {response.status_code}")
        print(f"  - Kakao Error Code: {res_json.get('code')}")
        print(f"  - Kakao Message: {res_json.get('msg')}")

if __name__ == "__main__":
    unittest.main()