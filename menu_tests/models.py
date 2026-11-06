from django.db import models  # noqa: F401

# MenuTest, Ingredient
# - 추가 고정비는 MenuTest.additional_fixed_cost 단일 값 (FixedCost 모델 없음)
# - status는 저장하지 않고 started_at / ended_at으로 계산
