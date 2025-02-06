from locust import HttpUser, task, between
import random
import json

class BoardUser(HttpUser):
    # 사용자 간 요청 간격 설정 (1~3초 대기)
    wait_time = between(1, 3)
    
    @task(2)
    def get_board_list(self):
        # 전체 Board 목록 조회 API 호출
        with self.client.get("/boards", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"GET /boards 실패: {response.status_code}")

    @task(2)
    def get_board(self):
        # 특정 board id 조회 (여기서는 1 ~ 100 사이의 임의 id 사용)
        board_id = random.randint(1, 100)
        with self.client.get(f"/boards/{board_id}", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"GET /boards/{board_id} 실패: {response.status_code}")

    @task(1)
    def create_board(self):
        # 새로운 Board 생성 API 호출. 이름에 랜덤 값을 부여해 중복을 피함
        board_data = {
            "name": f"Board_{random.randint(1,10000)}",
            "description": "샘플 게시판 설명"
        }
        headers = {"Content-Type": "application/json"}
        with self.client.post("/boards", data=json.dumps(board_data), headers=headers, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"POST /boards 실패: {response.status_code}")

    @task(1)
    def delete_board(self):
        # 삭제 테스트: 존재할 법한 board id를 선택 (실제 운영에서는 삭제 가능 여부를 고려하여 구현 필요)
        board_id = random.randint(1, 100)
        with self.client.delete(f"/boards/{board_id}", catch_response=True) as response:
            # 없는 경우 404가 오는 것도 정상 상황일 수 있으므로 이를 고려
            if response.status_code not in [200, 204, 404]:
                response.failure(f"DELETE /boards/{board_id} 실패: {response.status_code}")
