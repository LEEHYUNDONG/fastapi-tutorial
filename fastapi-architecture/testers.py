"""
어떤 결과를 만들 것인지
개발자 수준에서 tdd가 중요한 이유
기능을 만들기 전에 테스트를 먼저한다. 코드를 안짜고 테스트를 먼저짜고 결과값을 미리 알고
코드 작성에 들어간다.
"""
import unittest
from fastapi.testclient import TestClient
from main import app


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.cookies.clear()

    def test_login_get(self):
        response = self.client.get("/login")
        self.assertEqual(200, response.status_code)

    def test_login_post(self):
        response = self.client.post("/login", data={"username":"hyundong", "password":"password"})
        self.assertEqual(302, response.status_code)
    
    def test_unauthenticated(self):
        response = self.client.post("/login", data = {"username":"hyundong","password":"password"})
        self.assertEqual(302,response.status_code)

        response = self.client.get("/login/test")
        self.assertEqual(200,response.status_code)

if __name__ == "__main__":
    unittest.main()